import time
from pymongo import MongoClient
from .models import ProductDetails
from .config import logger

class MongoDBHandler:
   
    def __init__(self, connection_string: str, db_name: str , collection_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.create_unique_index_on_asin(collection_name)
    
    def store_product(self, product: ProductDetails, collection_name: str) -> None:
        collection = self.db[collection_name]
        timeStamp = int(time.time())

        asin = product.additional_details.get("ASIN ", "") or product.additional_details.get("ASIN", "")

        existing_product = collection.find_one({"_id": asin})
        if existing_product or not asin:
            logger.info(f"product with asin {asin} already exists in the database or has empty asin, skipping.")
            return
        product_dict = {
            "_id" : asin,
            "Selling Price": product.selling_price,
            "MRP": product.mrp,
            "Rating":product.rating,
            "TotalBought":product.totalBought,
            "Page": product.page,
            "TotalRating": product.totalRating,
            "URL": product.url,
            "timestamp": timeStamp,
            **product.additional_details,
            **product.product_attributes,
        }
        result = collection.insert_one(product_dict)
        logger.info(f"Inserted document ID: {result.inserted_id}")
    
    def create_unique_index_on_asin(self, collection_name: str) -> None:
        """Create a unique index on the ASIN field of a collection"""
        collection = self.db[collection_name]
        collection.create_index("ASIN ", unique=True)
