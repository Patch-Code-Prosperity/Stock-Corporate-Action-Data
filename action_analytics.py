import pandas as pd
import yfinance as yf
from datetime import timedelta


# This script fetches stock prices for a given ticker symbol for specific dates and adds them to a DataFrame.

# Function to fetch stock prices
def fetch_stock_price(ticker, date_before, date_after):
    """
    Fetches the adjusted close price for a given stock ticker within a specified date range.

    Parameters:
    ticker (str): The stock ticker symbol.
    date_before (str): The start date for the price data in 'YYYY-MM-DD' format.
    date_after (str): The end date for the price data in 'YYYY-MM-DD' format.

    Returns:
    pd.Series: A series containing the adjusted close prices for the given date range.
    """
    stock_data = yf.download(ticker, start=date_before, end=date_after)
    return stock_data['Adj Close']


# Read the CSV file into a DataFrame
csv_file_path = 'final_updated_extracted_actions.csv'
extracted_actions_df = pd.read_csv(csv_file_path)

# Initialize empty lists to store stock prices
prices_day_before = []
prices_three_days_after = []

# Loop through each row in the DataFrame to fetch stock prices
for _, row in extracted_actions_df.iterrows():
    ticker = row['Ticker']
    action_date = pd.to_datetime(row['Action Date'])

    # Calculate the date one day before and three days after the action
    date_before = action_date - timedelta(days=1)
    date_after = action_date + timedelta(days=3)

    # Fetch stock prices
    try:
        prices = fetch_stock_price(ticker, date_before.strftime('%Y-%m-%d'), date_after.strftime('%Y-%m-%d'))

        # Store the prices in the lists
        prices_day_before.append(prices.get(date_before, None))
        prices_three_days_after.append(prices.get(date_after, None))

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        prices_day_before.append(None)
        prices_three_days_after.append(None)

# Add the fetched stock prices as new columns in the DataFrame
extracted_actions_df['Price Day Before'] = prices_day_before
extracted_actions_df['Price 3 Days After'] = prices_three_days_after

# Save the DataFrame to a new CSV file if needed
extracted_actions_df.to_csv('updated_file.csv', index=False)  # Replace the path as needed
