from typing import List
from pydantic import BaseModel, Field


class Property(BaseModel):
    price_usd: str = Field(..., description="Price of the property in USD")
    expenses_ars: str = Field(..., description="Expenses in ARS")
    address: str = Field(..., description="Property address")
    total_area_m2: str = Field(..., description="Total area in square meters")
    covered_area_m2: str = Field(..., description="Covered area in square meters")
    rooms: int = Field(..., description="Number of rooms")
    bathrooms: int = Field(..., description="Number of bathrooms")
    description: str = Field(..., description="Short description of the property")


class PropertyManager:
    def __init__(self):
        self.properties: List[Property] = []

    def add_property(self, property_data: dict):
        """Adds a property to the list"""
        property_obj = Property(**property_data)
        self.properties.append(property_obj)

    def get_properties(self) -> List[Property]:
        """Returns the list of properties"""
        return self.properties

    def clear_list(self) -> None:
        self.properties.clear()
