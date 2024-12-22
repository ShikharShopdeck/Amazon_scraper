from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from typing import List
from .models import ProductDetails
from .config import logger
from pyvirtualdisplay import Display

class AmazonScraper:
    def __init__(self, base_url: str, driver: webdriver.Chrome = None):
        self.base_url = base_url
        self.display = Display(visible=False, size=(1024, 768))
        self.display.start()
        self.driver = driver or webdriver.Firefox()
        self._setup_tabs()
    
    def _setup_tabs(self) -> None:
        """Initialize two tabs for scraping"""
        if len(self.driver.window_handles) < 2:
            self.driver.execute_script("window.open('');")
    
    def _switch_to_tab(self, tab_index: int) -> None:
        """Switch to specified browser tab"""
        self.driver.switch_to.window(self.driver.window_handles[tab_index])
    def open_first_page_links(self) -> None:
        self._switch_to_tab(0)
        self.driver.get(self.base_url)

    def get_product_links(self) -> List[str]:
        
        try:
            elements = self.driver.find_elements(
                By.XPATH, 
                "//a[@class='a-link-normal s-no-outline']"
            )
            return  [elem.get_attribute('href') for elem in elements if elem.get_attribute('href')]
        except Exception as e:
            logger.error(f"Error getting links from page: {e}")
            return []

    def check_next_page_button(self):
        """
        Checks if the 'Next Page' button exists on the current page and is not disabled.

        Args:
            driver (webdriver): The Selenium WebDriver instance.

        Returns:
            bool: True if the 'Next Page' button exists and is not disabled, False otherwise.
        """
        try:
            # Locate the Next Page button by its class name
            next_page_button = self.driver.find_element(By.CLASS_NAME, "s-pagination-next")

            # Check if the button has the 's-pagination-disabled' class
            if "s-pagination-disabled" in next_page_button.get_attribute("class"):
                return False
            return True
        except NoSuchElementException:
            return False

    def click_next_page_button(self):
        """
        Clicks the 'Next Page' button if it exists and is not disabled.

        Args:
            driver (webdriver): The Selenium WebDriver instance.

        Returns:
            bool: True if the button was clicked, False otherwise.
        """
        try:
            # Locate and click the Next Page button by its class name
            next_page_button = self.driver.find_element(By.CLASS_NAME, "s-pagination-next")
            next_page_button.click()
            sleep(2)
            return True
        except NoSuchElementException:
            return False
    def _extract_price_info(self,driver) -> tuple[str, str]:
        """Extract selling price and MRP"""
        selling_price = "Price not found"
        mrp = "MRP not found"
        
        try:
            price_whole = driver.find_element(By.CLASS_NAME, "a-price-whole").text.strip()
            price_fraction = driver.find_element(By.CLASS_NAME, "a-price-fraction").text.strip()
            selling_price = f"{price_whole}.{price_fraction}"
            
        except Exception as e:
            logger.error(f"Error extracting price information: {e}")
        
        try:
            mrp_element = driver.find_element(By.XPATH, "//span[contains(@class, 'a-price a-text-price')]")
            mrp = mrp_element.text
        except Exception as e:
            mrp = "MRP not found"
            
        return selling_price, mrp
    
    def extract_rating(self,driver) -> str:
        rating = "Rating not Found"

        # Rating
        try:
            rating_element = driver.find_element(By.XPATH, "//span[@id='acrPopover']//span[@class='a-size-base a-color-base']")
            rating = rating_element.text.strip()
            rating = rating
        except Exception as e:
            rating = "Rating not found"

        return rating
    
    def getTotalRating(self,driver) ->str:
        totalRating = ""

        try:
            totalRating_element = driver.find_element(By.XPATH, "//span[@id='acrCustomerReviewText']")
            totalRating = totalRating_element.text.strip()
        except Exception as e:
            totalRating = ""

        return totalRating
    
    def total_number_of_bought(self,driver) ->str:
        # Extract the number of people bought in the last month
        totalBought = "Data not available"

        try:
            bought_element = driver.find_element(By.XPATH, "//span[@id='social-proofing-faceout-title-tk_bought']")
            bought_text = bought_element.text.strip()
            totalBought = bought_text.split()[0]
        except Exception:
            totalBought = "Data not available"
        
        return totalBought
    


    def extract_product_Attributes(self) -> dict:
        details = {}
        try:
            # Locate the main div containing product details
            # product_details_section = self.driver.find_element(By.ID, "productFactsDesktopExpander")
            
            # Extract all rows under "Product details"
            product_facts = self.driver.find_elements(By.XPATH, ".//div[contains(@class, 'product-facts-detail')]")
            for fact in product_facts:
                try:
                    key_element = fact.find_element(By.XPATH, ".//div[contains(@class, 'a-col-left')]//span[@class='a-color-base']")
                    value_element = fact.find_element(By.XPATH, ".//div[contains(@class, 'a-col-right')]//span[@class='a-color-base']")
                    key = key_element.text.strip()
                    value = value_element.text.strip()
                    details[key] = value
                except Exception as e:
                    logger.error(f"Error extracting fact: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error extracting product details: {e}")

        return details



    def _extract_product_details(self,driver) -> dict:
        """Extract product details from the details section"""

        sleep(5)
        details = {}
        try:
            details_wrapper = driver.find_element(By.ID, "detailBulletsWrapper_feature_div")
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

            try:
                rows = driver.find_elements(By.CSS_SELECTOR, "#productDetails_detailBullets_sections1 tr")
                # Extract data from each row
                for row in rows:
                    try:
                        header = row.find_element(By.TAG_NAME, "th").text.strip()
                        value = row.find_element(By.TAG_NAME, "td").text.strip()
                        details[header] = value
                    except:
                        continue

            except Exception as e:
                print(f"An error occurred in second method: {str(e)}")
                return None
            
        return details
    def quit(self):
        self.driver.quit()
        self.display.quit()

    def get_product_details(self, url: str, page: int, driver: webdriver.Chrome) -> ProductDetails:
        """Get complete product details"""
        driver.get(url)
        
        selling_price, mrp = self._extract_price_info(driver)
        additional_details = self._extract_product_details(driver)
        product_attributes = self.extract_product_Attributes()
        rating = self.extract_rating(driver)
        totalBought = self.total_number_of_bought(driver)
        totalRating = self.getTotalRating(driver)
        
        return ProductDetails(
            selling_price=selling_price,
            mrp=mrp,
            page=page,
            additional_details=additional_details,
            product_attributes=product_attributes,
            rating=rating,
            totalRating=totalRating,
            totalBought=totalBought,
            url=url
        )