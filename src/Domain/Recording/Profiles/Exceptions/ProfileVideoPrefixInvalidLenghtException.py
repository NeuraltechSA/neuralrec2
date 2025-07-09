class ProfileVideoPrefixInvalidLenghtException(Exception):
    def __init__(self, current_length: int, min_length: int, max_length: int ):
        super().__init__(f"Profile file prefix must be between {min_length} and {max_length} characters, current length: {current_length}")