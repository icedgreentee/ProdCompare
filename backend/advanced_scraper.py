"""
Advanced scraping utilities with Selenium support
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time
import random

class AdvancedScraper:
    def __init__(self, use_selenium=False):
        self.use_selenium = use_selenium
        self.driver = None
        self.ua = UserAgent()
        
    def setup_selenium_driver(self):
        """Setup Chrome driver with stealth options"""
        if self.driver:
            return self.driver
            
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return self.driver
        except Exception as e:
            print(f"Failed to setup Selenium driver: {e}")
            return None
    
    def scrape_with_selenium(self, url, selectors, max_wait=10):
        """Scrape using Selenium for JavaScript-heavy sites"""
        try:
            if not self.driver:
                self.setup_selenium_driver()
            
            if not self.driver:
                return None
                
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            
            # Wait for page to load
            WebDriverWait(self.driver, max_wait).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll to load dynamic content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Find product elements
            products = []
            for selector in selectors.get('product_cards', []):
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements[:3]:  # Limit to 3 products
                            product_data = self.extract_product_data_selenium(element, selectors)
                            if product_data:
                                products.append(product_data)
                        break
                except Exception as e:
                    print(f"Error with selector {selector}: {e}")
                    continue
            
            return products[0] if products else None
            
        except Exception as e:
            print(f"Selenium scraping error: {e}")
            return None
    
    def extract_product_data_selenium(self, element, selectors):
        """Extract product data from Selenium element"""
        try:
            # Extract name
            name = None
            for selector in selectors.get('name', []):
                try:
                    name_elem = element.find_element(By.CSS_SELECTOR, selector)
                    name = name_elem.text.strip()
                    if name:
                        break
                except:
                    continue
            
            # Extract price
            price = None
            price_text = None
            for selector in selectors.get('price', []):
                try:
                    price_elem = element.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    if price_text:
                        # Extract numeric price
                        import re
                        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace(',', ''))
                        if price_match:
                            price = float(price_match.group())
                            break
                except:
                    continue
            
            # Extract image
            image = None
            for selector in selectors.get('image', []):
                try:
                    img_elem = element.find_element(By.CSS_SELECTOR, selector)
                    image = img_elem.get_attribute('src') or img_elem.get_attribute('data-src')
                    if image:
                        break
                except:
                    continue
            
            # Extract link
            link = None
            for selector in selectors.get('link', []):
                try:
                    link_elem = element.find_element(By.CSS_SELECTOR, selector)
                    link = link_elem.get_attribute('href')
                    if link:
                        break
                except:
                    continue
            
            if name and price:
                return {
                    'name': name,
                    'price': price,
                    'currency': 'AUD',  # Default, will be updated based on site
                    'url': link,
                    'image': image,
                    'in_stock': 'out of stock' not in (price_text or '').lower()
                }
            
        except Exception as e:
            print(f"Error extracting product data: {e}")
            
        return None
    
    def close_driver(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
