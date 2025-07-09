import datetime
import threading
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Services.RecordingFinishedStrategy import ProfileRecordingFinishedStrategy
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.Recording.Profiles.Contracts.ProfileRecorder import ProfileRecorder
from src.Domain.Recording.Profiles.Entities.Profile import Profile
import ffmpeg
import datetime
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
import asyncio

class FfmpegProfileRecorder(ProfileRecorder):
    def __init__(self, 
                 logger: LoggerInterface,
                 time_provider: TimeProviderInterface):
        self.logger = logger
        self.time_provider = time_provider
    
    def _get_ffmpeg_output(self, profile: Profile, storage_path: ProfileVideoStoragePath):
        duration_seconds = profile.recording_minutes.value * 60
        time_title = self.time_provider.now_local().strftime("%Y-%m-%d_%H-%M-%S")
        input = ffmpeg.input(profile.uri.value, rtsp_transport="tcp")
        output = ffmpeg.output(
            input.video,
            f"{storage_path.value}/{profile.video_prefix.value}_{time_title}.mp4",
            vcodec="copy",
            loglevel="error",
            t=duration_seconds
        )
        return output
    
    def _record_async(self, 
                      profile: Profile, 
                      storage_path: ProfileVideoStoragePath, 
                      recording_finished_strategy: ProfileRecordingFinishedStrategy) -> None:
        output = self._get_ffmpeg_output(profile, storage_path)
        self.logger.debug(f"Recording profile with ffmpeg: {profile.id.value}")
        event_loop = asyncio.get_event_loop()
        def record():
            self.logger.debug(f"Spawning thread {threading.current_thread().name}")
            try:
                ffmpeg.run(output)
            except ffmpeg.Error as e:
                self.logger.error(f"FFmpeg error recording profile {profile.id.value}: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error recording profile {profile.id.value}: {e}")
            finally:
                self.logger.debug(f"Finished recording profile with ffmpeg: {profile.id.value}")
                asyncio.run_coroutine_threadsafe(recording_finished_strategy.execute(profile), event_loop)                
        threading.Thread(target=record).start()