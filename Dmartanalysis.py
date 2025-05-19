import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Loading the CSV file
df= pd.read_csv('DMart.csv')
print('The given dataset has been successfully loaded!')
#column names
print('The column names are as follows:\n',df.columns)
#Display the datatypes of the given columns
print('The data types of the given columns are as follows:\n',df.dtypes)
#Display first 5 rows of the dataset
print('The first 5 rows are as follows:\n',df.head())
#Display high price and low price itmes
high_price = df[df['Price'] > 1000]
print('The first 5 items with price greater than 1000 are as follows:\n',high_price.head())
low_quantity = df[df['Price'] < 1000]
print('The first 5 items with price less than 1000 are as follows:\n',low_quantity.head())
#Compare Price
highest_price = df['Price'].max()
print('The highest price is:',highest_price)
lowest_price = df['Price'].min()
print('The lowest price is:',lowest_price)
#Group by Category
category_items = df.groupby('Category')['Price'].max()
print("Items under each category and their highest prices:\n", category_items.head())
