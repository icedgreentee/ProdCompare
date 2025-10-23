# Scraping Configuration
import random

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
]

# Request headers
HEADERS = {
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
}

# Rate limiting settings
RATE_LIMITS = {
    'sephora_au': {'requests_per_minute': 10, 'delay_between_requests': 6},
    'sephora_in': {'requests_per_minute': 10, 'delay_between_requests': 6},
    'nykaa': {'requests_per_minute': 15, 'delay_between_requests': 4}
}

# Product selectors for different sites
SELECTORS = {
    'sephora_au': {
        'product_cards': [
            'div[data-testid*="product"]',
            'div[class*="product"]',
            'article[class*="product"]',
            '.product-card',
            '.product-item'
        ],
        'name': ['h3', 'h4', 'a[data-testid*="product"]', '[class*="title"]', '[class*="name"]'],
        'price': ['[class*="price"]', '[class*="cost"]', '[data-testid*="price"]', '.price'],
        'image': ['img[data-testid*="product"]', 'img[class*="product"]', 'img'],
        'link': ['a[href*="/product/"]', 'a[data-testid*="product"]']
    },
    'sephora_in': {
        'product_cards': [
            'div[class*="product"]',
            'article[class*="product"]',
            '.product-card',
            '.product-item'
        ],
        'name': ['h3', 'h4', '[class*="title"]', '[class*="name"]'],
        'price': ['[class*="price"]', '[class*="cost"]', '.price'],
        'image': ['img[class*="product"]', 'img'],
        'link': ['a[href*="/product/"]']
    },
    'nykaa': {
        'product_cards': [
            'div[class*="product"]',
            'article[class*="product"]',
            '.product-card',
            '.product-item'
        ],
        'name': ['h3', 'h4', '[class*="title"]', '[class*="name"]'],
        'price': ['[class*="price"]', '[class*="cost"]', '.price'],
        'image': ['img[class*="product"]', 'img'],
        'link': ['a[href*="/product/"]']
    }
}

def get_random_user_agent():
    """Get a random user agent"""
    return random.choice(USER_AGENTS)

def get_headers_with_user_agent():
    """Get headers with random user agent"""
    headers = HEADERS.copy()
    headers['User-Agent'] = get_random_user_agent()
    return headers
