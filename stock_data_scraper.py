# imports 
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

# MANUAL DATA FROM FINVIZ FOR SHORTS AND WEB ARCHIVE FOR BORROW FEE
#https://finviz.com/quote.ashx?t=GME&ty=si&p=d
#https://web.archive.org/web/20210304230440/https://iborrowdesk.com/report/GME
MANUAL_DATA = {
    "2021-01-04": {"short_float_pct": 121.05, "bf": 0.226},
    "2021-01-05": {"short_float_pct": 121.05, "bf": 0.226},
    "2021-01-06": {"short_float_pct": 121.05, "bf": 0.219},
    "2021-01-07": {"short_float_pct": 121.05, "bf": 0.163},
    "2021-01-08": {"short_float_pct": 121.05, "bf": 0.217},
    "2021-01-11": {"short_float_pct": 121.05, "bf": 0.217},
    "2021-01-12": {"short_float_pct": 121.05, "bf": 0.245},
    "2021-01-13": {"short_float_pct": 121.05, "bf": 0.224},
    "2021-01-14": {"short_float_pct": 121.05, "bf": 0.273},
    "2021-01-15": {"short_float_pct": 105.04, "bf": 0.453},
    "2021-01-19": {"short_float_pct": 105.04, "bf": 0.312},
    "2021-01-20": {"short_float_pct": 105.04, "bf": 0.255},
    "2021-01-21": {"short_float_pct": 105.04, "bf": 0.258},
    "2021-01-22": {"short_float_pct": 105.04, "bf": 0.236},
    "2021-01-25": {"short_float_pct": 105.04, "bf": 0.327},
    "2021-01-26": {"short_float_pct": 105.04, "bf": 0.836},
    "2021-01-27": {"short_float_pct": 105.04, "bf": 0.509},
    "2021-01-28": {"short_float_pct": 105.04, "bf": 0.420},
    "2021-01-29": {"short_float_pct": 36.40, "bf": 0.360},
    "2021-02-01": {"short_float_pct": 36.40, "bf": 0.280},
    "2021-02-02": {"short_float_pct": 36.40, "bf": 0.200},
    "2021-02-03": {"short_float_pct": 36.40, "bf": 0.150},
    "2021-02-04": {"short_float_pct": 36.40, "bf": 0.100},
    "2021-02-05": {"short_float_pct": 36.40, "bf": 0.090},
    "2021-02-08": {"short_float_pct": 36.40, "bf": 0.040},
    "2021-02-09": {"short_float_pct": 36.40, "bf": 0.030},
    "2021-02-10": {"short_float_pct": 36.40, "bf": 0.020},
    "2021-02-11": {"short_float_pct": 36.40, "bf": 0.020},
    "2021-02-12": {"short_float_pct": 32.83, "bf": 0.020},
    "2021-02-16": {"short_float_pct": 32.83, "bf": 0.010},
}


# CONFIGS
SYMBOL = "GME"
COMPANY_NAME = "GameStop Corp."
START_DATE = "2021-01-04"
END_DATE = "2021-02-16"
ALPHA_VANTAGE_API_KEY = "KVF6G8WHRYA1I47U"


# HELPER FUNCTIONS
def get_price_volume_data(symbol, start_date, end_date):
    """Fetch OHLCV data with 60-day buffer for RSI calculation"""
    ticker = yf.Ticker(symbol)
    buffer_days = 60
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    buffer_dt = start_dt - timedelta(days=buffer_days)
    buffer_start_str = buffer_dt.strftime("%Y-%m-%d")
    
    hist = ticker.history(start=buffer_start_str, end=end_date)
    hist.reset_index(inplace=True)
    hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
    
    return hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]


def get_shares_info(symbol):
    """Get shares outstanding and float"""
    ticker = yf.Ticker(symbol)
    info = ticker.info
    return {
        'sharesOutstanding': info.get('sharesOutstanding', 447908690),  # GME Jan 2021
        'floatShares': info.get('floatShares', 408656827),  # GME Jan 2021
    }

def get_rsi_from_api(symbol, api_key):
    """Fetch RSI from Alpha Vantage API"""
    print("  - Fetching RSI from Alpha Vantage API...")
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'RSI',
        'symbol': symbol,
        'interval': 'daily',
        'time_period': 14,
        'series_type': 'close',
        'apikey': api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'Technical Analysis: RSI' in data:
            rsi_data = data['Technical Analysis: RSI']
            df = pd.DataFrame.from_dict(rsi_data, orient='index')
            df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
            df.columns = ['RSI']
            df['RSI'] = df['RSI'].astype(float)
            return df
        else:
            print(f"Warning: Could not fetch RSI. Response: {data}")
            return None
    except Exception as e:
        print(f"Error fetching RSI: {e}")
        return None



def calculate_adv(volume_series, period=20):
    """Calculate Average Daily Volume"""
    return volume_series.rolling(window=period, min_periods=1).mean()


# BUILD DATASET WITH MANUAL DATA
def build_stock_dataset():    
    # Get price vol data (with our for the rsi calc buffer)
    price_data = get_price_volume_data(SYMBOL, START_DATE, END_DATE)
    
    # Get shares info
    shares_info = get_shares_info(SYMBOL)
    public_float = shares_info['floatShares']
    total_shares = shares_info['sharesOutstanding']
    
    # Get RSI from API and ADV calculation
    rsi_df = get_rsi_from_api(SYMBOL, "KVF6G8WHRYA1I47U")
    price_data['ADV'] = calculate_adv(price_data['Volume'])
    
    # Merge RSI data by date
    if rsi_df is not None:
        price_data = price_data.merge(rsi_df, left_on='Date', right_index=True, how='left')
    else:
        price_data['RSI'] = 50.0  # Fallback

    # Filter to our requested date range only
    price_data = price_data[price_data['Date'] >= START_DATE]
    price_data.reset_index(drop=True, inplace=True)
    
    # Build final dataset with manual short data
    results = []
    
    for idx, row in price_data.iterrows():
        date_str = row['Date']
        adv = row['ADV'] if pd.notna(row['ADV']) else row['Volume']
        
        # Get manual data for this date (if available)
        if date_str in MANUAL_DATA:
            manual = MANUAL_DATA[date_str]
            short_float_pct = manual['short_float_pct']
            bf = manual['bf']
            
            # Calculate SHORTS from Short Float %
            shorts = int((short_float_pct / 100.0) * public_float)
            
            # Calculate SIR (Days to Cover) = SHORTS / ADV
            sir = shorts / adv if adv > 0 else 0
        else:
            # Fallback if date not in manual data
            shorts = 0
            sir = 0
            bf = 0.12
        
        results.append({
            'DAY': idx,
            'TICKER': SYMBOL,
            'COMPANY_NAME': COMPANY_NAME,
            'TOTAL_SHARES': total_shares,
            'SHORTS': shorts,
            'SIR': round(sir, 2),
            'RSI': round(row['RSI'], 2) if pd.notna(row['RSI']) else 50.0,
            'BF': round(bf, 4),
            'ADV': round(adv, 0),
            'PUBLIC': public_float,
            'PRICE_PER_SHARE': round(row['Close'], 2),
            'SS': 0  # Placeholder
        })
    
    return pd.DataFrame(results)


# MAIN EXECUTION
if __name__ == "__main__":
    df = build_stock_dataset()
    
    output_file = f"{SYMBOL}_api.csv"
    df.to_csv(output_file, index=False)
    