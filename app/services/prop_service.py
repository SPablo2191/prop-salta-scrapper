from bs4 import BeautifulSoup
import httpx
from loguru import logger
import pandas as pd
from app.config import settings
from app.schemas import PropertyManager, Property


class PropService:
    property_manager = PropertyManager()

    async def get_properties(self) -> list[Property]:
        self.property_manager.clear_list()
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

        async with httpx.AsyncClient() as client:
            while True:
                params["page"] = page
                try:
                    response = await client.get(website_url, params=params)
                    response.raise_for_status()
                    page_content = response.text

                    if (
                        "No hay propiedades que coincidan con tu búsqueda"
                        in page_content
                    ):
                        logger.info(
                            f"No more properties found on page {page}. Stopping."
                        )
                        break

                    soup = BeautifulSoup(page_content, "html.parser")
                    logger.info(f"Page {page} processed successfully.")
                    properties = soup.findAll("div", class_="card-remax viewList")
                    logger.info(len(properties))
                    self.scrape_property(properties)
                    page += 1

                except httpx.HTTPStatusError as http_err:
                    logger.error(f"HTTP error occurred: {http_err}")
                    break
                except Exception as e:
                    logger.error(f"An error occurred: {e}")
                    break

        return self.property_manager.get_properties()

    def set_data_csv(self, dataRows: list[dict]):
        df = pd.DataFrame(dataRows)
        df.to_csv("properties.csv", index=False)

    def scrape_property(self, properties: list[any]):
        dataRows = []
        for prop in properties:

            def safe_select(selector):
                element = prop.select_one(selector)
                return element.text.strip() if element else "N/A"

            price_usd = (
                safe_select(".card__price").replace(".", "").replace(" USD", "").strip()
            )
            expenses_ars = (
                safe_select(".card__expenses")
                .replace("+ ", "")
                .replace(".", "")
                .replace(" ARS expensas", "")
                .strip()
            )
            address = safe_select(".card__address")
            total_area_m2 = safe_select(".feature--m2total span")
            covered_area_m2 = safe_select(".feature--m2cover span")
            rooms = safe_select(".feature--ambientes span")
            bathrooms = safe_select(".feature--bathroom span")
            description = safe_select(".card__description")
            property_data = {
                "price_usd": price_usd,
                "expenses_ars": expenses_ars,
                "address": address,
                "total_area_m2": total_area_m2,
                "covered_area_m2": covered_area_m2,
                "rooms": rooms,
                "bathrooms": bathrooms,
                "description": description,
            }
            dataRows.append(property_data)
            self.property_manager.add_property(property_data=property_data)
        self.set_data_csv(dataRows=dataRows)


property_service = PropService()
