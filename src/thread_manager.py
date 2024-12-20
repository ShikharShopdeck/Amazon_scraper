import threading
from queue import Queue
from typing import List
from time import sleep
from .scraper import AmazonScraper
from .database import MongoDBHandler
from .config import logger

class ScraperThread(threading.Thread):
    def __init__(self, 
                 thread_id: int,
                 url_queue: Queue,
                 base_url: str,
                 db_handler: MongoDBHandler,
                 collection_name: str):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url_queue = url_queue
        self.base_url = base_url
        self.db_handler = db_handler
        self.collection_name = collection_name
        self.scraper = None

    def run(self):
        logger.info(f"Starting thread {self.thread_id}")
        self.scraper = AmazonScraper(self.base_url)
        
        try:
            while True:
                try:
                    # Get URL and page number from queue with timeout
                    url, page = self.url_queue.get(timeout=5)
                except Queue.Empty:
                    break
                
                try:
                    logger.info(f"Thread {self.thread_id} processing: {url}")
                    product = self.scraper.get_product_details(url, page)
                    self.db_handler.store_product(product, self.collection_name)
                    sleep(2)  # Prevent overwhelming the server
                except Exception as e:
                    logger.error(f"Error in thread {self.thread_id}: {e}")
                finally:
                    self.url_queue.task_done()
                    
        except Exception as e:
            logger.error(f"Thread {self.thread_id} encountered error: {e}")
        finally:
            if self.scraper:
                self.scraper.cleanup()
            logger.info(f"Thread {self.thread_id} finished")

class ThreadManager:
    def __init__(self, 
                 num_threads: int,
                 base_url: str,
                 db_handler: MongoDBHandler,
                 collection_name: str):
        self.num_threads = num_threads
        self.base_url = base_url
        self.db_handler = db_handler
        self.collection_name = collection_name
        self.url_queue = Queue()
        self.threads: List[ScraperThread] = []

    def start_threads(self):
        """Initialize and start scraper threads"""
        for i in range(self.num_threads):
            thread = ScraperThread(
                i,
                self.url_queue,
                self.base_url,
                self.db_handler,
                self.collection_name
            )
            self.threads.append(thread)
            thread.start()

    def add_urls(self, urls: List[str], page: int):
        """Add URLs to the processing queue"""
        for url in urls:
            self.url_queue.put((url, page))

    def wait_completion(self):
        """Wait for all threads to complete"""
        self.url_queue.join()
        for thread in self.threads:
            thread.join()