import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#load dataset
df=pd.read_csv('adult.csv')
# Display the first few rows of the dataset
print('The dataset displays the following info:\n',df.info())
print('The first few rows of the dataset are given below:\n',df.head())
# Check for missing values
print('The number of missing values in each column are:\n',df.isnull().sum())
#drop rows with ? in native-country column
df = df[df['native.country'] != '?']
#Drop ? values in 'workclass' column
df = df[df['workclass'] != '?']
print('The updated dataset after dropping rows with ? in workclass column is:\n', df.head(10))
# check unique values in 'income' column
print('The unique values in the income column are:\n', df['income'].unique())
#check minimum and maximum age in the dataset
min_age = df['age'].min()
max_age = df['age'].max()

#Provide age range
print(f'The minimum age in the dataset is {min_age} and the maximum age is {max_age}.')
bins = [17,21,31,41,51,61,81,91]
labels = ['17-20', '21-30', '31-40', '41-50', '51-60', '61-80', '81-90']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
print('The first few rows after binning the age column are:\n', df.head(10))
# Convert 'income' column to binary values
df['income'] = df['income'].apply(lambda x: 1 if x == '>50K' else 0)
# Display the first few rows after conversion
print('The first few rows after converting income column to binary values are:\n', df.head(10))

#to check  average income by age
average_income_by_age = df.groupby('age_group')['income'].mean().reset_index()
average_income_by_age.columns = ['age_group', 'average_income_proportion']
print('The average income by age is:\n', average_income_by_age.head(10))
# Plotting the average income by age group
plt.figure(figsize=(10,6))
sns.barplot(x='age_group', y='average_income_proportion', data=average_income_by_age, palette='viridis')
plt.title('Average Income by Age Group', fontsize=16)
plt.xlabel('Age Group', fontsize=14)
plt.ylabel('Average Income (0 = <=50K, 1 = >50K)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#check for average income by education
average_income_by_education = df.groupby('education')['income'].mean().reset_index()
average_income_by_education.columns = ['education', 'average_income_proportion']
print('The average income by education is:\n', average_income_by_education.head(10))
# Plotting the average income by education
plt.figure(figsize=(12,6))
sns.barplot(x='education', y='average_income_proportion', data=average_income_by_education, palette='plasma')
plt.title('Average Income by Education Level', fontsize=16)
plt.xlabel('Education Level', fontsize=14)
plt.ylabel('Average Income (0 = <=50K, 1 = >50K)', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# checking average income by gender
average_income_by_gender = df.groupby('sex')['income'].mean().reset_index()
average_income_by_gender.columns = ['gender', 'average_income_proportion']
print('Average income by gender:\n', average_income_by_gender)
# Plotting average income by gender
plt.figure(figsize=(6,6))
plt.pie(average_income_by_gender['average_income_proportion'], 
        labels=average_income_by_gender['gender'], 
        autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Proportion of High Earners by Gender')
plt.show()

# checking average income by marital status
average_income_by_marital = df.groupby('marital.status')['income'].mean().reset_index()
average_income_by_marital.columns = ['marital.status', 'average_income_proportion']
print('Average income by marital status:\n', average_income_by_marital)
# Plotting average income by marital status
plt.figure(figsize=(12,6))
sns.barplot(x='marital.status', y='average_income_proportion', data=average_income_by_marital, palette='mako')
plt.title('Average Income by Marital Status', fontsize=16)
plt.xlabel('Marital Status', fontsize=14)
plt.ylabel('Proportion Earning >50K', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# Define bins for hours-per-week
bins = [0, 20, 35, 40, 50, 60, 100]
labels = ['<20', '21-35', '36-40', '41-50', '51-60', '60+']
df['work_hours_group'] = pd.cut(df['hours.per.week'], bins=bins, labels=labels, right=False)

# checking average income by work hours group
average_income_by_hours = df.groupby('work_hours_group')['income'].mean().reset_index()
average_income_by_hours.columns = ['work_hours_group', 'average_income_proportion']
print('Average income by work hours:\n', average_income_by_hours)
# Plotting average income by work hours
plt.figure(figsize=(10,6))
sns.barplot(x='work_hours_group', y='average_income_proportion', data=average_income_by_hours, palette='husl')
plt.title('Average Income by Weekly Work Hours', fontsize=16)
plt.xlabel('Work Hours per Week', fontsize=14)
plt.ylabel('Proportion Earning >50K', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
