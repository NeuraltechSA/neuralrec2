from src.Infraestructure.Recording.Profiles.ProfileSleeper import ProfileSleeper
from src.Infraestructure.Recording.Storage.SqliteStorageRepository import SqliteStorageRepository
from src.Domain.Recording.Storage.Services.LocalStorageFinder import LocalStorageFinder
from src.Domain.Recording.Storage.Services.RemoteStorageFinder import RemoteStorageFinder
from src.Domain.Recording.Profiles.Services.RecordingService import RecordingService
from src.Application.Recording.Profiles.UseCases.RunLoopUseCase import RunLoopUseCase
from src.Infraestructure.Recording.Profiles.FfmpegProfileRecorder import FfmpegProfileRecorder
from src.Infraestructure.Recording.Profiles.SqliteProfileRepository import SqliteProfileRepository
from src.Infraestructure.SharedKernel.TimeProvider import TimeProvider

storage_repository = SqliteStorageRepository()
profile_repository = SqliteProfileRepository("profiles.db")
profile_recorder = FfmpegProfileRecorder("ffmpeg")
local_storage_finder = LocalStorageFinder(storage_repository)
remote_storage_finder = RemoteStorageFinder(storage_repository)
recording_service = RecordingService(profile_repository, profile_recorder, local_storage_finder, remote_storage_finder)

run_loop_use_case = RunLoopUseCase(TimeProvider(), recording_service, ProfileSleeper())
run_loop_use_case.execute(1)