import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

# Create a persistent session
session = requests.Session()

# Headers with updated cookies (make sure to refresh these before running)
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
    'cookie': os.getenv('NSE_COOKIE'),
    'referer': 'https://www.nseindia.com/reports-indices-historical-index-data',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def get_index_data(date_range, retries=5):
    from_date, to_date = date_range
    url = f"https://www.nseindia.com/api/historical/indicesHistory?indexType=NIFTY%2050&from={from_date}&to={to_date}"
    
    attempt = 0
    while attempt < retries:
        try:
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json().get('data', {}).get('indexCloseOnlineRecords', [])
                return from_date, to_date, data
            elif response.status_code == 429:
                print(f"Rate limit exceeded for {from_date} to {to_date}. Retrying after a delay...")
                time.sleep(2 ** attempt)  # Exponential backoff
            elif response.status_code == 401:
                print(f"Unauthorized request for {from_date} to {to_date}. Please check your headers or cookies.")
                break
            else:
                print(f"Failed to fetch data for {from_date} to {to_date}. Status Code: {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {from_date} to {to_date}: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff for other request failures
        attempt += 1
    return from_date, to_date, []

def calculate_return(data):
    if len(data) >= 2:
        start_close = data[0]['EOD_CLOSE_INDEX_VAL']
        end_close = data[-1]['EOD_CLOSE_INDEX_VAL']
        return (end_close - start_close) / start_close * 100
    return None

def get_all_returns():
    end_date = datetime.strptime("01-10-2024", "%d-%m-%Y")
    date_ranges = []
    
    while True:
        start_date = end_date - timedelta(days=365)
        from_date = start_date.strftime("%d-%m-%Y")
        to_date = end_date.strftime("%d-%m-%Y")
        date_ranges.append((from_date, to_date))
        end_date = end_date - timedelta(days=1)
        if start_date.year < 1990:  # Assuming data is not available before 1990
            break
    
    returns = []
    dates = []
    
    # Create CSV file and write header
    csv_filename = 'nifty50_returns.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date', 'Return (%)', 'Start Date', 'End Date'])
    
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        future_to_date_range = {executor.submit(get_index_data, date_range): date_range for date_range in date_ranges}
        for future in as_completed(future_to_date_range):
            from_date, to_date, data = future.result()
            if data:
                print(f'Fetched data for time period {from_date} to {to_date}')
                yearly_return = calculate_return(data)
                if yearly_return is not None:
                    returns.append(yearly_return)
                    dates.append(to_date)
                    
                    # Append data to CSV file
                    with open(csv_filename, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow([to_date, yearly_return, from_date, to_date])
            time.sleep(0.2)  # Small delay to avoid overwhelming the server
    
    return returns, dates

def plot_returns(returns, dates):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, returns, marker='o')
    plt.title('NIFTY 50 Returns for 365-Day Periods (Daily Shift)')
    plt.xlabel('Date')
    plt.ylabel('Return (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    returns, dates = get_all_returns()
    plot_returns(returns, dates)
    print(f"Data has been saved to nifty50_returns.csv")