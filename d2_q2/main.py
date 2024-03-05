import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
hdb_resale_prices = pd.read_csv('datasets/hdb_resale_prices.csv')

"""
Month	Town	Flat type	Block	Street name	Storey range	Floor area sqm	Flat model	Lease commence date	Remaining lease	Resale price
2017-01	ANG MO KIO	2 ROOM	406	ANG MO KIO AVE 10	10 TO 12	44	Improved	1979	61 years 04 months	232000
......
"""

# For each town, find the median flat price in 2022. Plot a bar chart to illustrate the median flat price for each town.

# Step 1: Filter the data for 2022
hdb_resale_prices_2022 = hdb_resale_prices[hdb_resale_prices['month'].str.contains('2022')]
# Step 2: Group the data by town and calculate the median price
median_prices_2022 = hdb_resale_prices_2022.groupby('town')['resale_price'].median()

print(median_prices_2022)

# Step 3: Plot the bar chart
median_prices_2022.plot(kind='bar')
plt.title('Median flat price in 2022')
plt.xlabel('Town')
plt.ylabel('Median price')
plt.show()

print('\n')

# For each town, find the median flat price in 2017.  Which are the top 3 towns with the greatest change in median flat prices from 2017 to 2022?
# Step 1: Filter the data for 2017
hdb_resale_prices_2017 = hdb_resale_prices[hdb_resale_prices['month'].str.contains('2017')]
# Step 2: Group the data by town and calculate the median price
median_prices_2017 = hdb_resale_prices_2017.groupby('town')['resale_price'].median()
# Step 3: Calculate the change in median prices from 2017 to 2022
change_in_median_prices = median_prices_2022 - median_prices_2017
# Step 4: Sort the change in median prices and display the top 3 towns
top_3_towns = change_in_median_prices.sort_values(ascending=False).head(3)
print('Towns with the greatest change in median flat prices from 2017 to 2022:')
print(top_3_towns)

# plot the changes in median prices over the years
hdb_resale_prices['year'] = hdb_resale_prices['month'].str[:4]
median_prices_over_years = hdb_resale_prices.groupby(['town', 'year'])['resale_price'].median().unstack().sample(5)

# swap the rows and columns
median_prices_over_years = median_prices_over_years.T

median_prices_over_years.plot(kind='line', marker='o')
plt.title('Median flat price over the years')
plt.xlabel('Year')
plt.ylabel('Median price')
plt.show()
