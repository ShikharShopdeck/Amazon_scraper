from dataclasses import dataclass
import time
from typing import Dict

@dataclass
class ProductDetails:
    selling_price: str
    mrp: str
    page: int
    additional_details: Dict[str, str]
    product_attributes: Dict[str, str]
    rating: str
    totalBought: str
    totalRating: str
    url: str
    timeStamp: int = int(time.time())