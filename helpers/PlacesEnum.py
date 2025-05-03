from enum import Enum

class PlacesEnum(Enum):
    """
    Enum class for different types of places.
    """
    MOUNTAIN = "mountain"
    BEACH = "beach"
    BIG_CITY = "big_city"
    VILLAGE = "village"

    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def get_members(cls) -> list[str]:
        """
        Get all members of the enum class.
        """
        return [member.value for member in cls]