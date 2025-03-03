# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b6dZ4tB6ADvHg7LPzTDFmMSE3vIzZHQs
"""

import io
from google.colab import files
uploaded = files.upload()

import pandas as pd
import io
df = pd.read_csv(io.BytesIO(uploaded['test.csv']))
print(df)



print(df.columns)
import numpy as np
df[' Date']= pd.to_datetime(df[' Date']) # Converts to date time format
df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')
df['Rates'] = pd.to_numeric(df['Rates'], errors='coerce')
df['Weekly_Cost'] = df['Hours'] * df['Rates']
df_filtered = df[(df['Hours'] >= 0) & (df['Rates']>= 0)].dropna() # Getting rid of the rows with negative values

df.sort_values(by=' Date', inplace=True)  #Get the dates order
df.groupby(pd.Grouper(key=' Date', freq= 'W')).sum() # Group by the weeks


df_filtered['Weeks'] = df_filtered[' Date'].dt.isocalendar().week  # Returns the week number according to the ISO 8601 calendar
df_out =(df_filtered.groupby('Weeks', as_index=False).agg(Weekly_Employee_Total=('Rates','sum'))) # Groups weeks and aggregates the column into an 'Aggregate_Total' column
df_out["Aggregate_Total"] = df_out['Weekly_Employee_Total'].rolling(window=13, min_periods=1).sum() # Aggregation on a week by week basis
print(df_out)

total_cost = df_filtered['Rates'].sum() #Gets the total cost that is utilised at the present moment
print('Total amount spent currently = £'+str(total_cost))
budget = 100000

#Now I will do a linear regression to forecast the future utilisation.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

x = np.array(df_out['Weeks']).reshape((-1,1)) #This is the independent vaiable and (-1,1) as the function expects a 2D array
y = np.array(df_out['Aggregate_Total']).reshape((-1,1)) #This is the dependent variable

model = LinearRegression() # Creates a linear regression model
model.fit(x,y) # Creates a linear regression model

future_weeks = np.array([53,54,55,56,57,58,59,60]) # Array of the desired weeks that I want forecasted for
predicted_cost= model.predict(future_weeks.reshape((-1,1))) # This predict the future costs using the regression model
print(predicted_cost)
print('Final consultant utilised amount is ' + str(predicted_cost[-1]) + ' GBP') # Forecasted final value

Variance = 100000 - predicted_cost[-1] # Checking if the project costs is within budget.
print('The variance calculated is ', Variance)
if Variance > 0  :
 print ('The total costs is within budget')
else :
 print('The project will run out of budget')

## Visual Line graph using matplotlib.pyplot
plt.figure(figsize=(10,6))
plt.plot(df_out['Weeks'], df_out['Aggregate_Total'], label='Historical Data')
plt.plot(future_weeks, predicted_cost, label='Predicted Costs', linestyle='--', marker='o')
plt.title('Historical and Predicted Aggregate Totals')
plt.xlabel('Weeks')
plt.ylabel('Aggregate Total')
plt.legend()
plt.grid(True)
plt.show()
