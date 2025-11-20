import numpy as np
import pandas as pd

def update_rsi(rsi_prev, price_change_pct, day, squeeze_start, squeeze_end):
    if squeeze_start <= day <= squeeze_end:
        rsi_step = price_change_pct * 20 + np.random.normal(0, 1)
    elif day < squeeze_start:
        rsi_step = price_change_pct * 10 + np.random.normal(0, 0.5)
    else:
        rsi_step = price_change_pct * 40 + np.random.normal(0, 0.2)
    return float(np.clip(rsi_prev + rsi_step, 0, 100))


def simulate_days(seed, days=30, force_squeeze=False, squeeze_start=4, squeeze_end=24):
    np.random.seed(42)  # reproducibility
    
    # Initialize values from seed
    total_shares = seed['TOTAL_SHARES']
    shorts = seed['SHORTS']
    adv = seed['ADV']
    public_float = seed['PUBLIC']
    price = seed['PRICE_PER_SHARE']
    bf = seed['BF']
    rsi = seed['RSI']
    ticker = seed['TICKER']
    company_name = seed['COMPANY_NAME']
    
    prices = [price]
    shorts_array = [shorts]
    adv_array = [adv]
    rsi_array = [rsi]
    sir_array = [shorts / adv if adv > 0 else 0]
    ss_array = [0]
    
    for day in range(1, days + 1):
        squeeze_active = force_squeeze and (squeeze_start <= day <= squeeze_end)
        post_squeeze = force_squeeze and (day > squeeze_end)
        
        # Price dynamics
        if squeeze_active:
            daily_return = np.random.normal(0.15, 0.05)  # surge
        elif post_squeeze:
            daily_return = np.random.normal(-0.20, 0.03)  # retracement
        else:
            daily_return = np.random.normal(0.001, 0.005)  # normal
        
        new_price = max(prices[-1] * (1 + daily_return), 0.1)
        prices.append(new_price)
        
        # Shorts dynamics
        if squeeze_active:
            shorts = max(shorts * np.random.uniform(0.7, 0.85) + np.random.randint(-50000, 50000), 0)
        else:
            if day < squeeze_start:
                shorts = shorts * np.random.uniform(1.01, 1.05) + np.random.randint(-10000, 20000)
            else:
                shorts = shorts * np.random.uniform(0.99, 1.01) + np.random.randint(-10000, 10000)
            shorts = max(shorts, 0)
        shorts_array.append(int(shorts))
        
        # Volume (ADV) dynamics
        if squeeze_active:
            adv = adv * np.random.uniform(1.1, 1.3) + np.random.randint(50000, 200000)
        elif day < squeeze_start:
            adv = adv * np.random.uniform(1.01, 1.05) + np.random.randint(-10000, 10000)
        else:
            adv = adv * np.random.uniform(0.95, 0.98) + np.random.randint(-10000, 10000)
            adv = max(adv, seed['ADV'] * 0.85)
        adv_array.append(int(adv))
        
        # Calculate SIR
        sir = shorts / adv if adv > 0 else 0
        sir_array.append(round(sir, 2))
        
        # Update RSI
        price_change_pct = (prices[-1] - prices[-2]) / prices[-2] if prices[-2] > 0 else 0
        rsi = update_rsi(rsi, price_change_pct, day, squeeze_start, squeeze_end)
        rsi_array.append(round(rsi, 2))
        
        # Squeeze flag
        ss_array.append(1 if squeeze_active else 0)
    
    # Build DataFrame
    df = pd.DataFrame({
        'DAY': list(range(1, days + 1)),
        'TICKER': ticker,
        'COMPANY_NAME': company_name,
        'TOTAL_SHARES': total_shares,
        'SHORTS': shorts_array[1:],  # exclude initial seed
        'SIR': sir_array[1:],
        'RSI': rsi_array[1:],
        'BF': round(bf, 2),
        'ADV': adv_array[1:],
        'PUBLIC': public_float,
        'PRICE_PER_SHARE': [round(p, 2) for p in prices[1:]],
        'SS': ss_array[1:]
    })
    
    return df
