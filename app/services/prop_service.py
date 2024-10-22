import httpx
from bs4 import BeautifulSoup
from loguru import logger
from app.config import settings
from app.schemas import PropertyManager, Property


class PropService:
    property_manager = PropertyManager()

    def get_properties(self) -> list[Property]:
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
                soup = BeautifulSoup(page_content, "html.parser")
                logger.info(f"Page {page} processed successfully.")
                properties = soup.find_all("div", class_="card-remax__header-body")
                self.structure_property(properties)
                page += 1

            except httpx.HTTPStatusError as http_err:
                logger.error(f"HTTP error occurred: {http_err}")
                break
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                break

        return self.property_manager.get_properties()

    def structure_property(self, properties: list[any]):
        for prop in properties:
            self.property_manager.add_property(
                property_data={
                    "price_usd": float(
                        prop.find("span", class_="price")
                        .text.replace("$", "")
                        .replace(",", "")
                        .strip()
                    ),
                    "expenses_ars": float(
                        prop.find("span", class_="expenses")
                        .text.replace("$", "")
                        .replace(",", "")
                        .strip()
                    ),
                    "address": prop.find("span", class_="address").text.strip(),
                    "total_area_m2": float(
                        prop.find("span", class_="total-area")
                        .text.replace("m²", "")
                        .strip()
                    ),
                    "covered_area_m2": float(
                        prop.find("span", class_="covered-area")
                        .text.replace("m²", "")
                        .strip()
                    ),
                    "rooms": int(prop.find("span", class_="rooms").text.strip()),
                    "bathrooms": int(
                        prop.find("span", class_="bathrooms").text.strip()
                    ),
                    "description": prop.find("p", class_="description").text.strip(),
                    "broker_name": prop.find("span", class_="broker-name").text.strip(),
                    "broker_license": prop.find(
                        "span", class_="broker-license"
                    ).text.strip(),
                    "contact_phone": prop.find(
                        "span", class_="contact-phone"
                    ).text.strip(),
                    "contact_office": prop.find(
                        "span", class_="contact-office"
                    ).text.strip(),
                }
            )


property_service = PropService()
