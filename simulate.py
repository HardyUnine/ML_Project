import numpy as np
import pandas as pd

#def simulate_days(seed, days=30, force_squeeze=False, squeeze_start=np.random.randint(12,13), squeeze_end=np.random.randint(18,19)):
def simulate_days(seed, days=30, force_squeeze=False, squeeze_start=13, squeeze_end=19):
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
            price_change_pct = np.random.uniform(0.02, 0.08)
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            price_change_pct = np.random.uniform(0.30, 0.50)  # +25% to +45% per day, should arrive to peak like real daata
        elif force_squeeze and day == squeeze_end + 1:
            # Reset price to squeeze_start price (day 13's price)
            price = prices[squeeze_start]  # Use the price from squeeze_start day
            
        elif force_squeeze and day > squeeze_end + 1:
            # After reset, price stabilizes with tiny noise
            price_change_pct = np.random.uniform(-0.02, 0.02)  # ±2% daily noise
        else:
            price_change_pct = np.random.normal(0, 0.01)
        price *= (1 + price_change_pct) 
        # append rounding to 2 decimals
        prices.append(round(price, 2))

        # Simulate shorts change
        if force_squeeze and day < squeeze_start:
            shorts_change_pct = np.random.uniform(-0.01, 0.01)  # flat / tiny changes pre-squeeze
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            shorts_change_pct = np.random.uniform(-0.15, -0.25) 
        elif force_squeeze and day > squeeze_end:
            shorts_change_pct = np.random.uniform(-0.02, 0.02)   # stabilize after
        else:
            shorts_change_pct = np.random.normal(0, 0.02)

        shorts *= (1 + shorts_change_pct)
        # append rounding to integer 
        shorts_array.append(round(shorts))

        # Simulate BF change
        if force_squeeze and day < squeeze_start:
            bf_change = np.random.uniform(-0.02, 0.02)   # small noise
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            bf_change = np.random.uniform(0.20, 0.40)    # strong spike
        elif force_squeeze and day > squeeze_end:
            bf_change = np.random.uniform(-0.35, -0.15)  # aggressive decay
        else:
            bf_change = np.random.normal(0.0, 0.03)

        bf *= (1 + bf_change)
        # cap BF in a realistic range
        bf = max(0.01, min(bf, 0.9))
        bf_array.append(round(bf, 3))


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
            # upward momentum building
            rsi_change = np.random.uniform(1.0, 3.0)    # RSI rising each day
        elif force_squeeze and squeeze_start <= day <= squeeze_end:
            # strong overbought pressure
            rsi_change = np.random.uniform(5.0, 12.0)
        elif force_squeeze and day > squeeze_end:
            # momentum unwinding
            rsi_change = np.random.uniform(-12.0, -5.0)
        else:
            rsi_change = np.random.normal(0.5, 1.5)

        # IMPORTANT: no division by 10 here
        rsi = max(0, min(100, rsi + rsi_change))
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
