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

def get_category_statistics(cat_perf_df):
    """Computes category volume distribution, top performers, and concentration shares."""
    if cat_perf_df.empty or cat_perf_df['products_sold'].sum() == 0:
        return {
            'top_category': 'N/A', 'top_units': 0, 'top_share': 0.0,
            'second_category': 'N/A', 'second_units': 0, 'second_share': 0.0,
            'third_category': 'N/A', 'third_units': 0, 'third_share': 0.0,
            'top3_units': 0, 'top3_share': 0.0,
            'top10_units': 0, 'top10_share': 0.0,
            'total_units': 0
        }
    sorted_df = cat_perf_df.sort_values('products_sold', ascending=False).reset_index(drop=True)
    tot = int(sorted_df['products_sold'].sum())
    
    c1 = sorted_df.iloc[0]
    c2 = sorted_df.iloc[1] if len(sorted_df) > 1 else c1
    c3 = sorted_df.iloc[2] if len(sorted_df) > 2 else c2
    
    top3_u = int(sorted_df.head(3)['products_sold'].sum())
    top10_u = int(sorted_df.head(10)['products_sold'].sum())
    
    return {
        'top_category': str(c1['category_clean']),
        'top_units': int(c1['products_sold']),
        'top_share': float((c1['products_sold'] / tot * 100) if tot > 0 else 0.0),
        'second_category': str(c2['category_clean']),
        'second_units': int(c2['products_sold']) if len(sorted_df) > 1 else 0,
        'second_share': float((c2['products_sold'] / tot * 100) if len(sorted_df) > 1 and tot > 0 else 0.0),
        'third_category': str(c3['category_clean']),
        'third_units': int(c3['products_sold']) if len(sorted_df) > 2 else 0,
        'third_share': float((c3['products_sold'] / tot * 100) if len(sorted_df) > 2 and tot > 0 else 0.0),
        'top3_units': top3_u,
        'top3_share': float((top3_u / tot * 100) if tot > 0 else 0.0),
        'top10_units': top10_u,
        'top10_share': float((top10_u / tot * 100) if tot > 0 else 0.0),
        'total_units': tot
    }

def get_category_region_statistics(cat_region_matrix):
    """Computes regional category variations, peak category-region combinations, and variation spread."""
    if cat_region_matrix.empty or len(cat_region_matrix.columns) == 0:
        return {
            'largest_cat': 'N/A', 'largest_region': 'N/A', 'largest_share': 0.0,
            'lowest_cat': 'N/A', 'lowest_region': 'N/A', 'lowest_share': 0.0,
            'max_variation_cat': 'N/A', 'max_variation_val': 0.0,
            'max_variation_high_reg': 'N/A', 'max_variation_high_val': 0.0,
            'max_variation_low_reg': 'N/A', 'max_variation_low_val': 0.0
        }
    
    # Stacked values for max and min
    stacked = cat_region_matrix.stack()
    if stacked.empty:
        return {
            'largest_cat': 'N/A', 'largest_region': 'N/A', 'largest_share': 0.0,
            'lowest_cat': 'N/A', 'lowest_region': 'N/A', 'lowest_share': 0.0,
            'max_variation_cat': 'N/A', 'max_variation_val': 0.0,
            'max_variation_high_reg': 'N/A', 'max_variation_high_val': 0.0,
            'max_variation_low_reg': 'N/A', 'max_variation_low_val': 0.0
        }
    
    max_idx = stacked.idxmax()
    min_idx = stacked.idxmin()
    
    # Row differences
    row_diff = cat_region_matrix.max(axis=1) - cat_region_matrix.min(axis=1)
    max_var_cat = str(row_diff.idxmax())
    max_var_val = float(row_diff.max())
    
    high_reg = str(cat_region_matrix.loc[max_var_cat].idxmax())
    high_val = float(cat_region_matrix.loc[max_var_cat, high_reg])
    low_reg = str(cat_region_matrix.loc[max_var_cat].idxmin())
    low_val = float(cat_region_matrix.loc[max_var_cat, low_reg])
    
    return {
        'largest_cat': str(max_idx[0]),
        'largest_region': str(max_idx[1]),
        'largest_share': float(stacked[max_idx]),
        'lowest_cat': str(min_idx[0]),
        'lowest_region': str(min_idx[1]),
        'lowest_share': float(stacked[min_idx]),
        'max_variation_cat': max_var_cat,
        'max_variation_val': max_var_val,
        'max_variation_high_reg': high_reg,
        'max_variation_high_val': high_val,
        'max_variation_low_reg': low_reg,
        'max_variation_low_val': low_val
    }

def get_category_comparison_statistics(table_df):
    """Identifies metric-leading categories across sales value, units, AOV, and orders."""
    if table_df.empty:
        return {
            'highest_sales_cat': 'N/A', 'highest_sales_val': 0.0,
            'highest_units_cat': 'N/A', 'highest_units_val': 0,
            'highest_aov_cat': 'N/A', 'highest_aov_val': 0.0,
            'highest_orders_cat': 'N/A', 'highest_orders_val': 0
        }
    
    top_sales_row = table_df.sort_values('product_sales', ascending=False).iloc[0]
    top_units_row = table_df.sort_values('products_sold', ascending=False).iloc[0]
    top_aov_row = table_df.sort_values('avg_sales_per_order', ascending=False).iloc[0]
    top_orders_row = table_df.sort_values('orders', ascending=False).iloc[0]
    
    return {
        'highest_sales_cat': str(top_sales_row['category_clean']),
        'highest_sales_val': float(top_sales_row['product_sales']),
        'highest_units_cat': str(top_units_row['category_clean']),
        'highest_units_val': int(top_units_row['products_sold']),
        'highest_aov_cat': str(top_aov_row['category_clean']),
        'highest_aov_val': float(top_aov_row['avg_sales_per_order']),
        'highest_orders_cat': str(top_orders_row['category_clean']),
        'highest_orders_val': int(top_orders_row['orders'])
    }
