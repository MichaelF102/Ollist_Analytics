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

def get_customer_geography_statistics(state_cust_df, total_customers=None):
    """Computes distribution, ranking, and concentration statistics for customer geography by state."""
    if state_cust_df.empty or state_cust_df['customer_count'].sum() == 0:
        return {
            'top_state': 'N/A', 'top_customers': 0, 'top_share': 0.0,
            'lowest_state': 'N/A', 'lowest_customers': 0,
            'top3_states': [], 'top3_customers': 0, 'top3_share': 0.0,
            'top5_states': [], 'top5_customers': 0, 'top5_share': 0.0,
            'total_customers': 0
        }
    sorted_df = state_cust_df.sort_values('customer_count', ascending=False).reset_index(drop=True)
    tot = total_customers if total_customers is not None and total_customers > 0 else float(sorted_df['customer_count'].sum())
    
    top_s = sorted_df.iloc[0]
    low_s = sorted_df.iloc[-1]
    
    top3_cust = int(sorted_df.head(3)['customer_count'].sum())
    top5_cust = int(sorted_df.head(5)['customer_count'].sum())
    
    return {
        'top_state': str(top_s['customer_state']),
        'top_customers': int(top_s['customer_count']),
        'top_share': float((top_s['customer_count'] / tot * 100) if tot > 0 else 0.0),
        'lowest_state': str(low_s['customer_state']),
        'lowest_customers': int(low_s['customer_count']),
        'top3_states': sorted_df.head(3)['customer_state'].tolist(),
        'top3_customers': top3_cust,
        'top3_share': float((top3_cust / tot * 100) if tot > 0 else 0.0),
        'top5_states': sorted_df.head(5)['customer_state'].tolist(),
        'top5_customers': top5_cust,
        'top5_share': float((top5_cust / tot * 100) if tot > 0 else 0.0),
        'total_customers': int(tot)
    }

def get_city_concentration_statistics(city_cust_df, total_customers=None):
    """Computes metropolitan concentration, gap between top cities, and urban share."""
    if city_cust_df.empty or city_cust_df['customer_count'].sum() == 0:
        return {
            'top_city': 'N/A', 'top_city_customers': 0,
            'second_city': 'N/A', 'second_city_customers': 0,
            'gap_top2': 0, 'ratio_top2': 1.0,
            'top3_customers': 0, 'top3_share': 0.0,
            'top10_customers': 0, 'top10_share': 0.0,
            'total_customers': 0
        }
    sorted_df = city_cust_df.sort_values('customer_count', ascending=False).reset_index(drop=True)
    tot = total_customers if total_customers is not None and total_customers > 0 else float(sorted_df['customer_count'].sum())
    
    c1 = sorted_df.iloc[0]
    c2 = sorted_df.iloc[1] if len(sorted_df) > 1 else c1
    
    gap = int(c1['customer_count'] - (c2['customer_count'] if len(sorted_df) > 1 else 0))
    ratio = float(c1['customer_count'] / c2['customer_count']) if (len(sorted_df) > 1 and c2['customer_count'] > 0) else 1.0
    
    top3_cust = int(sorted_df.head(3)['customer_count'].sum())
    top10_cust = int(sorted_df.head(10)['customer_count'].sum())
    
    return {
        'top_city': str(c1['customer_city']),
        'top_city_customers': int(c1['customer_count']),
        'second_city': str(c2['customer_city']) if len(sorted_df) > 1 else 'None',
        'second_city_customers': int(c2['customer_count']) if len(sorted_df) > 1 else 0,
        'gap_top2': gap,
        'ratio_top2': ratio,
        'top3_customers': top3_cust,
        'top3_share': float((top3_cust / tot * 100) if tot > 0 else 0.0),
        'top10_customers': top10_cust,
        'top10_share': float((top10_cust / tot * 100) if tot > 0 else 0.0),
        'total_customers': int(tot)
    }

def get_order_frequency_statistics(freq_df):
    """Computes breakdown of order count cohorts (1-order vs repeat purchasers)."""
    if freq_df.empty or freq_df['customer_count'].sum() == 0:
        return {
            'one_order_count': 0, 'one_order_share': 0.0,
            'two_orders_count': 0, 'two_orders_share': 0.0,
            'three_orders_count': 0, 'three_orders_share': 0.0,
            'four_plus_count': 0, 'four_plus_share': 0.0,
            'repeat_count': 0, 'repeat_share': 0.0,
            'three_plus_count': 0, 'three_plus_share': 0.0,
            'total_customers': 0
        }
    
    def _get_val(bucket_name):
        row = freq_df[freq_df['frequency_bucket'] == bucket_name]
        return int(row['customer_count'].iloc[0]) if not row.empty else 0
        
    def _get_pct(bucket_name):
        row = freq_df[freq_df['frequency_bucket'] == bucket_name]
        return float(row['share_pct'].iloc[0]) if not row.empty else 0.0
        
    cnt_1 = _get_val('1 Order')
    cnt_2 = _get_val('2 Orders')
    cnt_3 = _get_val('3 Orders')
    cnt_4plus = _get_val('4+ Orders')
    
    tot = int(freq_df['customer_count'].sum())
    rep_cnt = cnt_2 + cnt_3 + cnt_4plus
    three_plus_cnt = cnt_3 + cnt_4plus
    
    return {
        'one_order_count': cnt_1,
        'one_order_share': _get_pct('1 Order'),
        'two_orders_count': cnt_2,
        'two_orders_share': _get_pct('2 Orders'),
        'three_orders_count': cnt_3,
        'three_orders_share': _get_pct('3 Orders'),
        'four_plus_count': cnt_4plus,
        'four_plus_share': _get_pct('4+ Orders'),
        'repeat_count': rep_cnt,
        'repeat_share': float((rep_cnt / tot * 100) if tot > 0 else 0.0),
        'three_plus_count': three_plus_cnt,
        'three_plus_share': float((three_plus_cnt / tot * 100) if tot > 0 else 0.0),
        'total_customers': tot
    }
