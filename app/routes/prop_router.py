from fastapi import APIRouter, HTTPException
from app.schemas import Property
from app.services import property_service
from loguru import logger

router = APIRouter(prefix="/property", tags=["Property"])


@router.get("/")
async def get_properties() -> list[Property]:
    try:
        return await property_service.get_properties()
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


async def set_properties():
    try:
        await property_service.get_properties()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e)
