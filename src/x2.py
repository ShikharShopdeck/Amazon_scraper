from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def extract_product_details(url):
    # Set up Firefox options
    # Uncomment below line if you want to run in headless mode
    # firefox_options.add_argument('--headless')
    
    # Initialize the Firefox driver
    driver = webdriver.Firefox()

    driver.get(url)
        
        # Wait for the product details section to load
    wait = WebDriverWait(driver, 10)    
    details = {}
    # try:
    #     details_wrapper = driver.find_element(By.ID, "detailBulletsWrapper_feature_div")
    #     detail_rows = details_wrapper.find_elements(By.XPATH, ".//ul/li")
            
    #     for row in detail_rows:
    #         try:
    #             key_element = row.find_element(By.XPATH, ".//span[@class='a-text-bold']")
    #             key = key_element.text.strip().replace(":", "")
    #             value = key_element.find_element(
    #                 By.XPATH, 
    #             "./following-sibling::span"
    #             ).text.strip()
    #             details[key] = value
    #         except Exception:
    #             continue
                    
    # except Exception as e:

    #     try:
    #         rows = driver.find_elements(By.CSS_SELECTOR, "#productDetails_detailBullets_sections1 tr")
    #         # Extract data from each row
    #         for row in rows:
    #             try:
    #                 header = row.find_element(By.TAG_NAME, "th").text.strip()
    #                 value = row.find_element(By.TAG_NAME, "td").text.strip()
    #                 details[header] = value
    #             except:
    #                 continue

    #     except Exception as e:
    #         print(f"An error occurred in second method: {str(e)}")
    #         return None
            
    #     return details
        
    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")
    #     return None
        


def main():
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