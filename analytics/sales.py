import pandas as pd
import numpy as np
from utils.calculations import calculate_concentration

def get_executive_kpis(orders_df, items_df, payments_df):
    total_orders = len(orders_df)
    total_revenue = orders_df['total_payment'].sum()
    unique_customers = orders_df['customer_unique_id'].nunique() if 'customer_unique_id' in orders_df.columns else 0
    aov = (total_revenue / total_orders) if total_orders > 0 else 0.0
    products_sold = len(items_df)
    
    return {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'unique_customers': unique_customers,
        'aov': aov,
        'products_sold': products_sold
    }

def get_monthly_orders_and_revenue(orders_df):
    if orders_df.empty:
        return pd.DataFrame(columns=['year_month', 'orders_count', 'revenue'])
    
    monthly = orders_df.groupby('year_month').agg(
        orders_count=('order_id', 'count'),
        revenue=('total_payment', 'sum')
    ).reset_index()
    
    # Sort chronologically
    monthly = monthly.sort_values('year_month').reset_index(drop=True)
    return monthly

def get_orders_by_weekday(orders_df):
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if orders_df.empty:
        return pd.DataFrame(columns=['weekday', 'orders_count', 'share_pct'])
    
    wk = orders_df['weekday'].value_counts().reindex(weekday_order).fillna(0).reset_index()
    wk.columns = ['weekday', 'orders_count']
    total = wk['orders_count'].sum()
    wk['share_pct'] = (wk['orders_count'] / total * 100) if total > 0 else 0.0
    return wk

def get_payment_method_distribution(payments_df):
    if payments_df.empty:
        return pd.DataFrame(columns=['payment_type_clean', 'total_value', 'share_pct'])
    
    pmt = payments_df.groupby('payment_type_clean')['payment_value'].sum().reset_index()
    pmt.columns = ['payment_type_clean', 'total_value']
    pmt = pmt.sort_values('total_value', ascending=False).reset_index(drop=True)
    total = pmt['total_value'].sum()
    pmt['share_pct'] = (pmt['total_value'] / total * 100) if total > 0 else 0.0
    return pmt

def get_top_states_by_revenue(orders_df, top_n=10):
    if orders_df.empty:
        return pd.DataFrame(columns=['customer_state', 'total_revenue', 'share_pct'])
    
    state_rev = orders_df.groupby('customer_state')['total_payment'].sum().reset_index()
    state_rev.columns = ['customer_state', 'total_revenue']
    state_rev = state_rev.sort_values('total_revenue', ascending=False).reset_index(drop=True)
    total = state_rev['total_revenue'].sum()
    state_rev['share_pct'] = (state_rev['total_revenue'] / total * 100) if total > 0 else 0.0
    return state_rev.head(top_n)

def get_non_delivered_orders(orders_df):
    non_deliv = orders_df[orders_df['order_status'] != 'delivered'].copy()
    if non_deliv.empty:
        return pd.DataFrame(columns=['order_status', 'count', 'share_pct', 'revenue_at_risk'])
    
    status_summary = non_deliv.groupby('order_status').agg(
        count=('order_id', 'count'),
        revenue_at_risk=('total_payment', 'sum')
    ).reset_index()
    status_summary = status_summary.sort_values('count', ascending=False).reset_index(drop=True)
    total = status_summary['count'].sum()
    status_summary['share_pct'] = (status_summary['count'] / total * 100) if total > 0 else 0.0
    return status_summary
