import datetime
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Profiles.Entities.Profile import Profile
import ffmpeg
import datetime

class FfmpegProfileRecorder(ProfileRecorderInterface):

    def record(self, profile: Profile, storage_path: ProfileVideoStoragePath):
        duration_seconds = profile.recording_minutes.value * 60
        time_title = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        input = ffmpeg.input(profile.uri.value, rtsp_transport="tcp")
        output = ffmpeg.output(
            input.video,
            f"{storage_path.value}/output_{profile.id.value}_{time_title}.mp4",
            vcodec="copy",
            loglevel="error",
            t=duration_seconds
        )
        ffmpeg.run(output)
        '''
        out, err = ffmpeg.run(output)
        if err:
            raise Exception(f"Error recording profile: {err}")
        return out
        '''
    
    