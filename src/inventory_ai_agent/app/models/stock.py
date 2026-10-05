from pydantic import BaseModel, Field
from enum import Enum

class CategoryEnum(str, Enum):
    SABATES = "Sabates"
    SAMARRETA = "Samarreta"
    SUDADERA = "Sudadera"
    PANTALONS = "Pantalons"
    JAQUETA = "Jaqueta"
    ACCESSORI = "Accessori"

class ConditionEnum(str, Enum):
    NOU = "Nou"
    MOLT_BO = "Molt bo"
    BO = "Bo"
    ACCEPTABLE = "Acceptable"


class ClothingItem(BaseModel):
    name: str = Field(..., description="Specific name of the item")
    category: CategoryEnum
    brand: str
    size:str
    condition: ConditionEnum
    price: float