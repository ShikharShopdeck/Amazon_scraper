import logging

# URL Configuration
BASE_URL = "https://www.amazon.in/s?k=tshirt+for+man&crid=2R7R4H8TMQ4AZ&qid=1734267058&sprefix=tshir,aps,231"

# MongoDB Configuration
MONGODB_CONNECTION = "mongodb://localhost:27017/"
DB_NAME = "ProductDatabase"
COLLECTION_NAME = "ProductDetails"

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)