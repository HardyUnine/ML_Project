import numpy as np
import pandas as pd

def simulate_days(seed, days=30, force_squeeze=False, squeeze_start=np.random.randint(14,17), squeeze_end=np.random.randint(20,23)):
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
    bf_array = [bf]
    rsi_array = [rsi]
    sir_array = [shorts / adv if adv > 0 else 0]
    ss_array = [0]
    
    
    for day in range(1, days + 1):
        # Simulate price change
        if force_squeeze and day < squeeze_start:
            price_change_pct = np.random.uniform(-0.05, -0.15)
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            price_change_pct = np.random.uniform(0.3, 0.5)
        elif force_squeeze and day > squeeze_end:
            price_change_pct = np.random.uniform(-0.05, 0.01)
        else:
            price_change_pct = np.random.normal(0, 0.01)
        price *= (1 + price_change_pct) 
        # append rounding to 2 decimals
        prices.append(round(price, 2))

        # Simulate shorts change
        if force_squeeze and day < squeeze_start:
            shorts_change_pct = np.random.uniform(0.01, 0.03)  # Slow increase pre-squeeze
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            shorts_change_pct = np.random.uniform(-0.15, -0.25)  # AGGRESSIVE covering

        elif force_squeeze and day > squeeze_end:
            shorts_change_pct = np.random.uniform(0.05, 0.1)
        else:
            shorts_change_pct = np.random.normal(0, 0.05)
        shorts *= (1 + shorts_change_pct/10)
        # append rounding to integer 
        shorts_array.append(round(shorts))

        # Simulate BF change
        if force_squeeze and day < squeeze_start:
            bf_change = np.random.uniform(-0.01, 0.01)
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            bf_change = np.random.uniform(0.3, 0.5)
        elif force_squeeze and day > squeeze_end:
            bf_change = np.random.uniform(-0.2, -0.1)
        else:
            bf_change = np.random.normal(0, 0.05)
        bf *= (1 + bf_change/10)
        bf_array.append(round(bf, 2))

        # Simulate ADV change
        if force_squeeze and day < squeeze_start:
            adv_change_pct = np.random.uniform(0.001, 0.01)
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            adv_change_pct = np.random.uniform(0.2, 0.3)
        elif force_squeeze and day > squeeze_end:
            adv_change_pct = np.random.uniform(-0.2, -0.3)
        else:
            adv_change_pct = np.random.normal(0, 0.02)
        adv *= (1 + adv_change_pct)
        adv_array.append(round(adv, 2))

        # Update SIR
        sir = shorts / adv if adv > 0 else 0
        # append --> we round in the data frame creation step
        sir_array.append(sir)

        # Update RSI
        if force_squeeze and day < squeeze_start:
            rsi_change = np.random.uniform(-5, -2)
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            rsi_change = np.random.uniform(10, 20)
        elif force_squeeze and day > squeeze_end:
            rsi_change = np.random.uniform(-10, -5)
        else:
            # rsi change equally likely to go up or down by the same amount
            rsi_change = np.random.normal(0.2, 0.5)
        rsi = max(0, min(100, rsi + rsi_change/10))
        # append rounding to 2 decimals
        rsi_array.append(round(rsi, 2))

        # SS flag
        if force_squeeze and squeeze_start <= day <= squeeze_end:
            ss = 1
        else:
            ss = 0
        ss_array.append(ss)

    # Build DataFrame
    df = pd.DataFrame({
        # Days from 0 to days showing initial seed values as day 0
        'DAY': list(range(0, days + 1)),
        'TICKER': ticker,
        'COMPANY_NAME': company_name,
        'TOTAL_SHARES': total_shares,
        'SHORTS': shorts_array,
        'SIR': [round(val, 2) for val in sir_array],
        'RSI': rsi_array,
        'BF': bf_array,
        'ADV': adv_array,
        'PUBLIC': public_float,
        'PRICE_PER_SHARE': prices,
        'SS': ss_array
    })
    
    return df
