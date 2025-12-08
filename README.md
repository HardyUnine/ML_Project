# Can we develop a predictive model to assess the
likelihood of a stock experiencing a short
squeeze within the next 5 to 10 trading days?

## Overview

This project implements a classification model to predict short squeeze events using historical stock market indicators. We combine real market data from January-February 2021 with simulated datasets to train and evaluate machine learning models.

## Key Features

- Real Data Collection: Automated scraping of OHLCV data, short interest metrics, and borrow fees from Yahoo Finance and Finviz
- Discrete-Event Simulation: Custom simulator modeling stock price, shorts covering, RSI evolution, and borrow fee dynamics
- Model Evaluation: Comparative analysis of LightGBM and Random Forest classifiers with comprehensive metrics
- Data Visualization: Side-by-side comparison of real vs. simulated data across multiple indicators

## Dataset

- Time Period: January 4 - February 16, 2021
- Ticker: GME (GameStop Corp.)
- Squeeze Window: January 22 - February 1, 2021 (labeled as SS=1)
- Features: PRICE_PER_SHARE, SHORTS, SIR, RSI, BF, ADV

## Installation

Prerequisites: Python 3.8+, pip

Setup:

git clone https://github.com/HardyUnine/ML_Project.git
cd ML_Project
pip install -r requirements.txt

## Authors

Hardy Keenan and Andreadi Angeliki

## License

Educational purposes only.

## Disclaimer

For educational and research purposes only. Not financial advice.
