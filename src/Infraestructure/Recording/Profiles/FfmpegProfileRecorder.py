import threading
import time
from typing_extensions import final
from typing import Callable
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Services.RecordingFinishedStrategy import ProfileRecordingFinishedStrategy
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.Recording.Profiles.Contracts.ProfileRecorder import ProfileRecorder
from src.Domain.Recording.Profiles.Entities.Profile import Profile
import ffmpeg
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
import asyncio
from src.Infraestructure.SharedKernel.PyventusBus import PyventusBus

@final
class FfmpegProfileRecorder(ProfileRecorder):
    _recording_threads: list[threading.Thread] = []
    def __init__(self, 
                 logger: LoggerInterface,
                 time_provider: TimeProviderInterface,
                 event_bus: PyventusBus):
        self.logger = logger
        self.time_provider = time_provider
        super().__init__(event_bus)
    
    def __get_video_file_path(self, profile: Profile, storage_path: ProfileVideoStoragePath):
        time_title = self.time_provider.now_local().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{storage_path.value}/{profile.video_prefix.value}_{time_title}.mkv"
    
    def _get_ffmpeg_output(self, profile: Profile, storage_path: ProfileVideoStoragePath):
        duration_seconds = profile.recording_seconds.value
        rtsp_timeout_microseconds = 30 * 1000000
        input = ffmpeg.input(profile.uri.value, 
                             rtsp_transport="tcp",
                             timeout=rtsp_timeout_microseconds
                             )
        output_path = self.__get_video_file_path(profile, storage_path)
        output = ffmpeg.output(
            input.video,
            output_path,
            vcodec="copy",
            loglevel="error",
            t=duration_seconds
        )
        return output, output_path
    
    def _record_async(self, 
                      profile: Profile, 
                      storage_path: ProfileVideoStoragePath, 
                      on_recording_finished: Callable[[Profile, str], None]) -> None:
        output, output_path = self._get_ffmpeg_output(profile, storage_path)
        self.logger.debug(f"Recording profile with ffmpeg: {profile.id.value}")

        def record():
            loop = asyncio.new_event_loop()
            self.logger.debug(f"Spawning thread {threading.current_thread().name}")
            try:
                ffmpeg.run(output)
            except ffmpeg.Error as e:
                self.logger.error(f"FFmpeg error recording profile {profile.id.value}: {e}")
                # TODO: notify
            except Exception as e:
                self.logger.error(f"Unexpected error recording profile {profile.id.value}: {e}")
                # TODO: notify
            finally:
                self.logger.debug(f"Finished recording profile with ffmpeg: {profile.id.value}")
                #asyncio.run_coroutine_threadsafe(recording_finished_strategy.execute(profile), loop)
                on_recording_finished(profile, output_path)
                loop.close()
                
        thread = threading.Thread(target=record)
        thread.start()
        
        self._recording_threads.append(thread)
    
    def wait_recordings_to_finish(self) -> None:
        """
        Espera a que todas las grabaciones en curso terminen.
        Este método bloquea hasta que todos los hilos de grabación hayan completado.
        """
        self.logger.debug(f"Esperando que {len(self._recording_threads)} grabaciones terminen...")
        
        for thread in self._recording_threads:
            thread.join()
        
        self.logger.debug("Todas las grabaciones han terminado")
        # Limpiar la lista de hilos ya que todos han terminado
        self._recording_threads.clear()