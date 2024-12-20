from dataclasses import dataclass
from typing import Dict

@dataclass
class ProductDetails:
    selling_price: str
    mrp: str
    page: int
    additional_details: Dict[str, str]
    rating: str
    totalBought: str
    totalRating: str
    url: str