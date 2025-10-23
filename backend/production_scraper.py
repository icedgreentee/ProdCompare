"""
Production-ready scraping with multiple fallback strategies
"""
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus
from advanced_scraper import AdvancedScraper
from scraping_config import get_headers_with_user_agent, SELECTORS, RATE_LIMITS

class ProductionScraper:
    def __init__(self):
        self.session = requests.Session()
        self.advanced_scraper = AdvancedScraper()
        self.last_request_time = {}
        
    def rate_limit_check(self, site):
        """Check if we need to rate limit for a site"""
        if site in self.last_request_time:
            time_since_last = time.time() - self.last_request_time[site]
            min_delay = RATE_LIMITS.get(site, {}).get('delay_between_requests', 5)
            if time_since_last < min_delay:
                time.sleep(min_delay - time_since_last)
        self.last_request_time[site] = time.time()
    
    def search_with_fallback(self, site, product_name):
        """Search with multiple fallback strategies"""
        strategies = [
            self.search_with_requests,
            self.search_with_selenium,
            self.search_with_api
        ]
        
        for strategy in strategies:
            try:
                result = strategy(site, product_name)
                if result:
                    return result
            except Exception as e:
                print(f"Strategy failed: {e}")
                continue
        
        return None
    
    def search_with_requests(self, site, product_name):
        """Search using requests + BeautifulSoup"""
        self.rate_limit_check(site)
        
        # Get site-specific URL and headers
        urls = self.get_search_urls(site, product_name)
        headers = get_headers_with_user_agent()
        
        for url in urls:
            try:
                response = self.session.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html5lib')
                    product = self.extract_product_from_soup(soup, site)
                    if product:
                        return product
            except Exception as e:
                print(f"Requests strategy failed for {url}: {e}")
                continue
        
        return None
    
    def search_with_selenium(self, site, product_name):
        """Search using Selenium for JavaScript-heavy sites"""
        try:
            urls = self.get_search_urls(site, product_name)
            selectors = SELECTORS.get(site, {})
            
            for url in urls:
                result = self.advanced_scraper.scrape_with_selenium(url, selectors)
                if result:
                    return result
        except Exception as e:
            print(f"Selenium strategy failed: {e}")
        
        return None
    
    def search_with_api(self, site, product_name):
        """Search using official APIs if available"""
        # This would implement official API calls
        # For now, return None to use other strategies
        return None
    
    def get_search_urls(self, site, product_name):
        """Get multiple search URL variations"""
        base_urls = {
            'sephora_au': 'https://www.sephora.com.au/search',
            'sephora_in': 'https://www.sephora.in/search',
            'nykaa': 'https://www.nykaa.com/search'
        }
        
        base_url = base_urls.get(site)
        if not base_url:
            return []
        
        # Create multiple URL variations
        search_terms = [
            product_name,
            product_name.replace(' ', '+'),
            quote_plus(product_name),
            product_name.replace(' ', '%20')
        ]
        
        urls = []
        for term in search_terms:
            urls.append(f"{base_url}?keyword={term}")
            urls.append(f"{base_url}?q={term}")
        
        return urls
    
    def extract_product_from_soup(self, soup, site):
        """Extract product data from BeautifulSoup object"""
        selectors = SELECTORS.get(site, {})
        
        # Find product cards
        product_cards = []
        for selector in selectors.get('product_cards', []):
            cards = soup.select(selector)
            if cards:
                product_cards = cards
                break
        
        if not product_cards:
            return None
        
        # Extract data from first product
        product_card = product_cards[0]
        
        # Extract name
        name = None
        for selector in selectors.get('name', []):
            elem = product_card.select_one(selector)
            if elem:
                name = elem.get_text(strip=True)
                if name:
                    break
        
        # Extract price
        price = None
        price_text = None
        for selector in selectors.get('price', []):
            elem = product_card.select_one(selector)
            if elem:
                price_text = elem.get_text(strip=True)
                if price_text:
                    import re
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace(',', ''))
                    if price_match:
                        price = float(price_match.group())
                        break
        
        # Extract image
        image = None
        for selector in selectors.get('image', []):
            elem = product_card.select_one(selector)
            if elem:
                image = elem.get('src') or elem.get('data-src')
                if image:
                    break
        
        # Extract link
        link = None
        for selector in selectors.get('link', []):
            elem = product_card.select_one(selector)
            if elem:
                link = elem.get('href')
                if link:
                    break
        
        if name and price:
            return {
                'name': name,
                'price': price,
                'currency': 'AUD' if site == 'sephora_au' else 'INR',
                'url': link,
                'image': image,
                'in_stock': 'out of stock' not in (price_text or '').lower()
            }
        
        return None
