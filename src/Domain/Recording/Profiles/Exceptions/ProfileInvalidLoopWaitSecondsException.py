class ProfileInvalidLoopWaitSecondsException(Exception):
    def __init__(self, wait_seconds: int):
        self.wait_seconds = wait_seconds
        super().__init__(f"Invalid loop wait seconds: {wait_seconds}")