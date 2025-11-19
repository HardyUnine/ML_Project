import numpy as np
import pandas as pd

def simulate_days(seed_row, days=30, N_agents=100):
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

    def update_company_state(company_state, net_buy_volume, day):
        squeeze_start, squeeze_end = 7, 24

        # Amplified impact of net buy volume on price
        price_change_pct = 0.05 * net_buy_volume / company_state['TOTAL_SHARES']
        company_state['PRICE_PER_SHARE'] *= (1 + price_change_pct)

        # RSI highly sensitive to price movement plus random noise
        company_state['RSI'] = np.clip(
            company_state['RSI'] + price_change_pct * 300 + np.random.normal(0, 1), 0, 100)

        # Borrow fee increases with positive buy volume, capped at 50%
        bf_change = 0.005 * max(net_buy_volume, 0) / company_state['TOTAL_SHARES']
        company_state['BF'] = np.clip(company_state['BF'] + bf_change, 0, 0.5)

        # ADV surges with trading volume magnitude
        adv_change = 200000 * abs(net_buy_volume) / company_state['TOTAL_SHARES']
        company_state['ADV'] = max(company_state['ADV'] + adv_change, 0)

        # Short interest ratio increases during squeeze, decreases afterward
        if squeeze_start <= day <= squeeze_end:
            company_state['SIR'] = min(company_state['SIR'] + 3, 150)
        elif day > squeeze_end:
            company_state['SIR'] = max(company_state['SIR'] - 2, 110)

        return company_state

    # Stronger weights for risky agents to emphasize buy decisions during squeeze
    groups_params = {
        'risky':    ({'SIR': 0.6, 'RSI': 0.5, 'BF': 0.2, 'ADV': 0.2, 'PUBLIC': 0.4}, (-0.6, 0.0)),
        'neutral':  ({'SIR': 0.4, 'RSI': 0.3, 'BF': 0.15, 'ADV': 0.1, 'PUBLIC': 0.3}, (-0.3, 0.15)),
        'scared':   ({'SIR': 0.2, 'RSI': 0.1, 'BF': 0.4, 'ADV': 0.25, 'PUBLIC': 0.3}, (0.1, 0.5))
    }


    current_state = seed_row.copy()
    current_state['DAY'] = 0
    current_state['SS'] = 0
    history = [current_state.copy()]

    for day in range(1, days + 1):
        # Bias agents towards risky buyers during squeeze window to ensure buy pressure
        if 7 <= day <= 24:
            group_probs = [0.9, 0.05, 0.05]  # Mostly risky buyers during squeeze
        else:
            group_probs = [0.33, 0.34, 0.33]  # Balanced groups otherwise

        groups_sampled = np.random.choice(['risky', 'neutral', 'scared'], size=N_agents, p=group_probs)
        persons = [Person(i, grp) for i, grp in enumerate(groups_sampled)]
        shares_per_person = assign_shares(current_state['TOTAL_SHARES'], N_agents)

        net_buy_volume = 0
        for i, p in enumerate(persons):
            weights, thresholds = groups_params[p.group]
            decision = p.decide(current_state, weights, thresholds)
            net_buy_volume += decision * shares_per_person[i]

        # Inject a baseline positive buy pressure during squeeze window to guarantee price movement
        if 7 <= day <= 24:
            net_buy_volume += 0.01 * current_state['TOTAL_SHARES']

        current_state = update_company_state(current_state, net_buy_volume, day)
        current_state['DAY'] = day

        # Mark short squeeze when RSI > 60 during squeeze days
        current_state['SS'] = 1 if (current_state['RSI'] > 60 and 7 <= day <= 24) else 0

        history.append(current_state.copy())

    return pd.DataFrame(history)
