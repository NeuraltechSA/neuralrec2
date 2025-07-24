from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable
from av.container import  OutputContainer
from typing_extensions import final, override
from src.Domain.Recording.Profiles.Contracts.ProfileRecorder import ProfileRecorder
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Infraestructure.SharedKernel.PyventusBus import PyventusBus
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
import av
import os

@final
class PyAvProfileRecorder(ProfileRecorder):
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))
    __futures: list[Future[Any]] = [] # pyright: ignore[reportExplicitAny]
    
    def __init__(self, 
                 logger: LoggerInterface,
                 time_provider: TimeProviderInterface,
                 event_bus: PyventusBus):
        super().__init__(event_bus)
        self.__logger = logger
        self.__time_provider = time_provider
        self.__thread_pool = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)
        
    def __get_input_options(self):
        timeout_microseconds = 30 * 1000000
        return {
            "rtsp_transport": "tcp",
            "timeout": str(timeout_microseconds)
        }
    
    def __get_video_file_path(self, profile: Profile, storage_path: ProfileVideoStoragePath):
        time_title = self.__time_provider.now_local().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{storage_path.value}/{profile.video_prefix.value}_{time_title}.mkv"

    def __handle_packet(self, packet: av.Packet, out_stream: av.VideoStream, output: OutputContainer):
        # We need to skip the "flushing" packets that `demux` generates.
        if packet.dts is None: return
        packet.stream = out_stream
        output.mux(packet)

    def __duration_reached(self, dts:int | None, profile: Profile):
        if dts is None: return False
        return int(dts/1000) >= profile.recording_seconds.value

    def __remux(self, 
                profile: Profile,
                output_path: str):
        input = av.open(profile.uri.value, format="rtsp", options=self.__get_input_options())
        output = av.open(output_path, mode="w")
        try:
            in_stream = input.streams.video[0]
            out_stream:av.VideoStream = output.add_stream_from_template(in_stream) # pyright: ignore[reportUnknownMemberType]
            for packet in input.demux(in_stream):
                self.__handle_packet(packet, out_stream, output)
                if self.__duration_reached(packet.dts, profile):
                    break
                
        except av.HTTPBadRequestError as e:
            self.__logger.error(f"Error de autenticación: {e}")
            raise e
        except av.HTTPNotFoundError as e:
            self.__logger.error(f"Stream no encontrado: {e}")
            raise e
        except Exception as e:
            self.__logger.error(f"Error desconocido al grabar el video: {e}")
            raise e
        finally:
            input.close()
            output.close()

    @override
    def _record_async(self, 
                            profile: Profile, 
                            storage_path: ProfileVideoStoragePath, 
                            on_recording_finished: Callable[[Profile, str], None]
                            ) -> None:
        output_path = self.__get_video_file_path(profile, storage_path)
        self.__logger.info(f"Recording video with pyav: {storage_path.value}")
        def task():
            self.__remux(profile, output_path)
            on_recording_finished(profile, output_path)
        future = self.__thread_pool.submit(task)
        self.__futures.append(future)
        self.__futures = [f for f in self.__futures if not f.done()]
    
    def wait_recordings_to_finish(self):
        self.__thread_pool.shutdown()
        self.__futures = []