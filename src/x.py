from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_product_details(url):
    """Extract product details from Amazon product page"""
    # Set up Firefox options
    firefox_options = Options()
    # Uncomment below line if you want to run in headless mode
    # firefox_options.add_argument('--headless')
    
    # Initialize the Firefox driver
    driver = webdriver.Firefox(options=firefox_options)
    
    try:
        # Navigate to the URL
        logger.info(f"Navigating to {url}")
        driver.get(url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Dictionary to store the extracted data
        product_data = {}
        
        # Try first method - detailBulletsWrapper
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
                    product_data[key] = value
                except Exception:
                    continue
                    
        except Exception as e:
            logger.warning(f"First method failed: {e}")
            
            # Try second method - productDetails table
            try:
                wait.until(EC.presence_of_element_located((By.ID, "productDetails_db_sections")))
                rows = driver.find_elements(By.CSS_SELECTOR, "#productDetails_detailBullets_sections1 tr")
                
                for row in rows:
                    try:
                        header = row.find_element(By.TAG_NAME, "th").text.strip()
                        value = row.find_element(By.TAG_NAME, "td").text.strip()
                        product_data[header] = value
                    except Exception:
                        continue
                        
            except Exception as e:
                logger.error(f"Second method failed: {e}")
                return None
        
        if product_data:
            logger.info("Successfully extracted product details")
            return product_data
        else:
            logger.warning("No product details found")
            return None
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None
        
    finally:
        # Close the browser
        driver.quit()
        logger.info("Browser closed")

def main():
    """Main function to run the scraper"""
    # Get URL from user
    url = input("Please enter the Amazon product URL: ")
    
    # Extract the details
    product_details = extract_product_details(url)
    
    # Print the results
    if product_details:
        print("\nProduct Details:")
        for key, value in product_details.items():
            print(f"{key}: {value}")
    else:
        print("Failed to extract product details.")

if __name__ == "__main__":
    main()