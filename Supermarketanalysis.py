import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#  Load the Dataset
df = pd.read_csv('SuperMarket Analysis.csv')
print(' DATA LOADED SUCCESSFULLY\n')

#  BASIC DATA CLEANING
# Strip column names and string values
df.columns = df.columns.str.strip()
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()
# Remove duplicate rows
df.drop_duplicates(inplace=True)
#  Display Basic Info
print(' BASIC INFORMATION:')
print(df.info(), "\n")
print(' FIRST 5 ROWS IN THE DATASET:')
print(df.head(), "\n")
# Check for Missing Values
print('CHECKING FOR MISSING VALUES:')
missing = df.isnull().sum()
print(missing)
if missing.sum() == 0:
    print(' NO NULL VALUES IN THE DATASET\n')
else:
    print(' Null values detected! Please review.\n')


#  BAR PLOT FOR TOTAL SALES BY PRODUCT LINE
# Unique Product Lines
print("PRODUCT LINES INCLUDE:\n")
for line in df['Product line'].unique():
    print(f"• {line}")
# Grouping
sales_by_product = df.groupby('Product line')['Sales'].sum().sort_values()
print('\n TOTAL SALES BY PRODUCT LINE:\n', sales_by_product, "\n")

plt.figure(figsize=(10,6))
sns.barplot(x=sales_by_product.values, y=sales_by_product.index, palette="viridis")
plt.title('Total Sales by Product Line', fontsize=16)
plt.xlabel('Total Sales')
plt.ylabel('Product Line')
plt.grid(axis='x', linestyle='--', alpha=1)
plt.tight_layout()
plt.show()

#  BAR PLOT FOR TOTAL SALES BY CITY
# Unique Cities
print("\n CITIES IN THE DATASET:\n")
for city in df['City'].unique():
    print(f"• {city}")
#  Total Sales by City
sales_by_city = df.groupby('City')['Sales'].sum().sort_values()
print('\n TOTAL SALES BY CITY:\n', sales_by_city, "\n")

plt.figure(figsize=(10,6))
sns.barplot(x=sales_by_city.values, y=sales_by_city.index, palette="dark")
plt.title('Total Sales by City', fontsize=16)
plt.xlabel('Total Sales')
plt.ylabel('City')
plt.grid(axis='x', linestyle='--', alpha=1)
plt.tight_layout()
plt.show()

#  BAR PLOT FOR SALES BY GENDER
#  Genders in the Dataset
print("\n GENDERS IN THE DATASET:\n")
for gender in df['Gender'].unique():
    print(f"• {gender}")
#  Sales by Gender
sales_by_gender = df.groupby('Gender')['Sales'].sum().sort_values()
print('\n TOTAL SALES BY GENDER:\n', sales_by_gender, "\n")

plt.figure(figsize=(10,6))
sns.barplot(x=sales_by_gender.values, y=sales_by_gender.index, palette="mako")
plt.title('Total Sales by Gender', fontsize=16)
plt.xlabel('Total Sales')
plt.ylabel('Gender')
plt.grid(axis='x', linestyle='--', alpha=1)
plt.tight_layout()
plt.show()
