from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time
import os

app = Flask(__name__)
CORS(app)

class PriceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
    
    def search_sephora_au(self, product_name):
        """Search Sephora Australia for products"""
        try:
            # Sephora AU search URL
            search_url = f"https://www.sephora.com.au/search?keyword={product_name.replace(' ', '%20')}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html5lib')
            
            # Look for product cards
            products = []
            product_cards = soup.find_all('div', class_=re.compile(r'product|item'))
            
            for card in product_cards[:3]:  # Limit to first 3 results
                try:
                    # Extract product information
                    name_elem = card.find(['h3', 'h4', 'a'], class_=re.compile(r'title|name|product'))
                    price_elem = card.find(['span', 'div'], class_=re.compile(r'price|cost'))
                    link_elem = card.find('a', href=True)
                    img_elem = card.find('img')
                    
                    if name_elem and price_elem:
                        name = name_elem.get_text(strip=True)
                        price_text = price_elem.get_text(strip=True)
                        
                        # Extract numeric price
                        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace(',', ''))
                        if price_match:
                            price = float(price_match.group())
                            
                            product = {
                                'name': name,
                                'price': price,
                                'currency': 'AUD',
                                'url': f"https://www.sephora.com.au{link_elem['href']}" if link_elem else search_url,
                                'image': img_elem['src'] if img_elem and img_elem.get('src') else None,
                                'in_stock': 'out of stock' not in price_text.lower()
                            }
                            products.append(product)
                except Exception as e:
                    continue
            
            return products[0] if products else None
            
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
        
        # Search all three stores
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
