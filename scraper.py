import requests
import json
import csv
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
INDEX_NAMES = [
    "NIFTY 100", "NIFTY 200", "NIFTY 50", "NIFTY 50 ARBITRAGE", "NIFTY 50 FUTURES PR",
    "NIFTY 50 FUTURES TR", "NIFTY 500", "NIFTY ALPHA 50", "NIFTY ALPHA LOW-VOLATILITY 30",
    "NIFTY ALPHA QUALITY LOW-VOLATILITY 30", "NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30",
    "NIFTY AUTO", "NIFTY BANK", "NIFTY CAPITAL MARKETS", "NIFTY COMMODITIES",
    "NIFTY CONSUMER DURABLES", "NIFTY CORE HOUSING", "NIFTY CPSE",
    "NIFTY DIVIDEND OPPORTUNITIES 50", "NIFTY ENERGY", "NIFTY EV & NEW AGE AUTOMOTIVE",
    "NIFTY FINANCIAL SERVICES", "NIFTY FINANCIAL SERVICES 25/50",
    "NIFTY FINANCIAL SERVICES EX-BANK", "NIFTY FMCG", "NIFTY GROWTH SECTORS 15",
    "NIFTY HEALTHCARE", "NIFTY HIGH BETA 50", "NIFTY HOUSING", "NIFTY INDIA CONSUMPTION",
    "NIFTY INDIA CORPORATE GROUP INDEX - ADITYA BIRLA GROUP",
    "NIFTY INDIA CORPORATE GROUP INDEX - MAHINDRA GROUP",
    "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP",
    "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP", "NIFTY INDIA DEFENCE",
    "NIFTY INDIA DIGITAL", "NIFTY INDIA MANUFACTURING", "NIFTY INDIA TOURISM",
    "NIFTY INFRASTRUCTURE", "NIFTY IPO", "NIFTY IT", "NIFTY LARGEMIDCAP 250",
    "NIFTY LOW VOLATILITY 50", "NIFTY MEDIA", "NIFTY METAL", "NIFTY MICROCAP 250",
    "NIFTY MIDCAP 100", "NIFTY MIDCAP 150", "NIFTY MIDCAP 50", "NIFTY MIDCAP LIQUID 15",
    "NIFTY MIDCAP SELECT", "NIFTY MIDCAP150 MOMENTUM 50", "NIFTY MIDCAP150 QUALITY 50",
    "NIFTY MIDSMALL FINANCIAL SERVICES", "NIFTY MIDSMALL HEALTHCARE",
    "NIFTY MIDSMALL INDIA CONSUMPTION", "NIFTY MIDSMALL IT & TELECOM",
    "NIFTY MIDSMALLCAP 400", "NIFTY MIDSMALLCAP400 MOMENTUM QUALITY 100", "NIFTY MNC",
    "NIFTY MOBILITY", "NIFTY NEXT 50", "NIFTY NON-CYCLICAL CONSUMER", "NIFTY OIL & GAS",
    "NIFTY PHARMA", "NIFTY PRIVATE BANK", "NIFTY PSE", "NIFTY PSU BANK",
    "NIFTY QUALITY LOW-VOLATILITY 30", "NIFTY REALTY", "NIFTY REITS & INVITS",
    "NIFTY RURAL", "NIFTY SERVICES SECTOR", "NIFTY SHARIAH 25", "NIFTY SMALLCAP 100",
    "NIFTY SMALLCAP 250", "NIFTY SMALLCAP 50", "NIFTY SMALLCAP250 MOMENTUM QUALITY 100",
    "NIFTY SMALLCAP250 QUALITY 50", "NIFTY SME EMERGE", "NIFTY TOP 10 EQUAL WEIGHT",
    "NIFTY TOTAL MARKET", "NIFTY TRANSPORTATION & LOGISTICS", "NIFTY100 ALPHA 30",
    "NIFTY100 ENHANCED ESG", "NIFTY100 EQUAL WEIGHT", "NIFTY100 ESG",
    "NIFTY100 ESG SECTOR LEADERS", "NIFTY100 LIQUID 15", "NIFTY100 LOW VOLATILITY 30",
    "NIFTY100 QUALITY 30", "NIFTY200 ALPHA 30", "NIFTY200 MOMENTUM 30",
    "NIFTY200 QUALITY 30", "NIFTY200 VALUE 30", "NIFTY50 DIVIDEND POINTS",
    "NIFTY50 EQUAL WEIGHT", "NIFTY50 PR 1X INVERSE", "NIFTY50 PR 2X LEVERAGE",
    "NIFTY50 SHARIAH", "NIFTY50 TR 1X INVERSE", "NIFTY50 TR 2X LEVERAGE", "NIFTY50 USD",
    "NIFTY50 VALUE 20", "NIFTY500 EQUAL WEIGHT",
    "NIFTY500 LARGEMIDSMALL EQUAL-CAP WEIGHTED", "NIFTY500 MOMENTUM 50",
    "NIFTY500 MULTICAP 50:25:25", "NIFTY500 MULTICAP INDIA MANUFACTURING 50:30:20",
    "NIFTY500 MULTICAP INFRASTRUCTURE 50:30:20",
    "NIFTY500 MULTICAP MOMENTUM QUALITY 50", "NIFTY500 SHARIAH", "NIFTY500 VALUE 50"
]

BASE_URL = "https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString"
OUTPUT_DIR = "nifty_data"
START_DATE = datetime(1991, 1, 1)
END_DATE = datetime(2024, 10, 1)  # Update this to the current date when running the script

# Prepare headers
HEADERS = {
    "connection": "keep-alive",
    "content-type": "application/json; charset=UTF-8",
    "cookie": os.getenv('COOKIE'),
    "host": "www.niftyindices.com",
    "origin": "https://www.niftyindices.com",
    "referer": "https://www.niftyindices.com/reports/historical-data",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

def fetch_data(index_name, start_date, end_date):
    """Fetch data for a given index and date range."""
    payload = {
        "cinfo": json.dumps({
            "name": index_name,
            "startDate": start_date.strftime('%d-%b-%Y'),
            "endDate": end_date.strftime('%d-%b-%Y'),
            "indexName": index_name
        })
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        return json.loads(response.json()['d'])
    except requests.RequestException as e:
        logger.error(f"Error fetching data for {index_name} from {start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}: {str(e)}")
        return None

def save_to_csv(data, filename):
    """Save data to a CSV file."""
    if not data:
        logger.warning(f"No data to save for {filename}")
        return
    
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for row in data:
            row.pop('RequestNumber', None)  # Remove the RequestNumber column
            writer.writerow(row)

csv_lock = threading.Lock()

def process_index(index_name):
    """Process a single index."""
    try:
        data = fetch_data(index_name, START_DATE, END_DATE)
        if data:
            filename = os.path.join(OUTPUT_DIR, f"{index_name.replace(' ', '_')}.csv")
            with csv_lock:
                save_to_csv(data, filename)
            logger.info(f"Data for {index_name} from {START_DATE.strftime('%d-%b-%Y')} to {END_DATE.strftime('%d-%b-%Y')} saved successfully.")
        else:
            logger.warning(f"No data fetched for {index_name} from {START_DATE.strftime('%d-%b-%Y')} to {END_DATE.strftime('%d-%b-%Y')}")
    except Exception as e:
        logger.error(f"Error processing data for {index_name} from {START_DATE.strftime('%d-%b-%Y')} to {END_DATE.strftime('%d-%b-%Y')}: {str(e)}")

def main():
    """Main function to run the scraper."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_index, index_name) for index_name in INDEX_NAMES]
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions that occurred during execution

if __name__ == "__main__":
    main()