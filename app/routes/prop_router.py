from fastapi import APIRouter, HTTPException
from app.schemas import Property
from app.services import property_service

router = APIRouter(prefix="/property", tags=["Property"])


@router.get("/")
def get_properties() -> list[Property]:
    try:
        return property_service.get_properties()
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
