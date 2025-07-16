import argparse
from CLIApp import CLIApp
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("--recording-loop")
parser.add_argument("--move-local-stored-files-to-remote")
args = parser.parse_args()

app = CLIApp()

if __name__ == "__main__":
    if args.recording_loop:
        asyncio.run(app.run_recording_loop())
    elif args.move_local_stored_files_to_remote:
        asyncio.run(app.run_move_local_stored_files_to_remote())