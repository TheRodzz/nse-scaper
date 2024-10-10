# NIFTY 50 Returns Analyzer

This Python script fetches historical data for the NIFTY 50 index from the National Stock Exchange of India (NSE) website and calculates 365-day returns. It then visualizes these returns over time. The script now uses parallel processing to significantly speed up data retrieval.

## Features

- Fetches NIFTY 50 index data from the NSE API using parallel processing
- Calculates 365-day returns for each day, moving backwards in time
- Implements rate limiting, error handling, and retry mechanisms
- Visualizes the returns data using matplotlib
- Uses environment variables for secure cookie storage
- Saves fetched data to a CSV file for further analysis

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone this repository or download the script.
2. Install the required packages:

```bash
pip install requests pandas matplotlib python-dotenv
```

3. Create a `.env` file in the same directory as the script with the following content:

```
NSE_COOKIE=your_nse_cookie_value_here
```

Replace `your_nse_cookie_value_here` with the actual cookie value from the NSE website.

## Usage

1. Ensure your `.env` file is set up with the correct NSE_COOKIE value.
2. Run the script:

```bash
python scraper.py
```

3. The script will fetch data using parallel processing, calculate returns, save the data to a CSV file, and display a plot of the results.

## Configuration

- Adjust the `end_date` in the `get_all_returns()` function to change the analysis period.
- Modify the `max_workers` parameter in `ThreadPoolExecutor(max_workers=5)` to adjust the number of concurrent requests.
- Adjust the `time.sleep(0.2)` duration in the main loop to fine-tune the rate limiting as needed.

## Important Notes

- This script relies on making requests to the NSE website. Ensure you have permission to access and use this data.
- The cookie value in the `.env` file needs to be updated regularly to maintain access to the NSE API.
- Be mindful of NSE's terms of service and any rate limiting they may impose.
- The parallel processing feature significantly improves performance but may require adjustments based on your system's capabilities and the server's rate limits.

## Disclaimer

This tool is for educational and research purposes only. It is not intended for making investment decisions. Always verify the data independently and consult with a financial advisor before making any investment choices.

## License

This project is open-source and available under the MIT License.