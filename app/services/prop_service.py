import httpx
from loguru import logger
from app.config import settings


class PropService:
    def get_properties(self):
        website_url = settings.website_url
        params = {
            "page": 0,  # Este valor lo iremos incrementando
            "pageSize": 24,
            "sort": "-createdAt",
            "in:operationId": 1,
            "in:eStageId": "0,1,2,3,4",
            "in:typeId": "1,2,3,4,5,6,7,8",
            "locations": "in:SA@Salta::::::",
            "filterCount": 1,
            "viewMode": "listViewMode",
        }
        page = 0

        while True:
            params["page"] = page
            try:
                response = httpx.get(website_url, params=params)
                response.raise_for_status()
                page_content = response.text
                if "No hay propiedades que coincidan con tu búsqueda" in page_content:
                    logger.info(f"No more properties found on page {page}. Stopping.")
                    break
                logger.info(f"Page {page} processed successfully.")
                page += 1

            except httpx.HTTPStatusError as http_err:
                logger.error(f"HTTP error occurred: {http_err}")
                break
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                break

        return None


property_service = PropService()
