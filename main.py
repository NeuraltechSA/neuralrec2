from src.Application.Recording.Profiles.UseCases.RunLoopUseCase import RunLoopUseCase
from src.Infraestructure.Recording.Profiles.FfmpegProfileRecorder import FfmpegProfileRecorder
from src.Infraestructure.Recording.Profiles.SqliteProfileRepository import SqliteProfileRepository
from src.Application.Recording.Profiles.UseCases.StartRecordingUseCase import StartRecordingUseCase
from src.Infraestructure.SharedKernel.TimeProvider import TimeProvider

profile_repository = SqliteProfileRepository("profiles.db")
profile_recorder = FfmpegProfileRecorder("ffmpeg")
start_recording = StartRecordingUseCase(profile_repository, profile_recorder)

run_loop_use_case = RunLoopUseCase(TimeProvider(), start_recording)
run_loop_use_case.execute(1)