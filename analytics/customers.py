import pandas as pd
import numpy as np

def get_customer_kpis(orders_df, items_df):
    if orders_df.empty or 'customer_unique_id' not in orders_df.columns:
        return {
            'unique_customers': 0,
            'repeat_customers': 0,
            'repeat_rate': 0.0,
            'unique_products': 0,
            'unique_categories': 0,
            'products_sold': 0
        }
    
    cust_orders = orders_df.groupby('customer_unique_id')['order_id'].nunique()
    unique_cust = len(cust_orders)
    repeat_cust = (cust_orders > 1).sum()
    repeat_rate = (repeat_cust / unique_cust * 100) if unique_cust > 0 else 0.0
    
    unique_prods = items_df['product_id'].nunique() if not items_df.empty else 0
    unique_cats = items_df['category_clean'].nunique() if not items_df.empty else 0
    prods_sold = len(items_df)
    
    return {
        'unique_customers': unique_cust,
        'repeat_customers': repeat_cust,
        'repeat_rate': repeat_rate,
        'unique_products': unique_prods,
        'unique_categories': unique_cats,
        'products_sold': prods_sold
    }

def get_customers_by_state(orders_df):
    if orders_df.empty:
        return pd.DataFrame(columns=['customer_state', 'customer_count', 'share_pct'])
    
    state_cust = orders_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
    state_cust.columns = ['customer_state', 'customer_count']
    state_cust = state_cust.sort_values('customer_count', ascending=False).reset_index(drop=True)
    total = state_cust['customer_count'].sum()
    state_cust['share_pct'] = (state_cust['customer_count'] / total * 100) if total > 0 else 0.0
    return state_cust

def get_top_cities_by_customers(orders_df, top_n=10):
    if orders_df.empty:
        return pd.DataFrame(columns=['customer_city', 'customer_count'])
    
    # Clean city names to Title Case
    city_cust = orders_df.groupby('customer_city')['customer_unique_id'].nunique().reset_index()
    city_cust.columns = ['customer_city', 'customer_count']
    city_cust['customer_city'] = city_cust['customer_city'].str.title()
    city_cust = city_cust.groupby('customer_city')['customer_count'].sum().reset_index()
    city_cust = city_cust.sort_values('customer_count', ascending=False).reset_index(drop=True)
    return city_cust.head(top_n)

def get_customers_by_order_frequency(orders_df):
    if orders_df.empty:
        return pd.DataFrame(columns=['frequency_bucket', 'customer_count', 'share_pct'])
    
    cust_orders = orders_df.groupby('customer_unique_id')['order_id'].nunique()
    
    freq_1 = (cust_orders == 1).sum()
    freq_2 = (cust_orders == 2).sum()
    freq_3 = (cust_orders == 3).sum()
    freq_4plus = (cust_orders >= 4).sum()
    
    total = len(cust_orders)
    data = [
        {'frequency_bucket': '1 Order', 'customer_count': freq_1, 'share_pct': (freq_1 / total * 100) if total > 0 else 0},
        {'frequency_bucket': '2 Orders', 'customer_count': freq_2, 'share_pct': (freq_2 / total * 100) if total > 0 else 0},
        {'frequency_bucket': '3 Orders', 'customer_count': freq_3, 'share_pct': (freq_3 / total * 100) if total > 0 else 0},
        {'frequency_bucket': '4+ Orders', 'customer_count': freq_4plus, 'share_pct': (freq_4plus / total * 100) if total > 0 else 0}
    ]
    return pd.DataFrame(data)
