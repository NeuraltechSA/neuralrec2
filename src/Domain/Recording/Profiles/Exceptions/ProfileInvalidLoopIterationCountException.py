class ProfileInvalidLoopIterationCountException(Exception):
    def __init__(self, iterations_number: int):
        super().__init__(f"Invalid loop iteration count: {iterations_number}")