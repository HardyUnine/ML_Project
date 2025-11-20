import numpy as np
import pandas as pd


class Person:
    def __init__(self, id, group):
        self.id = id
        self.group = group

    def decide(self, company_state, weights, thresholds):
        RSI = company_state['RSI'] / 100
        BF = company_state['BF'] / 0.05
        ADV = company_state['ADV'] / company_state['TOTAL_SHARES']
        D = (weights['SIR'] * company_state['SIR'] +
             weights['RSI'] * RSI +
             weights['BF'] * BF +
             weights['ADV'] * ADV +
             weights['PUBLIC'] * company_state['PUBLIC'])
        if D < thresholds[0]:
            return -1  # Sell
        elif D > thresholds[1]:
            return 1   # Buy
        else:
            return 0   # Hold
        

def assign_shares(total_shares, N):
    weights = np.random.rand(N)
    weights /= weights.sum()
    shares = (weights * total_shares).astype(int)
    diff = total_shares - shares.sum()
    for i in range(diff):
        shares[i % N] += 1
    return shares


def update_company_state(company_state, net_buy_volume, day, squeeze_start, squeeze_end):
    # Price dynamics
    if squeeze_start <= day <= squeeze_end:
        # Sharp price increase during squeeze
        price_change_pct = 0.15 * net_buy_volume / company_state['TOTAL_SHARES']
    elif day < squeeze_start:
        # Slow price change before squeeze (small positive or negative)
        price_change_pct = 0.01 * net_buy_volume / company_state['TOTAL_SHARES']
    elif day > squeeze_end:
        # Slight price decrease after squeeze
        price_change_pct = -0.05 * net_buy_volume / company_state['TOTAL_SHARES']
    else:
        # No squeeze case: very mild stable price changes
        price_change_pct = 0.001 * net_buy_volume / company_state['TOTAL_SHARES']

    new_price = company_state['PRICE_PER_SHARE'] * (1 + price_change_pct)
    company_state['PRICE_PER_SHARE'] = max(round(new_price, 2), 0.01)

    # RSI changes: more reactive during squeeze, minimal otherwise
    if squeeze_start <= day <= squeeze_end:
        rsi_change = price_change_pct * 30 + np.random.normal(0, 1)
    elif day < squeeze_start:
        rsi_change = price_change_pct * 10 + np.random.normal(0, 0.5)
    else:
        rsi_change = price_change_pct * 40 + np.random.normal(0, 0.2)
    company_state['RSI'] = np.clip(round(company_state['RSI'] + rsi_change, 2), 0, 100)
    # Borrow fee (BF) changes: increases during squeeze, slowly decreases or stable no squeeze
    if squeeze_start <= day <= squeeze_end:
        bf_change = 0.005 * max(net_buy_volume, 0) / company_state['TOTAL_SHARES']
        company_state['BF'] = np.clip(round(company_state['BF'] + bf_change, 4), 0, 0.5)
    else:
        # Slowly revert to a baseline BF (e.g., 0.1)
        bf_diff = 0.1 - company_state['BF']
        bf_change = 0.001 * bf_diff
        company_state['BF'] = np.clip(round(company_state['BF'] + bf_change, 4), 0, 0.5)

    # ADV changes: increases during squeeze, reverts minimally otherwise
    if squeeze_start <= day <= squeeze_end:
        adv_change = 150000 * abs(net_buy_volume) / company_state['TOTAL_SHARES']
        company_state['ADV'] = min(round(company_state['ADV'] + adv_change), company_state['TOTAL_SHARES'])
    else:
        adv_diff = 5000000 - company_state['ADV']  # assume baseline ADV around 5 million
        adv_change = 0.01 * adv_diff  # slow reversion
        company_state['ADV'] = int(company_state['ADV'] + adv_change)

    # SIR changes: builds during squeeze, slowly cools off otherwise
    if squeeze_start <= day <= squeeze_end:
        company_state['SIR'] = min(round(company_state['SIR'] + 2), 150)
    else:
        company_state['SIR'] = max(round(company_state['SIR'] - 0.1), 110)  # slow decrease

    return company_state



def simulate_days(seed_row, days=30, N_agents=100, force_squeeze=False,
                  squeeze_start_range=(4,7), squeeze_end_range=(18,22)):
    
    groups_params = {
        'risky':    ({'SIR': 0.4, 'RSI': 0.35, 'BF': 0.1,  'ADV': 0.15, 'PUBLIC': 0.4}, (-0.5, 0.05)),
        'neutral':  ({'SIR': 0.3, 'RSI': 0.25, 'BF': 0.15, 'ADV': 0.1,  'PUBLIC': 0.3}, (-0.3, 0.1)),
        'scared':   ({'SIR': 0.2, 'RSI': 0.15, 'BF': 0.3,  'ADV': 0.2,  'PUBLIC': 0.3}, (0.0, 0.4))
    }
    
    current_state = seed_row.copy()
    current_state['DAY'] = 0
    current_state['SS'] = 0
    history = [current_state.copy()]
    
    # Randomly select squeeze period within given ranges if forced
    if force_squeeze:
        squeeze_start = np.random.randint(squeeze_start_range[0], squeeze_start_range[1] + 1)
        squeeze_end = np.random.randint(squeeze_end_range[0], squeeze_end_range[1] + 1)
    else:
        # No squeeze days included when force_squeeze is False
        squeeze_start, squeeze_end = days + 1, days + 1

    for day in range(1, days + 1):
        if force_squeeze and squeeze_start <= day <= squeeze_end:
            group_probs = [1.0, 0.0, 0.0]  # force all agents to be risky buyers
            force_decision = 1  # force buy
        else:
            # Normal randomized group probabilities
            group_probs = [0.33, 0.34, 0.33]
            force_decision = None
        
        groups_sampled = np.random.choice(['risky', 'neutral', 'scared'], size=N_agents, p=group_probs)
        persons = [Person(i, grp) for i, grp in enumerate(groups_sampled)]
        shares_per_person = assign_shares(current_state['TOTAL_SHARES'], N_agents)
        
        net_buy_volume = 0
        for i, p in enumerate(persons):
            weights, thresholds = groups_params[p.group]
            if force_decision is not None:
                decision = force_decision
            else:
                decision = p.decide(current_state, weights, thresholds)
            net_buy_volume += decision * shares_per_person[i]
        
        # Add a small baseline buy volume (mild normal trading activity)
        net_buy_volume += 0.005 * current_state['TOTAL_SHARES']
        
        current_state = update_company_state(current_state, net_buy_volume, day, squeeze_start, squeeze_end)
        current_state['DAY'] = day
        # Label SS only if RSI > 60 during squeeze period and force_squeeze is on
        current_state['SS'] = 1 if (force_squeeze and current_state['RSI'] > 60 and squeeze_start <= day <= squeeze_end) else 0
        
        history.append(current_state.copy())

    print(f"Squeeze period: Day {squeeze_start} to Day {squeeze_end}")
    return pd.DataFrame(history)
