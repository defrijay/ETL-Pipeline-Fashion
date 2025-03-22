import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np
import re

def extract_data():
    data = []
    base_url = "https://fashion-studio.dicoding.dev/"
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {base_url}: {e}")
        return pd.DataFrame(columns=['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp'])
    
    def scrape_page(url, page_num):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data from {url}: {e}")
            return
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return
        
        products = soup.find_all('div', class_='collection-card')
        if not products:
            print(f"No products found on page {page_num}")
        
        for product in products:
            title = product.find('h3', class_='product-title').text.strip() if product.find('h3', class_='product-title') else 'Unknown Product'
            price = product.find('span', class_='price').text.strip() if product.find('span', class_='price') else 'Price Unavailable'
            
            rating_elem = product.find('p', text=lambda x: x and 'Rating:' in x)
            if rating_elem:
                rating_text = rating_elem.text.replace('Rating: ⭐', '').strip()
                rating_match = re.search(r'(\d+(\.\d+)?) / 5', rating_text)
                rating = rating_match.group(1) if rating_match else 'Invalid Rating'
            else:
                rating = 'Invalid Rating'
            
            colors = product.find_all('p')[1].text.strip() if len(product.find_all('p')) > 1 else np.nan
            size = product.find_all('p')[2].text.strip() if len(product.find_all('p')) > 2 else np.nan
            gender = product.find_all('p')[3].text.strip() if len(product.find_all('p')) > 3 else np.nan
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            data.append([title, price, rating, colors, size, gender, timestamp])
            print(f"Extracted data: {title}, {price}, {rating}, {colors}, {size}, {gender}, {timestamp}")
    
    # Scrape halaman utama sebagai halaman pertama
    scrape_page(base_url, 1)
    
    # Scrape halaman berikutnya
    for page in range(2, 51):  
        page_url = f"{base_url}page{page}"
        scrape_page(page_url, page)
    
    return pd.DataFrame(data, columns=['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp'])
