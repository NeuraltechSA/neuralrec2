from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Profiles.Entities.Profile import Profile
import ffmpeg
from multiprocessing import Process

class FfmpegProfileRecorder(ProfileRecorderInterface):
    def __init__(self, ffmpeg_path: str):
        self.__ffmpeg_path = ffmpeg_path

    def record_async(self, profile: Profile, storage_path: ProfileVideoStoragePath):
        input = ffmpeg.input(profile.uri.value)
        output = ffmpeg.output(input.video, f"{storage_path.value}/output_{profile.id.value}.mp4")
        Process(target=ffmpeg.run, args=(output,)).start()
        '''
        out, err = ffmpeg.run(output)
        if err:
            raise Exception(f"Error recording profile: {err}")
        return out
        '''
    
    