import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('datasets/grad_pay.csv')

"""
year,university,school,degree,employment_rate_overall,employment_rate_ft_perm,basic_monthly_mean,basic_monthly_median,gross_monthly_mean,gross_monthly_median,gross_mthly_25_percentile,gross_mthly_75_percentile
2013,Nanyang Technological University,College of Business (Nanyang Business School),Accountancy and Business,97.4,96.1,3701,3200,3727,3350,2900,4000
......
"""

# get the top 3 degrees with the most increase in pay from 2013 to 2021
# calculate the increase in pay for each degree

# get the data for 2013 and 2021
data_2013 = data[data['year'] == 2013]
data_2021 = data[data['year'] == 2021]
degrees = data_2013['degree'].unique()

# calculate the increase in pay for each degree
increase = []
for degree in degrees:
		# check if the degree is present in both 2013 and 2021
		if degree in data_2013['degree'].values and degree in data_2021['degree'].values:
				# get the data for the degree in 2013 and 2021
				degree_data_2013 = data_2013[data_2013['degree'] == degree]
				degree_data_2021 = data_2021[data_2021['degree'] == degree]
				# calculate the increase in pay
				# increase.append((degree, int(degree_data_2021['gross_monthly_median'].values[0]) - int(degree_data_2013['gross_monthly_median'].values[0])))
				# calculate the percentage increase in pay
				increase.append((degree, (int(degree_data_2021['gross_monthly_median'].values[0]) - int(degree_data_2013['gross_monthly_median'].values[0]))/int(degree_data_2013['gross_monthly_median'].values[0])*100))

# sort the increase in pay
increase = sorted(increase, key=lambda x: x[1], reverse=True)

# get the top 3 degrees with the most increase in pay from 2013 to 2021
top_3 = increase[:3]

# plot the increase in pay for the top 3 degrees
degrees = [x[0] for x in top_3]
increase_pct = [x[1] for x in top_3]
plt.bar(degrees, increase_pct)
plt.xlabel('Degree')
plt.ylabel('Percentage Increase in Pay')
plt.title('Top 3 Degrees with the Most Increase in Pay from 2013 to 2021')

plt.show()

# get the 3 degrees with the least increase in pay from 2013 to 2021
bottom_3 = increase[-3:]

# plot the increase in pay for the bottom 3 degrees
degrees = [x[0] for x in bottom_3]
increase_pct = [x[1] for x in bottom_3]
plt.bar(degrees, increase_pct)
plt.xlabel('Degree')
plt.ylabel('Percentage Increase in Pay')
plt.title('Bottom 3 Degrees with the Least Increase in Pay from 2013 to 2021')

plt.show()

# Plot the 2013 to 2021 pay for the top 1 degree in NUS with highest & lowest % change in pay
# get the data for the top 1 degree with the highest % change in pay
degree = top_3[0][0]
degree_data_2013 = data_2013[data_2013['degree'] == degree]
degree_data_2021 = data_2021[data_2021['degree'] == degree]

degree1 = increase[-1][0]
degree_data1_2013 = data_2013[data_2013['degree'] == degree1]
degree_data1_2021 = data_2021[data_2021['degree'] == degree1]

# plot the 2013 to 2021 pay for the top 1 degree with the highest % change in pay
years = [2013, 2021]
pay = [int(degree_data_2013['gross_monthly_median'].values[0]), int(degree_data_2021['gross_monthly_median'].values[0])]
pay1 = [int(degree_data1_2013['gross_monthly_median'].values[0]), int(degree_data1_2021['gross_monthly_median'].values[0])]
plt.plot(years, pay, marker='o')
plt.plot(years, pay1, marker='o')
plt.xlabel('Year')
plt.ylabel('Gross Monthly Median Pay')
plt.title('2013 to 2021 Pay for the Top 1 Degree with the Highest % Change in Pay')

plt.show()

# Plot the MAS core inflation index from 2013 to 2021
# Load the data
inflation = pd.read_csv('datasets/cpi.csv')

"""
Data Series,All Items (Index),All Items -> Food (Index),All Items -> Food Excl Food Serving Services (Index),All Items -> Food Excl Food Serving Services -> Bread & Cereals (Index),All Items -> Food Excl Food Serving Services -> Meat (Index),All Items -> Food Excl Food Serving Services -> Fish & Seafood (Index),"All Items -> Food Excl Food Serving Services -> Milk, Cheese & Eggs (Index)",All Items -> Food Excl Food Serving Services -> Oils & Fats (Index),All Items -> Food Excl Food Serving Services -> Fruits (Index),All Items -> Food Excl Food Serving Services -> Vegetables (Index),"All Items -> Food Excl Food Serving Services -> Sugar, Preserves & Confectionery (Index)",All Items -> Food Excl Food Serving Services -> Non-Alcoholic Beverages (Index),All Items -> Food Excl Food Serving Services -> Other Food (Index),All Items -> Food Serving Services (Index),All Items -> Food Serving Services -> Restaurant Food (Index),All Items -> Food Serving Services -> Fast Food (Index),All Items -> Food Serving Services -> Hawker Food (Index),All Items -> Food Serving Services -> Catered Food (Index),All Items -> Clothing & Footwear (Index),All Items -> Clothing & Footwear -> Clothing (Index),All Items -> Clothing & Footwear -> Other Articles & Related Services (Index),All Items -> Clothing & Footwear -> Footwear (Index),All Items -> Housing & Utilities (Index),All Items -> Housing & Utilities -> Accommodation (Index),All Items -> Housing & Utilities -> Utilities & Other Fuels (Index),All Items -> Household Durables & Services (Index),All Items -> Household Durables & Services -> Household Durables (Index),All Items -> Household Durables & Services -> Household Services & Supplies (Index),All Items -> Health Care (Index),All Items -> Health Care -> Medicines & Health Products (Index),All Items -> Health Care -> Outpatient Services (Index),All Items -> Health Care -> Hospital Services (Index),All Items -> Health Care -> Health Insurance (Index),All Items -> Transport (Index),All Items -> Transport -> Private Transport (Index),All Items -> Transport -> Public Transport (Index),All Items -> Transport -> Other Transport Services (Index),All Items -> Communication (Index),All Items -> Communication -> Postage & Courier Services (Index),All Items -> Communication -> Telecommunication Equipment (Index),All Items -> Communication -> Telecommunication Services (Index),All Items -> Recreation & Culture (Index),All Items -> Recreation & Culture -> Recreational & Cultural Goods (Index),All Items -> Recreation & Culture -> Recreational & Cultural Services (Index),"All Items -> Recreation & Culture -> Newspapers, Books & Stationery (Index)",All Items -> Recreation & Culture -> Holiday Expenses (Index),All Items -> Education (Index),All Items -> Education -> Tuition & Other Fees (Index),All Items -> Education -> Textbooks & Study Guides (Index),All Items -> Miscellaneous Goods & Services (Index),All Items -> Miscellaneous Goods & Services -> Personal Care (Index),All Items -> Miscellaneous Goods & Services -> Alcoholic Drinks & Tobacco (Index),All Items -> Miscellaneous Goods & Services -> Personal Effects (Index),All Items -> Miscellaneous Goods & Services -> Social Services (Index),All Items -> Miscellaneous Goods & Services -> Other Miscellaneous Services (Index),All Items Less Imputed Rentals On Owner-Occupied Accommodation (Index),All Items Less Accommodation (Index)
  2013 Jan,98.1,88.5,89.3,91.9,94.2,84.7,87.6,97.1,82.1,89.3,95.2,94.2,90.7,88,87.4,89.7,88.2,90.4,99.2,100.4,96.5,95.7,111.9,113.2,103.4,91.7,100.2,87.8,89.2,99.1,92.4,80.8,89,104.6,106.3,96.8,100.5,101.9,91.9,117.5,101.3,94,103.8,91.9,92.3,92.1,82.3,82,96.6,97,101,87.9,98.2,na,na,94.5,94.3
	......
"""

inflation = inflation.astype(str)

# remove first column
inflation = inflation.iloc[:, 1:]

# get first row
years = inflation.columns

# get 2nd row
inflation_index = inflation.iloc[0, :]

# plot the MAS core inflation index from 2013 to 2021
plt.plot(years, inflation_index, marker='o')
plt.xlabel('Year')
plt.ylabel('MAS Core Inflation Index')
plt.title('MAS Core Inflation Index from 2013 to 2021')

plt.show()
