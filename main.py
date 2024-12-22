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
from selenium import webdriver

import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor


def process_product_links(scraper, db_handler, page, product_links):
    # Divide all product links into num_threads lists
    num_threads = 5
    batch_size = len(product_links) // num_threads
    batches = [product_links[i:i + batch_size] for i in range(0, len(product_links), batch_size)]


    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_links, scraper, db_handler, page, batch) for batch in batches]
        for future in futures:
            future.result()




def main():
    scraper = AmazonScraper(BASE_URL)
    db_handler = MongoDBHandler(MONGODB_CONNECTION, DB_NAME, COLLECTION_NAME)
    page = 1
    try:
        scraper.open_first_page_links()
        while scraper.check_next_page_button():

            product_links = scraper.get_product_links()
            print(scraper.driver.current_url)
            process_product_links(scraper, db_handler, page, product_links)
            scraper.click_next_page_button()
            page += 1

    finally:
        print("Done Scraping")
        scraper.driver.quit()
        

def process_links(scraper, db_handler, page, links):
    # create a new driver
    driver = webdriver.Firefox()
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    for link in links:
        process_link(scraper, db_handler, page, link,driver)

    driver.quit()

def process_link(scraper, db_handler, page, link,driver):
    try:
        logger.info(f"Scraping product details from {link}...")
        product = scraper.get_product_details(link, page, driver)
        db_handler.store_product(product, COLLECTION_NAME)
    except Exception as e:
        # product = extract_product_details_two(link)
        # db_handler.store_
        logger.error(f"Error scraping {link}: {e}")

if __name__ == "__main__":
    main()