import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51']

# Load cleaned data
df = pd.read_csv('xidmetler_listings_cleaned.csv')

print("Generating business insights charts...")

# ============================================================================
# CHART 1: Market Composition - Top Service Categories
# ============================================================================
print("Creating Chart 1: Market Composition by Service Category...")

# Extract main category (first part before comma)
df['main_category'] = df['categories'].astype(str).apply(
    lambda x: x.split(',')[0].strip() if x != 'nan' and x != 'N/A' else 'Uncategorized'
)

category_counts = df['main_category'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(range(len(category_counts)), category_counts.values, color=colors[0])
ax.set_yticks(range(len(category_counts)))
ax.set_yticklabels(category_counts.index, fontsize=11)
ax.set_xlabel('Number of Service Listings', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Service Categories on Platform\nMarket Composition Analysis',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, category_counts.values)):
    ax.text(value + 10, i, f'{value:,} ({value/len(df)*100:.1f}%)',
            va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/01_market_composition.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 2: Pricing Landscape - Price Distribution
# ============================================================================
print("Creating Chart 2: Pricing Landscape...")

price_data = df['price_numeric'].dropna()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
ax1.hist(price_data, bins=50, color=colors[1], edgecolor='black', alpha=0.7)
ax1.axvline(price_data.median(), color='red', linestyle='--', linewidth=2,
            label=f'Median: {price_data.median():.0f} AZN')
ax1.axvline(price_data.mean(), color='green', linestyle='--', linewidth=2,
            label=f'Average: {price_data.mean():.0f} AZN')
ax1.set_xlabel('Price (AZN)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Listings', fontsize=12, fontweight='bold')
ax1.set_title('Price Distribution Across All Services', fontsize=13, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(alpha=0.3)

# Price ranges
price_ranges_labels = ['0-50\nAZN', '51-100\nAZN', '101-200\nAZN',
                       '201-500\nAZN', '501-1000\nAZN']
price_ranges_counts = pd.cut(price_data,
                             bins=[0, 50, 100, 200, 500, 1000],
                             labels=price_ranges_labels).value_counts().sort_index()

bars = ax2.bar(range(len(price_ranges_counts)), price_ranges_counts.values,
               color=colors[:len(price_ranges_counts)], edgecolor='black', alpha=0.8)
ax2.set_xticks(range(len(price_ranges_counts)))
ax2.set_xticklabels(price_ranges_labels, fontsize=11)
ax2.set_ylabel('Number of Listings', fontsize=12, fontweight='bold')
ax2.set_title('Service Listings by Price Segment', fontsize=13, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Add value labels and percentages
for i, (bar, value) in enumerate(zip(bars, price_ranges_counts.values)):
    percentage = value / len(price_data) * 100
    ax2.text(i, value + 20, f'{value:,}\n({percentage:.1f}%)',
             ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/02_pricing_landscape.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 3: Pricing Strategy by Service Category
# ============================================================================
print("Creating Chart 3: Average Pricing by Service Category...")

# Calculate average price by main category (top 12)
top_categories = df['main_category'].value_counts().head(12).index
df_top = df[df['main_category'].isin(top_categories)].copy()
category_pricing = df_top.groupby('main_category')['price_numeric'].agg(['mean', 'median', 'count'])
category_pricing = category_pricing.sort_values('mean', ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))
x = range(len(category_pricing))
width = 0.35

bars1 = ax.barh([i - width/2 for i in x], category_pricing['mean'],
                width, label='Average Price', color=colors[2], alpha=0.8)
bars2 = ax.barh([i + width/2 for i in x], category_pricing['median'],
                width, label='Median Price', color=colors[3], alpha=0.8)

ax.set_yticks(x)
ax.set_yticklabels(category_pricing.index, fontsize=10)
ax.set_xlabel('Price (AZN)', fontsize=12, fontweight='bold')
ax.set_title('Average vs Median Pricing by Service Category\nPricing Strategy Analysis',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11, loc='lower right')
ax.grid(axis='x', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        width_val = bar.get_width()
        ax.text(width_val + 2, bar.get_y() + bar.get_height()/2,
                f'{width_val:.0f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('charts/03_pricing_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 4: Listing Quality & Completeness Score
# ============================================================================
print("Creating Chart 4: Listing Quality Analysis...")

# Calculate quality metrics
df['has_contact_name'] = df['contact_name'].notna().astype(int)
df['has_phone'] = df['phone'].notna().astype(int)
df['has_category'] = (~df['categories'].isin(['N/A', 'nan', np.nan])).astype(int)
df['has_images'] = df['images'].notna().astype(int)
df['has_description'] = df['description'].notna().astype(int)

df['quality_score'] = (df['has_contact_name'] + df['has_phone'] +
                       df['has_category'] + df['has_images'] +
                       df['has_description'])

quality_dist = df['quality_score'].value_counts().sort_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Quality score distribution
bars = ax1.bar(quality_dist.index, quality_dist.values,
               color=colors[4], edgecolor='black', alpha=0.8)
ax1.set_xlabel('Quality Score (0-5)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Listings', fontsize=12, fontweight='bold')
ax1.set_title('Listing Quality Score Distribution\n(Based on Data Completeness)',
              fontsize=13, fontweight='bold')
ax1.set_xticks(range(6))
ax1.grid(axis='y', alpha=0.3)

for bar, value in zip(bars, quality_dist.values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height + 10,
             f'{value:,}\n({value/len(df)*100:.1f}%)',
             ha='center', fontsize=10, fontweight='bold')

# Component breakdown
components = {
    'Contact Name': df['has_contact_name'].sum(),
    'Phone Number': df['has_phone'].sum(),
    'Category': df['has_category'].sum(),
    'Images': df['has_images'].sum(),
    'Description': df['has_description'].sum()
}

bars = ax2.barh(list(components.keys()), list(components.values()),
                color=colors[5], edgecolor='black', alpha=0.8)
ax2.set_xlabel('Number of Listings', fontsize=12, fontweight='bold')
ax2.set_title('Listing Completeness by Component\nData Quality Metrics',
              fontsize=13, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

for i, (bar, value) in enumerate(zip(bars, components.values())):
    percentage = value / len(df) * 100
    ax2.text(value + 20, i, f'{value:,} ({percentage:.1f}%)',
             va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/04_listing_quality.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 5: Market Segmentation - Budget vs Premium Services
# ============================================================================
print("Creating Chart 5: Market Segmentation Analysis...")

# Define segments
def categorize_segment(price):
    if pd.isna(price):
        return 'Unknown'
    elif price <= 50:
        return 'Budget (0-50 AZN)'
    elif price <= 100:
        return 'Mid-Range (51-100 AZN)'
    elif price <= 200:
        return 'Premium (101-200 AZN)'
    else:
        return 'Luxury (200+ AZN)'

df['market_segment'] = df['price_numeric'].apply(categorize_segment)

segment_counts = df['market_segment'].value_counts()
segment_order = ['Budget (0-50 AZN)', 'Mid-Range (51-100 AZN)',
                 'Premium (101-200 AZN)', 'Luxury (200+ AZN)', 'Unknown']
segment_counts = segment_counts.reindex(segment_order, fill_value=0)

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(range(len(segment_counts)), segment_counts.values,
              color=colors[:len(segment_counts)], edgecolor='black', alpha=0.8)
ax.set_xticks(range(len(segment_counts)))
ax.set_xticklabels(segment_counts.index, fontsize=11, rotation=15, ha='right')
ax.set_ylabel('Number of Listings', fontsize=12, fontweight='bold')
ax.set_title('Market Segmentation: Distribution Across Price Tiers\nStrategic Positioning Analysis',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)

# Add value labels and percentages
for bar, value in zip(bars, segment_counts.values):
    height = bar.get_height()
    percentage = value / len(df) * 100
    ax.text(bar.get_x() + bar.get_width()/2, height + 15,
            f'{value:,}\n({percentage:.1f}%)',
            ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/05_market_segmentation.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 6: Top Service Categories - Detailed Volume Analysis
# ============================================================================
print("Creating Chart 6: Service Volume by Top Categories...")

# Get top 15 categories with detailed breakdown
top_15_cats = df['main_category'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(range(len(top_15_cats)), top_15_cats.values,
              color=colors[0], edgecolor='black', alpha=0.7)
ax.set_xticks(range(len(top_15_cats)))
ax.set_xticklabels(top_15_cats.index, fontsize=10, rotation=45, ha='right')
ax.set_ylabel('Number of Listings', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Service Categories by Listing Volume\nMarket Opportunity Analysis',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, top_15_cats.values)):
    height = bar.get_height()
    percentage = value / len(df) * 100
    ax.text(i, height + 10, f'{value:,}\n{percentage:.1f}%',
            ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/06_top_categories_volume.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 7: Pricing Trends - Category Comparison
# ============================================================================
print("Creating Chart 7: Price Comparison Across Key Categories...")

# Focus on top 8 categories with sufficient data
top_8_cats = df['main_category'].value_counts().head(8).index
df_comp = df[df['main_category'].isin(top_8_cats) & df['price_numeric'].notna()].copy()

fig, ax = plt.subplots(figsize=(14, 8))

# Create box plot style visualization using bars
category_stats = []
positions = []
for i, cat in enumerate(top_8_cats):
    cat_data = df_comp[df_comp['main_category'] == cat]['price_numeric']
    if len(cat_data) > 0:
        category_stats.append({
            'category': cat,
            'min': cat_data.min(),
            'q25': cat_data.quantile(0.25),
            'median': cat_data.median(),
            'q75': cat_data.quantile(0.75),
            'max': cat_data.max(),
            'mean': cat_data.mean()
        })
        positions.append(i)

# Plot median prices
medians = [stat['median'] for stat in category_stats]
bars = ax.bar(positions, medians, color=colors[1], alpha=0.6,
              edgecolor='black', label='Median Price')

# Add mean as markers
means = [stat['mean'] for stat in category_stats]
ax.scatter(positions, means, color='red', s=100, zorder=5,
          label='Average Price', marker='D')

ax.set_xticks(positions)
ax.set_xticklabels([stat['category'] for stat in category_stats],
                   fontsize=10, rotation=45, ha='right')
ax.set_ylabel('Price (AZN)', fontsize=12, fontweight='bold')
ax.set_title('Price Comparison: Median and Average Across Top Service Categories\nCompetitive Pricing Analysis',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Add value labels
for i, (med, avg) in enumerate(zip(medians, means)):
    ax.text(i, med + 5, f'{med:.0f} AZN', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/07_category_price_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# Generate Summary Statistics File
# ============================================================================
print("Generating summary statistics...")

summary_stats = {
    'Total Listings': len(df),
    'Average Price (AZN)': f"{df['price_numeric'].mean():.2f}",
    'Median Price (AZN)': f"{df['price_numeric'].median():.2f}",
    'Price Range': f"{df['price_numeric'].min():.0f} - {df['price_numeric'].max():.0f} AZN",
    'Total Categories': df['main_category'].nunique(),
    'Listings in Baku': df[df['location'] == 'Bakı şəhəri'].shape[0],
    'Listings with Phone': df['has_phone'].sum(),
    'Listings with Images': df['has_images'].sum(),
    'Budget Services (0-50 AZN)': len(df[df['price_numeric'] <= 50]),
    'Mid-Range Services (51-100 AZN)': len(df[(df['price_numeric'] > 50) & (df['price_numeric'] <= 100)]),
    'Premium Services (100+ AZN)': len(df[df['price_numeric'] > 100]),
    'Top Category': df['main_category'].value_counts().index[0],
    'Top Category Volume': int(df['main_category'].value_counts().values[0])
}

with open('charts/summary_statistics.txt', 'w', encoding='utf-8') as f:
    f.write("XIDMETLER.AZ MARKETPLACE - KEY BUSINESS METRICS\n")
    f.write("=" * 60 + "\n\n")
    for key, value in summary_stats.items():
        f.write(f"{key}: {value}\n")

print("\n" + "="*80)
print("CHART GENERATION COMPLETE!")
print("="*80)
print("\nGenerated 7 business insight charts:")
print("  1. charts/01_market_composition.png")
print("  2. charts/02_pricing_landscape.png")
print("  3. charts/03_pricing_by_category.png")
print("  4. charts/04_listing_quality.png")
print("  5. charts/05_market_segmentation.png")
print("  6. charts/06_top_categories_volume.png")
print("  7. charts/07_category_price_comparison.png")
print("\nSummary statistics saved to: charts/summary_statistics.txt")
print("="*80)
