import logging

# URL Configuration
BASE_URL = "https://www.amazon.in/s?i=apparel&rh=n%3A1968254031&s=popularity-rank&fs=true"
# MongoDB Configuration
MONGODB_CONNECTION = "mongodb://stage_dev:SOh3TbYhx8ypJPxmt@34.93.48.32:27017/"
DB_NAME = "scraping_data"
COLLECTION_NAME = "amazon_products"

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)