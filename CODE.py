import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("C:/Users/HP/OneDrive/Desktop/DATA SCIENCE PYTHON PROJECT/sales_data_sample.csv", encoding="latin1")

# Convert ORDERDATE to datetime
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

# Preprocessing
df['YearMonth'] = df['ORDERDATE'].dt.to_period('M')
df['Year'] = df['ORDERDATE'].dt.year
df['Month'] = df['ORDERDATE'].dt.month

# -------------------------------------------
# 1. Sales Trend Analysis (Revenue & Volume)
# -------------------------------------------
monthly_data = df.groupby('YearMonth').agg({
    'SALES': 'sum',
    'ORDERNUMBER': pd.Series.nunique
}).rename(columns={'SALES': 'Total Revenue', 'ORDERNUMBER': 'Unique Orders'}).to_timestamp()

# Plot revenue and volume trends
plt.figure(figsize=(14, 5))
plt.plot(monthly_data.index, monthly_data['Total Revenue'], label='Revenue ($)', marker='o')
plt.plot(monthly_data.index, monthly_data['Unique Orders'], label='Order Volume', marker='s')
plt.title("Monthly Sales Trend")
plt.xlabel("Date")
plt.ylabel("Amount")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()

# -------------------------------------------
# 2. Product Performance Assessment
# -------------------------------------------
product_sales = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values()
product_sales.plot(kind='barh', figsize=(10, 6), color='skyblue')
plt.title("Revenue by Product Line")
plt.xlabel("Revenue ($)")
plt.ylabel("Product Line")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 3. Geographical Sales Insights
# -------------------------------------------
top_countries = df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False).head(10)
top_countries.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8), startangle=140)
plt.title("Top 10 Countries by Sales")
plt.ylabel("")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 4. Customer Segmentation
# -------------------------------------------
customer_total = df.groupby('CUSTOMERNAME')['SALES'].sum()
segments = pd.qcut(customer_total, 4, labels=["Low", "Mid", "High", "Top"])
segment_distribution = segments.value_counts().sort_index()
segment_distribution.plot(kind='bar', color='coral', figsize=(8, 5))
plt.title("Customer Segmentation by Revenue")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 5. Profitability Analysis
# -------------------------------------------
# Approximate cost: 70% of priceEach * quantity
df['COST'] = df['PRICEEACH'] * df['QUANTITYORDERED'] * 0.7
df['PROFIT'] = df['SALES'] - df['COST']

# Profit by product line
profit_by_product = df.groupby('PRODUCTLINE')['PROFIT'].sum().sort_values()
profit_by_product.plot(kind='barh', figsize=(10, 6), color='green')
plt.title("Profit by Product Line")
plt.xlabel("Profit ($)")
plt.ylabel("Product Line")
plt.tight_layout()
plt.show()

# Profit by country
profit_by_country = df.groupby('COUNTRY')['PROFIT'].sum().sort_values(ascending=False).head(10)
profit_by_country.plot(kind='bar', figsize=(10, 6), color='purple')
plt.title("Top 10 Countries by Profit")
plt.ylabel("Profit ($)")
plt.xlabel("Country")
plt.tight_layout()
plt.show()
