# Idea
## Step 1
Initial csv -> company_data.csv 
is only one line for now -> day 1 with DAY,SIR,RSI,BF,ADV,PUBLIC

## Step 2 
Define Class Person:
3 sub classes : 
    - risky
    - scared
    - neutral
with 3 defined decision making based on previous information ( company_data.csv )

*Decision making functions:* we will calculate a decision score formula with different weights for each investor category and threshold. Before applying these weights, we will scale each input so they are comparable. 
The decision score is defined as: 
D = wSIR * SIR + wRSI * RSI + wBF * -BF + wADV * ADV + wPS * PS

**Risk-seeking investor weights**
- wSIR = 0.3, want a high SIR, think a squeete is profitable
- wRSI = 0.25, want momentum, high RSI means increased bying tendency
- wBF = 0.05 low sensitivity to borrow cost, a sacrifice for big earnings
- wPI = 0.3 follow the hype so high importance of public sentiment
- wADV= 0.1, prefence for liquidity bit will trade with mid low adv too doesn't matter much
Thresholds: T1 = -0.25, T2 = +0.10

**Moderate traders weights**
- wSIR = 0.25
- wRSI = 0.02
- wBF = 0.15
- wPI = 0.3
- wADV ? = 0.1
Thresholds: T1 = -0.10, T2 = +0.25 

**Conservative investors weights**
- wSIR = 0.1, less interested by high sri, seen as more risky
- wRSI = 0.05
- wBF = 0.3, high sensitivity to borrow fee, costs deter them
- wPI = 0.35, strong reaction do sentiment, especially negative
- wADV = 0.2, prefer high liquidity
Thresholds: T1 = +0.05, T2 = +0.45

## Step 3
output to decisions.csv -> ID, GROUP, DECISION with ID being the person itself, GROUP being risky scared or neutral, and DECISION being 0, -1, 1 --> -1 being sell, 0 being nothing, 1 being buy 

## Step 4
Calculate change in company_data.csv based on the decisions from decisions.csv

## Step 5 
Loop step 3 - 4 until 14 days are completed 




#### PROBLEM


--> we are trying to predict a short squeeze, so we should be initialising the data as a short already and then seeing why/how short squeezes happen FROM ALREADY SHORTING, not from neutral

## Solution ? 
 
we simulate data that are in the fork of what can be considered a moment of short 