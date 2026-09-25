import pandas as pd
import numpy as np

def get_review_kpis(orders_df):
    rev_orders = orders_df[orders_df['review_score'].notna()].copy()
    if rev_orders.empty:
        return {
            'avg_review_score': 0.0,
            'low_rating_pct': 0.0,
            'ontime_avg_rating': 0.0,
            'late_avg_rating': 0.0,
            'severe_delay_rating': 0.0,
            'rating_gap': 0.0
        }
        
    avg_score = rev_orders['review_score'].mean()
    low_pct = (rev_orders['review_score'] <= 2).mean() * 100
    
    # Rating by delivery status
    ontime_orders = rev_orders[rev_orders['delay_bucket'] == 'On time / early']
    late_orders = rev_orders[rev_orders['is_late']]
    severe_orders = rev_orders[rev_orders['delay_bucket'] == '8+ days late']
    
    ontime_avg = ontime_orders['review_score'].mean() if not ontime_orders.empty else 0.0
    late_avg = late_orders['review_score'].mean() if not late_orders.empty else 0.0
    severe_avg = severe_orders['review_score'].mean() if not severe_orders.empty else 0.0
    rating_gap = ontime_avg - severe_avg
    
    return {
        'avg_review_score': avg_score,
        'low_rating_pct': low_pct,
        'ontime_avg_rating': ontime_avg,
        'late_avg_rating': late_avg,
        'severe_delay_rating': severe_avg,
        'rating_gap': rating_gap
    }

def get_ratings_by_delay_bucket(orders_df):
    """
    Hero Visual: Ratings Collapse Once a Parcel is Late.
    Delay Buckets: On time / early, 1-3 days late, 4-7 days late, 8+ days late.
    """
    rev_orders = orders_df[orders_df['review_score'].notna() & orders_df['is_delivered']].copy()
    if rev_orders.empty:
        return pd.DataFrame(columns=['delay_bucket', 'avg_score', 'low_rating_pct', 'orders_count'])
        
    buckets = ['On time / early', '1-3 days late', '4-7 days late', '8+ days late']
    filtered = rev_orders[rev_orders['delay_bucket'].isin(buckets)].copy()
    
    agg_df = filtered.groupby('delay_bucket').agg(
        avg_score=('review_score', 'mean'),
        low_rating_pct=('review_score', lambda x: (x <= 2).mean() * 100),
        orders_count=('order_id', 'count')
    ).reindex(buckets).reset_index()
    
    return agg_df

def get_category_sales_vs_experience(items_df):
    """
    For Treemap: Size = Product Sales, Color = Average Review Score.
    """
    valid = items_df[items_df['category_clean'].notna() & items_df['review_score'].notna()].copy()
    if valid.empty:
        return pd.DataFrame(columns=['category_clean', 'product_sales', 'avg_review_score', 'products_sold'])
        
    cat_stats = valid.groupby('category_clean').agg(
        product_sales=('price', 'sum'),
        avg_review_score=('review_score', 'mean'),
        products_sold=('order_item_id', 'count')
    ).reset_index()
    
    # Filter categories with at least 50 sales for meaningful treemap
    cat_stats = cat_stats[cat_stats['products_sold'] >= 30].sort_values('product_sales', ascending=False).reset_index(drop=True)
    return cat_stats

def get_low_rating_decomposition(orders_df, items_df, dimension='Delay Bucket'):
    """
    Investigates drivers of low ratings across selected dimension.
    Supported dimensions: 'Delay Bucket', 'Customer Region', 'Seller Region', 'Customer State', 'Product Category'
    """
    if dimension in ['Delay Bucket', 'Customer Region', 'Customer State']:
        valid = orders_df[orders_df['review_score'].notna()].copy()
        col_map = {
            'Delay Bucket': 'delay_bucket',
            'Customer Region': 'customer_region',
            'Customer State': 'customer_state'
        }
        dim_col = col_map[dimension]
        valid = valid[valid[dim_col].notna() & (valid[dim_col] != 'Not Delivered')]
        
        decomp = valid.groupby(dim_col).agg(
            orders=('order_id', 'count'),
            avg_review=('review_score', 'mean'),
            low_rating_count=('is_low_rating', 'sum')
        ).reset_index()
        decomp.rename(columns={dim_col: 'segment'}, inplace=True)
    else:
        # Requires items_df for Seller Region or Product Category
        valid = items_df[items_df['review_score'].notna()].copy()
        if dimension == 'Seller Region':
            dim_col = 'seller_region'
        else:
            dim_col = 'category_clean'
        valid = valid[valid[dim_col].notna() & (valid[dim_col] != 'Other')]
        
        decomp = valid.groupby(dim_col).agg(
            orders=('order_id', 'nunique'),
            avg_review=('review_score', 'mean'),
            low_rating_count=('is_low_rating', lambda x: x.sum())
        ).reset_index()
        decomp.rename(columns={dim_col: 'segment'}, inplace=True)
        
    decomp['low_rating_pct'] = (decomp['low_rating_count'] / decomp['orders'] * 100).fillna(0.0)
    # Filter tiny samples
    decomp = decomp[decomp['orders'] >= 20].sort_values('low_rating_pct', ascending=False).reset_index(drop=True)
    return decomp

def get_reviews_and_late_over_time(orders_df):
    """
    Combo chart over monthly time series:
    Bars: Late Delivery %
    Line: Average Review Score
    """
    delivered = orders_df[orders_df['is_delivered'] & orders_df['review_score'].notna()].copy()
    if delivered.empty:
        return pd.DataFrame(columns=['year_month', 'late_pct', 'avg_review_score'])
        
    time_agg = delivered.groupby('year_month').agg(
        total_delivered=('order_id', 'count'),
        late_delivered=('is_late', 'sum'),
        avg_review_score=('review_score', 'mean')
    ).reset_index()
    
    time_agg['late_pct'] = (time_agg['late_delivered'] / time_agg['total_delivered'] * 100)
    time_agg = time_agg.sort_values('year_month').reset_index(drop=True)
    # Filter months with at least 50 orders
    time_agg = time_agg[time_agg['total_delivered'] >= 50].reset_index(drop=True)
    return time_agg
