import pandas as pd
import numpy as np

def calculate_concentration(series, top_n=3):
    """Calculates the percentage share of the top N categories/states."""
    if series.empty or series.sum() == 0:
        return 0.0
    sorted_s = series.sort_values(ascending=False)
    top_sum = sorted_s.head(top_n).sum()
    total = series.sum()
    return (top_sum / total) * 100

def get_hhi(series):
    """Calculates Herfindahl-Hirschman Index for market/channel concentration."""
    if series.empty or series.sum() == 0:
        return 0.0
    shares = (series / series.sum()) * 100
    return (shares ** 2).sum()

def calculate_repeat_rate(orders_df):
    """Calculates total unique customers, repeat customers, and repeat rate."""
    if orders_df.empty or 'customer_unique_id' not in orders_df.columns:
        return 0, 0, 0.0
    cust_counts = orders_df.groupby('customer_unique_id')['order_id'].nunique()
    unique_cust = len(cust_counts)
    repeat_cust = (cust_counts > 1).sum()
    rate = (repeat_cust / unique_cust * 100) if unique_cust > 0 else 0.0
    return unique_cust, repeat_cust, rate
