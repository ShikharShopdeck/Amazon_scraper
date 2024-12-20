from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
from .models import ProductDetails
from .config import logger

class AmazonScraper:
    def __init__(self, base_url: str, driver: webdriver.Chrome = None):
        self.base_url = base_url
        self.driver = driver or webdriver.Chrome()
        self._setup_tabs()
    
    def _setup_tabs(self) -> None:
        """Initialize two tabs for scraping"""
        if len(self.driver.window_handles) < 2:
            self.driver.execute_script("window.open('');")
    
    def _switch_to_tab(self, tab_index: int) -> None:
        """Switch to specified browser tab"""
        self.driver.switch_to.window(self.driver.window_handles[tab_index])
    
    def get_product_links(self, page: int) -> List[str]:
        """Extract product links from a page"""
        url = f"{self.base_url}&page={page}"
        print("scrapint url", url)
        self._switch_to_tab(0)
        self.driver.get(url)
        
        try:
            elements = self.driver.find_elements(
                By.XPATH, 
                "//a[@class='a-link-normal s-no-outline']"
            )
            return [elem.get_attribute('href') for elem in elements if elem.get_attribute('href')]
        except Exception as e:
            logger.error(f"Error getting links from page: {e}")
            return []

    def _extract_price_info(self) -> tuple[str, str]:
        """Extract selling price and MRP"""
        selling_price = "Price not found"
        mrp = "MRP not found"
        
        try:
            price_whole = self.driver.find_element(By.CLASS_NAME, "a-price-whole").text.strip()
            price_fraction = self.driver.find_element(By.CLASS_NAME, "a-price-fraction").text.strip()
            selling_price = f"{price_whole}.{price_fraction}"
            
        except Exception as e:
            logger.error(f"Error extracting price information: {e}")
        
        try:
            mrp_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'a-price a-text-price')]")
            mrp = mrp_element.text
        except Exception as e:
            mrp = "MRP not found"
            
        return selling_price, mrp
    
    def extract_rating(self) -> str:
        rating = "Rating not Found"

        # Rating
        try:
            rating_element = self.driver.find_element(By.XPATH, "//span[@id='acrPopover']//span[@class='a-size-base a-color-base']")
            rating = rating_element.text.strip()
            rating = rating
        except Exception as e:
            rating = "Rating not found"

        return rating
    
    def getTotalRating(self) ->str:
        totalRating = ""

        try:
            totalRating_element = self.driver.find_element(By.XPATH, "//span[@id='acrCustomerReviewText']")
            totalRating = totalRating_element.text.strip()
        except Exception as e:
            totalRating = ""

        return totalRating
    
    def total_number_of_bought(self) ->str:
        # Extract the number of people bought in the last month
        totalBought = "Data not available"

        try:
            bought_element = self.driver.find_element(By.XPATH, "//span[@id='social-proofing-faceout-title-tk_bought']")
            bought_text = bought_element.text.strip()
            totalBought = bought_text.split()[0]
        except Exception:
            totalBought = "Data not available"
        
        return totalBought


    def _extract_product_details(self) -> dict:
        """Extract product details from the details section"""
        details = {}
        try:
            details_wrapper = self.driver.find_element(By.ID, "detailBulletsWrapper_feature_div")
            detail_rows = details_wrapper.find_elements(By.XPATH, ".//ul/li")
            
            for row in detail_rows:
                try:
                    key_element = row.find_element(By.XPATH, ".//span[@class='a-text-bold']")
                    key = key_element.text.strip().replace(":", "")
                    value = key_element.find_element(
                        By.XPATH, 
                        "./following-sibling::span"
                    ).text.strip()
                    details[key] = value
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Error extracting product details: {e}")
            
        return details

    def get_product_details(self, url: str, page: int) -> ProductDetails:
        """Get complete product details"""
        self._switch_to_tab(1)
        self.driver.get(url)
        
        selling_price, mrp = self._extract_price_info()
        additional_details = self._extract_product_details()
        rating = self.extract_rating()
        totalBought = self.total_number_of_bought()
        totalRating = self.getTotalRating()
        
        return ProductDetails(
            selling_price=selling_price,
            mrp=mrp,
            page=page,
            additional_details=additional_details,
            rating=rating,
            totalRating=totalRating,
            totalBought=totalBought,
            url=url
        )