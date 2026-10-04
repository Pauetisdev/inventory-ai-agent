from pydantic import BaseModel, Field
from enum import Enum

class CategoryEnum(str, Enum):
    T_SHIRT = "T-Shirt"
    TROUSERS = "Trousers"
    COAT = "Coat"
    SHOES = "Shoes"
    ACCESSORY = "Accessory"

class ConditionEnum(str, Enum):
    EXCELLENT = "Excellent"
    VERY_GOOD = "Very Good"
    GOOD = "Good"
    FAIR = "Fair"


class ClothingItem(BaseModel):
    category: CategoryEnum
    bradn: str
    size:str
    condition: ConditionEnum
    price: float

class ClothingItemCreate(ClothingItem):
    pass

class ClothingItemResponse(ClothingItem):
    id: str = Field(alias="_id")