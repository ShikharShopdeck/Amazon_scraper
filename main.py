from time import sleep
from src.scraper import AmazonScraper
from src.database import MongoDBHandler
from src.config import (
    BASE_URL, 
    MONGODB_CONNECTION, 
    DB_NAME, 
    COLLECTION_NAME,
    logger
)

def main():
    scraper = AmazonScraper(BASE_URL)
    db_handler = MongoDBHandler(MONGODB_CONNECTION, DB_NAME , COLLECTION_NAME)

    try:
        for page in range(1, 2):
            logger.info(f"Scraping page {page}...")
            product_links = scraper.get_product_links(page)
            
            for link in product_links:
                logger.info(f"Scraping product details from {link}...")
                product = scraper.get_product_details(link, page)
                db_handler.store_product(product, COLLECTION_NAME)
                sleep(2)
                
    finally:
        scraper.driver.quit()

if __name__ == "__main__":
    main()