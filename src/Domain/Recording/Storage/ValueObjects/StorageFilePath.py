from src.Domain.SharedKernel.ValueObjects.RequiredStringValueObject import RequiredStringValueObject

class StorageFilePath(RequiredStringValueObject):
    def __init__(self, value: str):
        super().__init__(value)
        
    def __str__(self):
        return self.value
    
    def get_name(self) -> str:
        return self.value.split("/")[-1]
    
    def get_relative_path(self, base_path: str) -> str:
        return self.value.replace(base_path, "")

    
    # TODO: ensure valid path