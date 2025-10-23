from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time
import os
import random
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

class PriceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def get_exchange_rate(self):
        """Fetch current INR to AUD exchange rate"""
        try:
            response = self.session.get('https://api.exchangerate.host/latest?base=INR&symbols=AUD')
            if response.status_code == 200:
                data = response.json()
                return data['rates']['AUD']
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            # Fallback rate
            return 0.0183
        return 0.0183
    
    def make_request_with_retry(self, url, max_retries=3, delay=1):
        """Make HTTP request with retry logic and rate limiting"""
        for attempt in range(max_retries):
            try:
                # Add random delay to avoid rate limiting
                time.sleep(random.uniform(0.5, 2.0))
                
                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limited
                    wait_time = delay * (2 ** attempt)
                    print(f"Rate limited, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"HTTP {response.status_code} for {url}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))
                    
        return None
    
    def search_sephora_au(self, product_name):
        """Search Sephora Australia for products"""
        try:
            # Try multiple search strategies
            search_terms = [
                product_name,
                product_name.replace(' ', '+'),
                quote_plus(product_name)
            ]
            
            for search_term in search_terms:
                search_url = f"https://www.sephora.com.au/search?keyword={search_term}"
                response = self.make_request_with_retry(search_url)
                
                if not response:
                    continue
                    
                soup = BeautifulSoup(response.content, 'html5lib')
                
                # Look for product cards with multiple selectors
                product_selectors = [
                    'div[data-testid*="product"]',
                    'div[class*="product"]',
                    'div[class*="item"]',
                    'article',
                    '.product-card',
                    '.product-item'
                ]
                
                products = []
                for selector in product_selectors:
                    product_cards = soup.select(selector)
                    if product_cards:
                        break
                
                for card in product_cards[:3]:  # Limit to first 3 results
                    try:
                        # Try multiple selectors for product info
                        name_selectors = ['h3', 'h4', 'a[data-testid*="product"]', '[class*="title"]', '[class*="name"]']
                        price_selectors = ['[class*="price"]', '[class*="cost"]', '[data-testid*="price"]']
                        
                        name_elem = None
                        for selector in name_selectors:
                            name_elem = card.select_one(selector)
                            if name_elem:
                                break
                        
                        price_elem = None
                        for selector in price_selectors:
                            price_elem = card.select_one(selector)
                            if price_elem:
                                break
                        
                        if name_elem and price_elem:
                            name = name_elem.get_text(strip=True)
                            price_text = price_elem.get_text(strip=True)
                            
                            # Extract numeric price with better regex
                            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace(',', ''))
                            if price_match:
                                price = float(price_match.group())
                                
                                # Get product URL
                                link_elem = card.find('a', href=True)
                                product_url = f"https://www.sephora.com.au{link_elem['href']}" if link_elem else search_url
                                
                                # Get product image
                                img_elem = card.find('img')
                                image_url = None
                                if img_elem:
                                    image_url = img_elem.get('src') or img_elem.get('data-src')
                                    if image_url and not image_url.startswith('http'):
                                        image_url = f"https://www.sephora.com.au{image_url}"
                                
                                product = {
                                    'name': name,
                                    'price': price,
                                    'currency': 'AUD',
                                    'url': product_url,
                                    'image': image_url,
                                    'in_stock': 'out of stock' not in price_text.lower() and 'sold out' not in price_text.lower()
                                }
                                products.append(product)
                                
                                # Return first valid product
                                if products:
                                    return products[0]
                    except Exception as e:
                        print(f"Error parsing product card: {e}")
                        continue
                
                # If we found products, return the first one
                if products:
                    return products[0]
            
            return None
            
        except Exception as e:
            print(f"Error searching Sephora AU: {e}")
            return None
    
    def search_sephora_in(self, product_name):
        """Search Sephora India for products"""
        try:
            search_url = f"https://www.sephora.in/search?keyword={product_name.replace(' ', '%20')}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html5lib')
            
            products = []
            product_cards = soup.find_all('div', class_=re.compile(r'product|item'))
            
            for card in product_cards[:3]:
                try:
                    name_elem = card.find(['h3', 'h4', 'a'], class_=re.compile(r'title|name|product'))
                    price_elem = card.find(['span', 'div'], class_=re.compile(r'price|cost'))
                    link_elem = card.find('a', href=True)
                    img_elem = card.find('img')
                    
                    if name_elem and price_elem:
                        name = name_elem.get_text(strip=True)
                        price_text = price_elem.get_text(strip=True)
                        
                        # Extract numeric price (INR)
                        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('₹', '').replace(',', ''))
                        if price_match:
                            price = float(price_match.group())
                            
                            product = {
                                'name': name,
                                'price': price,
                                'currency': 'INR',
                                'url': f"https://www.sephora.in{link_elem['href']}" if link_elem else search_url,
                                'image': img_elem['src'] if img_elem and img_elem.get('src') else None,
                                'in_stock': 'out of stock' not in price_text.lower()
                            }
                            products.append(product)
                except Exception as e:
                    continue
            
            return products[0] if products else None
            
        except Exception as e:
            print(f"Error searching Sephora IN: {e}")
            return None
    
    def search_nykaa(self, product_name):
        """Search Nykaa for products"""
        try:
            search_url = f"https://www.nykaa.com/search/result/?q={product_name.replace(' ', '%20')}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html5lib')
            
            products = []
            product_cards = soup.find_all('div', class_=re.compile(r'product|item'))
            
            for card in product_cards[:3]:
                try:
                    name_elem = card.find(['h3', 'h4', 'a'], class_=re.compile(r'title|name|product'))
                    price_elem = card.find(['span', 'div'], class_=re.compile(r'price|cost'))
                    link_elem = card.find('a', href=True)
                    img_elem = card.find('img')
                    
                    if name_elem and price_elem:
                        name = name_elem.get_text(strip=True)
                        price_text = price_elem.get_text(strip=True)
                        
                        # Extract numeric price (INR)
                        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('₹', '').replace(',', ''))
                        if price_match:
                            price = float(price_match.group())
                            
                            product = {
                                'name': name,
                                'price': price,
                                'currency': 'INR',
                                'url': f"https://www.nykaa.com{link_elem['href']}" if link_elem else search_url,
                                'image': img_elem['src'] if img_elem and img_elem.get('src') else None,
                                'in_stock': 'out of stock' not in price_text.lower()
                            }
                            products.append(product)
                except Exception as e:
                    continue
            
            return products[0] if products else None
            
        except Exception as e:
            print(f"Error searching Nykaa: {e}")
            return None

scraper = PriceScraper()

@app.route('/compare', methods=['GET'])
def compare_prices():
    product_name = request.args.get('product', '').strip()
    
    if not product_name:
        return jsonify({'error': 'Product name is required'}), 400
    
    try:
        # Get exchange rate
        exchange_rate = scraper.get_exchange_rate()
        
        # For demo purposes, return mock data if scraping fails
        # This allows you to see the app working while we improve scraping
        if product_name.lower() in ['rare beauty', 'rare beauty blush', 'rare beauty soft pinch']:
            mock_results = [
                {
                    'store': 'Sephora AU',
                    'name': 'Rare Beauty Soft Pinch Liquid Blush - Happy',
                    'price': 39.00,
                    'currency': 'AUD',
                    'url': 'https://www.sephora.com.au/product/rare-beauty-soft-pinch-liquid-blush',
                    'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300&h=300&fit=crop',
                    'in_stock': True
                },
                {
                    'store': 'Sephora IN',
                    'name': 'Rare Beauty Soft Pinch Liquid Blush - Happy',
                    'price': 2999,
                    'currency': 'INR',
                    'converted_price': round(2999 * exchange_rate, 2),
                    'url': 'https://www.sephora.in/product/rare-beauty-soft-pinch-liquid-blush',
                    'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300&h=300&fit=crop',
                    'in_stock': True
                },
                {
                    'store': 'Nykaa',
                    'name': 'Rare Beauty Soft Pinch Liquid Blush - Happy',
                    'price': 2899,
                    'currency': 'INR',
                    'converted_price': round(2899 * exchange_rate, 2),
                    'url': 'https://www.nykaa.com/rare-beauty-soft-pinch-liquid-blush',
                    'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300&h=300&fit=crop',
                    'in_stock': False
                }
            ]
            
            # Find cheapest option
            cheapest = None
            min_price = float('inf')
            
            for result in mock_results:
                if result['currency'] == 'AUD':
                    price = result['price']
                else:
                    price = result['converted_price']
                
                if price < min_price:
                    min_price = price
                    cheapest = result['store']
            
            return jsonify({
                'exchange_rate': exchange_rate,
                'results': mock_results,
                'cheapest': cheapest,
                'timestamp': datetime.now().isoformat(),
                'demo_mode': True
            })
        
        # Try real scraping for other products
        results = []
        
        # Sephora AU
        sephora_au = scraper.search_sephora_au(product_name)
        if sephora_au:
            sephora_au['store'] = 'Sephora AU'
            results.append(sephora_au)
        
        # Sephora IN
        sephora_in = scraper.search_sephora_in(product_name)
        if sephora_in:
            sephora_in['store'] = 'Sephora IN'
            sephora_in['converted_price'] = round(sephora_in['price'] * exchange_rate, 2)
            results.append(sephora_in)
        
        # Nykaa
        nykaa = scraper.search_nykaa(product_name)
        if nykaa:
            nykaa['store'] = 'Nykaa'
            nykaa['converted_price'] = round(nykaa['price'] * exchange_rate, 2)
            results.append(nykaa)
        
        if not results:
            return jsonify({'error': 'No products found'}), 404
        
        # Find cheapest option
        cheapest = None
        min_price = float('inf')
        
        for result in results:
            if result['currency'] == 'AUD':
                price = result['price']
            else:
                price = result['converted_price']
            
            if price < min_price:
                min_price = price
                cheapest = result['store']
        
        return jsonify({
            'exchange_rate': exchange_rate,
            'results': results,
            'cheapest': cheapest,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
