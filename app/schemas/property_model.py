from typing import List
from pydantic import BaseModel, Field


class Property(BaseModel):
    price_usd: float = Field(..., description="Price of the property in USD")
    expenses_ars: float = Field(..., description="Expenses in ARS")
    address: str = Field(..., description="Property address")
    total_area_m2: float = Field(..., description="Total area in square meters")
    covered_area_m2: float = Field(..., description="Covered area in square meters")
    rooms: int = Field(..., description="Number of rooms")
    bathrooms: int = Field(..., description="Number of bathrooms")
    description: str = Field(..., description="Short description of the property")
    broker_name: str = Field(..., description="Name of the responsible broker")
    broker_license: str = Field(..., description="License of the broker")
    contact_phone: str = Field(..., description="Contact phone number")
    contact_office: str = Field(..., description="Office contact information")


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
