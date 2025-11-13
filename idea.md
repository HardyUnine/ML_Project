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


## stuff todo

number of stock  --> LLM
number of individuals --> 100 for now 

# idea for csv 

company_data.csv one line per company 

the final csv would be one csv per company over 14 days 
we would have n csvs, n being the number of. companies --> maybe 20 different companies 

# problem and solution for market shares 
On assigne chaque individu une part du marché random :
marché = 1'000'000 shares 
1 indivdual has 25 shares, other has 250'000 
the sum of all individuals shares come to 1'000'000

for the +1, -1, 0 --> we do a weighted multiplier depending on how much each value is 

SIR = 40 for example 
Risky person buys if SIR > 30 
SIR = 40, miniimum = 30 --> weight is 40-30 = 10 

This person has 1'000 shares, so with this weight, we do some kind of formula --> that takes into account the difference in the minimum they would sell at and the real value