from src.Infraestructure.Recording.Profiles.ProfileDocument import ProfileDocument
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from beanie.operators import Inc, Set

import datetime
from src.Domain.Recording.Profiles.Entities.Profile import Profile

class BeanieProfileRepository(ProfileRepositoryInterface):
    async def find_ready_to_record(self, now: datetime.datetime) -> list[Profile]:
        profiles:list[ProfileDocument] = await ProfileDocument.find(ProfileDocument.is_recording == False).to_list()
        mapped_profiles = [p.map_to() for p in profiles]
        return [p for p in mapped_profiles if p.is_in_range(now)]
        

    async def find_one_by_id(self, id: str) -> Profile | None:
        profile = await ProfileDocument.find_one(ProfileDocument.id == id)
        if profile:
            return profile.map_to()
        return None
    
    async def save(self, profile: Profile) -> None:
        profile_document = ProfileDocument.map_from(profile)
        await profile_document.save()
    
    async def set_all_as_not_recording(self) -> None:
        # TODO: Fix typing error, update IS awaitable
        await ProfileDocument.find(ProfileDocument.is_recording == True).update({"$set": {ProfileDocument.is_recording: False}}) #type: ignore