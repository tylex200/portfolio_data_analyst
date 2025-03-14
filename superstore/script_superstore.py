import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter
import seaborn as sns

# Load the dataset
file_path = "superstore/superstore1.csv"
df = pd.read_csv(file_path, encoding_errors='ignore')

# Convert date columns to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Check for missing values
print(df.isnull().sum())

# Ensure numeric columns are properly formatted
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# Function to format y-axis as currency without decimals
def currency_format(x, _):
    return f'${x:,.0f}'  # Elimina los decimales

formatter = FuncFormatter(currency_format)

# Aggregate sales by month
df['Year-Month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('Year-Month')['Sales'].sum()

# Plot the trend
plt.figure(figsize=(12,6))
monthly_sales.plot(kind='line', marker='o', color='b')
plt.title('Sales Trends Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Total Sales')

# Apply currency format
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)
plt.show()

# Aggregate sales by customer segment
segment_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)

# Plot the segmentation
plt.figure(figsize=(8,5))
sns.barplot(x=segment_sales.index, y=segment_sales.values, palette="Blues_r")
plt.title('Sales by Customer Segment')
plt.xlabel('Customer Segment')
plt.ylabel('Total Sales')

# Apply currency format
plt.gca().yaxis.set_major_formatter(formatter)

plt.show()

# Scatter plot of discount vs. profit
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df['Discount'], y=df['Profit'], alpha=0.5)
plt.title('Impact of Discount on Profit')
plt.xlabel('Discount')
plt.ylabel('Profit')

# Format x-axis as percentages and y-axis as currency
plt.gca().xaxis.set_major_formatter(PercentFormatter(1.0))  # 1.0 means 100%
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)
plt.show()

# Print summary statistics
print(df[['Discount', 'Profit']].describe())

