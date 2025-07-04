class ProfileOutOfRangeException(Exception):
    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        super().__init__(f"El perfil {profile_id} no está en el rango de tiempo permitido")