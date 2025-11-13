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