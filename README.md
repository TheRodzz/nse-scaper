
# Nifty Indices Data Scraper

This Python script fetches historical data for a list of Nifty indices from the NSE website and saves the data in CSV format. The script uses multi-threading to speed up the process of data fetching and logging to track progress.

## Features

- Fetches data for multiple Nifty indices using a list of predefined index names.
- Supports fetching data for a specific date range.
- Saves the fetched data into CSV files.
- Multi-threaded to improve performance using `ThreadPoolExecutor`.
- Uses environment variables for sensitive data (e.g., cookies).
- Includes logging for error handling and progress tracking.

## Requirements

- Python 3.7+
- `requests` for making HTTP requests.
- `dotenv` for loading environment variables from a `.env` file.
- `csv` for saving data into CSV format.
- `concurrent.futures` for handling multi-threading.
- `logging` for tracking the process.
- `.env` file to store the required environment variables.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/TheRodzz/nse-scaper.git
    cd nse-scraper
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the `.env` file in the root directory of the project with the following content:

    ```
    cookie=your_cookie_here
    ```

## Usage

1. To run the script, simply execute the following command:

    ```bash
    python nse-scraper.py
    ```

2. The data will be fetched and saved to CSV files in the `nifty_data` folder. Each index will have its own CSV file.

## Customization

- You can modify the list of Nifty indices in the `INDEX_NAMES` list.
- Adjust the date range by changing the `START_DATE` and `END_DATE` variables.
  
    Example:
    
    ```python
    START_DATE = datetime(2000, 1, 1)
    END_DATE = datetime(2023, 12, 31)
    ```

## Logging

The script logs its activities, including successful downloads and errors, which can be helpful for monitoring its progress. The log messages are printed to the console.

## Contributing

If you wish to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.