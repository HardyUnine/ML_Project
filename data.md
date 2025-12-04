# Data info 

SIR = Short Interest Ratio ( = SHORTS / ADV ) --> also called DTC days to cover, > 5 indicates potential short squeeze 

RSI = Relative Strength Index (RSI) (random 0–100 series; simulate up/down swings) = calculated with RS = average gain / average loss -> RSI is $100 - 1/(1+RS)$

BF = Broker Fee (Borrow Cost) (values between 0.2%–4%, random, sometimes spiking with SI)

ADV = Average Daily Volume (ADV) (simulate trading volume, with normal or log-normal distribution and shocks)

PUBLIC = Public Sentiment (Bernoulli draws for "shock" days, plus noisy sentiment score)

SS = short squeeze, this is ( for now ) determined with SIR > 60 and SHORT SQUEEZE = True --> will tweek

SHOTS = total shorts, useful for SIR calculation

PRICE_PER_SHARE = close price 

## Data and interactions for simulation

$SIR$ = Short interest ratio 

**How to calculate :** 

$SIR = SHORTS / ADV$

---

$RSI$ = Relative Strength Index 

**How to calculate :**
It is calculated with $RS$ 

$RS = average$ $gain/average$ $loss$

$RSI = 100- 100/(1+RS)$

---

$BF$ = Broker fee

**How to calculate :**
$BF = ADV*Flat$ $Fee$
# Different companies' TICKERs :

AAPL — Apple Inc.

MSFT — Microsoft Corporation

GOOG — Alphabet Inc. (Google)

AMZN — Amazon.com Inc.

NVDA — NVIDIA Corporation

META — Meta Platforms, Inc. (Facebook)

TSLA — Tesla Inc.

BRK.B — Berkshire Hathaway Inc.

JPM — JPMorgan Chase & Co.

V — Visa Inc.

TSM — Taiwan Semiconductor Manufacturing Company

BABA — Alibaba Group Holding Ltd.

NFLX — Netflix Inc.

XOM — ExxonMobil Corporation

JNJ — Johnson & Johnson

BAC — Bank of America Corporation

WMT — Walmart Inc.

AVGO — Broadcom Inc.

DIS — The Walt Disney Company

ORCL — Oracle Corporation

## data description for company_data_revised.csv



| Category                                           | Ticker Symbols                                         | Description                                                                                              |
| -------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Mostly Holds (10 companies)                        | MSFT, GOOG, META, BRK.B, V, TSM, BABA, AVGO, JPM, NFLX | Moderate Short Interest (SIR ~0.35), RSI around 55, low Borrow Fee (~0.02), higher Public Float (~0.5)   |
| Balanced (4 companies)                             | AMZN, TSLA, DIS, NFLX                                  | Moderate SIR (~0.4-0.55), RSI ~45-50, moderate Borrow Fee (~0.03-0.05), moderate Public Float (~0.3-0.4) |
| Mostly Sells (4 companies)                         | XOM, JNJ, BAC, WMT, ORCL                               | Low SIR (~0.2), high RSI (~70), low Borrow Fee (~0.01), high Public Float (~0.6)                         |
| Highly Susceptible to Short Squeezes (2 companies) | AAPL, NVDA                                             | High SIR (~0.75), low RSI (~28), high Borrow Fee (~0.08), low Public Float (~0.15)                       |



| Category                   | SIR      | RSI   | Borrow Fee (BF) | Public Float |
| -------------------------- | -------- | ----- | --------------- | ------------ |
| Mostly Holds               | ~0.35    | ~55   | ~0.02           | ~0.5         |
| Balanced                   | 0.4-0.55 | 45-50 | 0.03-0.05       | 0.3-0.4      |
| Mostly Sells               | ~0.2     | ~70   | ~0.01           | ~0.6         |
| Highly Susceptible Squeeze | ~0.75    | ~28   | ~0.08           | ~0.15        |





--- 


## NEW DATA IN PLAN B -> 20 csvs
10 = short squeezes 
10 = shorts but no squeezes

### Short Squeeze csvs : 
AMC, BB, BYND, FUBO, GME, KOSS, NOK, PLTR, RIOT, TLRY

### SHORT csvs :
TSLA, AAPL, MSFT, GOOGL, AMZN, META, NFLX, NVDA, INTC, AMD

