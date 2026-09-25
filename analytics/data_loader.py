import os
import streamlit as st
import pandas as pd
from preprocess import preprocess_and_cache

PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')

@st.cache_data(show_spinner="Loading master analytical datasets...")
def load_analytical_data():
    orders_path = os.path.join(PROCESSED_DIR, 'orders_master.parquet')
    items_path = os.path.join(PROCESSED_DIR, 'items_master.parquet')
    payments_path = os.path.join(PROCESSED_DIR, 'payments_master.parquet')
    
    if not (os.path.exists(orders_path) and os.path.exists(items_path) and os.path.exists(payments_path)):
        preprocess_and_cache(raw_dir=RAW_DIR, processed_dir=PROCESSED_DIR)
        
    orders_df = pd.read_parquet(orders_path)
    items_df = pd.read_parquet(items_path)
    payments_df = pd.read_parquet(payments_path)
    
    return orders_df, items_df, payments_df

def apply_global_filters(orders_df, items_df, payments_df, filters):
    """
    Applies global sidebar filters consistently across the analytical dataframes.
    Filters dict keys:
    - year: 'All' or specific year (int)
    - quarter: 'All' or 'Q1', 'Q2', etc.
    - region: 'All' or list of regions
    - state: 'All' or list of states
    - category: 'All' or list of categories
    - status: 'All' or list of order statuses
    """
    filtered_orders = orders_df.copy()
    filtered_items = items_df.copy()
    filtered_payments = payments_df.copy()
    
    # Year filter
    if filters.get('year') and filters['year'] != 'All':
        y = int(filters['year'])
        filtered_orders = filtered_orders[filtered_orders['year'] == y]
        filtered_items = filtered_items[filtered_items['year'] == y]
        filtered_payments = filtered_payments[filtered_payments['year'] == y]
        
    # Quarter filter
    if filters.get('quarter') and filters['quarter'] != 'All':
        q = str(filters['quarter'])
        filtered_orders = filtered_orders[filtered_orders['quarter'] == q]
        filtered_items = filtered_items[filtered_items['quarter'] == q]
        
    # Region filter (Customer Region)
    if filters.get('region') and filters['region'] != 'All':
        regs = filters['region'] if isinstance(filters['region'], list) else [filters['region']]
        filtered_orders = filtered_orders[filtered_orders['customer_region'].isin(regs)]
        filtered_items = filtered_items[filtered_items['customer_region'].isin(regs)]
        filtered_payments = filtered_payments[filtered_payments['customer_region'].isin(regs)]
        
    # State filter (Customer State)
    if filters.get('state') and filters['state'] != 'All':
        sts = filters['state'] if isinstance(filters['state'], list) else [filters['state']]
        filtered_orders = filtered_orders[filtered_orders['customer_state'].isin(sts)]
        filtered_items = filtered_items[filtered_items['customer_state'].isin(sts)]
        filtered_payments = filtered_payments[filtered_payments['customer_state'].isin(sts)]
        
    # Category filter
    if filters.get('category') and filters['category'] != 'All':
        cats = filters['category'] if isinstance(filters['category'], list) else [filters['category']]
        # Sift items first
        filtered_items = filtered_items[filtered_items['category_clean'].isin(cats)]
        # Match orders containing these items
        valid_order_ids = set(filtered_items['order_id'])
        filtered_orders = filtered_orders[filtered_orders['order_id'].isin(valid_order_ids)]
        filtered_payments = filtered_payments[filtered_payments['order_id'].isin(valid_order_ids)]
        
    # Order status filter
    if filters.get('status') and filters['status'] != 'All':
        statuses = filters['status'] if isinstance(filters['status'], list) else [filters['status']]
        filtered_orders = filtered_orders[filtered_orders['order_status'].isin(statuses)]
        filtered_items = filtered_items[filtered_items['order_status'].isin(statuses)]
        filtered_payments = filtered_payments[filtered_payments['order_status'].isin(statuses)]
        
    return filtered_orders, filtered_items, filtered_payments
