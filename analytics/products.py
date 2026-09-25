import pandas as pd
import numpy as np

def get_product_category_performance(items_df, top_n=10):
    if items_df.empty:
        return pd.DataFrame(columns=['category_clean', 'products_sold', 'product_sales', 'share_pct'])
    
    cat_summary = items_df.groupby('category_clean').agg(
        products_sold=('order_item_id', 'count'),
        product_sales=('price', 'sum'),
        orders=('order_id', 'nunique')
    ).reset_index()
    
    total_prods = cat_summary['products_sold'].sum()
    total_sales = cat_summary['product_sales'].sum()
    
    cat_summary['share_pct'] = (cat_summary['products_sold'] / total_prods * 100) if total_prods > 0 else 0.0
    cat_summary['revenue_share_pct'] = (cat_summary['product_sales'] / total_sales * 100) if total_sales > 0 else 0.0
    cat_summary['avg_sales_per_order'] = (cat_summary['product_sales'] / cat_summary['orders']).fillna(0.0)
    
    cat_summary = cat_summary.sort_values('products_sold', ascending=False).reset_index(drop=True)
    return cat_summary.head(top_n)

def get_category_performance_table(items_df, top_n=15):
    """Detailed analytical table with formatting columns."""
    if items_df.empty:
        return pd.DataFrame()
    
    table_df = items_df.groupby('category_clean').agg(
        product_sales=('price', 'sum'),
        products_sold=('order_item_id', 'count'),
        orders=('order_id', 'nunique')
    ).reset_index()
    
    total_sales = table_df['product_sales'].sum()
    table_df['avg_sales_per_order'] = (table_df['product_sales'] / table_df['orders']).fillna(0.0)
    table_df['revenue_share'] = (table_df['product_sales'] / total_sales * 100) if total_sales > 0 else 0.0
    
    table_df = table_df.sort_values('product_sales', ascending=False).reset_index(drop=True)
    return table_df.head(top_n)

def get_category_share_by_region(items_df, top_n=9):
    """
    Computes percentage share of category sales across Brazilian macro-regions.
    Rows: Top Categories
    Columns: Central-West, North, Northeast, South, Southeast
    """
    if items_df.empty:
        return pd.DataFrame()
    
    # Exclude other/uncategorized if present or keep top categories
    valid_items = items_df[items_df['customer_region'] != 'Other'].copy()
    top_cats = valid_items['category_clean'].value_counts().head(top_n).index.tolist()
    sub_df = valid_items[valid_items['category_clean'].isin(top_cats)]
    
    # Crosstab normalized by region (column-wise percentage)
    matrix = pd.crosstab(sub_df['category_clean'], sub_df['customer_region'], normalize='columns') * 100
    
    region_cols = ['Central-West', 'North', 'Northeast', 'South', 'Southeast']
    available_cols = [c for c in region_cols if c in matrix.columns]
    matrix = matrix[available_cols].loc[top_cats]
    
    return matrix
