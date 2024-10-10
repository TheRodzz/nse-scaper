# NIFTY 50 Returns Analyzer

This Python script fetches historical data for the NIFTY 50 index from the National Stock Exchange of India (NSE) website and calculates 365-day returns. It then visualizes these returns over time.

## Features

- Fetches NIFTY 50 index data from the NSE API
- Calculates 365-day returns for each day, moving backwards in time
- Implements rate limiting and error handling
- Visualizes the returns data using matplotlib
- Uses environment variables for secure cookie storage

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
python nifty50_returns_analyzer.py
```

3. The script will fetch data, calculate returns, and display a plot of the results.

## Configuration

- Adjust the `end_date` in the `get_all_returns()` function to change the analysis period.
- Modify the `time.sleep()` duration to adjust the rate limiting as needed.

## Important Notes

- This script relies on making requests to the NSE website. Ensure you have permission to access and use this data.
- The cookie value in the `.env` file needs to be updated regularly to maintain access to the NSE API.
- Be mindful of NSE's terms of service and any rate limiting they may impose.
- Never commit your `.env` file to version control. Add it to your `.gitignore` file to prevent accidental commits.

## Disclaimer

This tool is for educational and research purposes only. It is not intended for making investment decisions. Always verify the data independently and consult with a financial advisor before making any investment choices.

## License

This project is open-source and available under the MIT License.