import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('xidmetler_listings.csv')

print("="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"\nTotal Records: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"\nColumn Names: {list(df.columns)}")

print("\n" + "="*80)
print("DATA SAMPLE")
print("="*80)
print(df.head())

print("\n" + "="*80)
print("DATA TYPES")
print("="*80)
print(df.dtypes)

print("\n" + "="*80)
print("MISSING VALUES")
print("="*80)
print(df.isnull().sum())

print("\n" + "="*80)
print("PRICE ANALYSIS")
print("="*80)
# Clean price column
df['price_clean'] = df['price'].astype(str).str.extract(r'(\d+)')[0]
df['price_numeric'] = pd.to_numeric(df['price_clean'], errors='coerce')

print(f"\nPrice Statistics:")
print(df['price_numeric'].describe())

print("\n" + "="*80)
print("LOCATION ANALYSIS")
print("="*80)
print("\nTop 10 Locations:")
print(df['location'].value_counts().head(10))

print("\n" + "="*80)
print("CATEGORIES ANALYSIS")
print("="*80)
print("\nTop 15 Categories:")
print(df['categories'].value_counts().head(15))

print("\n" + "="*80)
print("DATE ANALYSIS")
print("="*80)
# Parse dates
df['date_parsed'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
df['year'] = df['date_parsed'].dt.year
df['month'] = df['date_parsed'].dt.month
df['year_month'] = df['date_parsed'].dt.to_period('M')

print("\nListings by Year:")
print(df['year'].value_counts().sort_index())

print("\nListings by Month (2025):")
df_2025 = df[df['year'] == 2025]
print(df_2025['month'].value_counts().sort_index())

print("\n" + "="*80)
print("CONTACT INFORMATION ANALYSIS")
print("="*80)
print(f"\nListings with contact name: {df['contact_name'].notna().sum()}")
print(f"Listings with phone: {df['phone'].notna().sum()}")

print("\n" + "="*80)
print("PRICE RANGES")
print("="*80)
price_ranges = pd.cut(df['price_numeric'].dropna(),
                      bins=[0, 50, 100, 200, 500, 1000, 10000],
                      labels=['0-50 AZN', '51-100 AZN', '101-200 AZN',
                             '201-500 AZN', '501-1000 AZN', '1000+ AZN'])
print(price_ranges.value_counts().sort_index())

# Save cleaned data for chart generation
df.to_csv('xidmetler_listings_cleaned.csv', index=False)
print("\n" + "="*80)
print("Cleaned data saved to: xidmetler_listings_cleaned.csv")
print("="*80)
