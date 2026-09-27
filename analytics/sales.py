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

def get_monthly_statistics(monthly_df):
    """Computes peak, lowest, totals, and correlation statistics from monthly orders and revenue."""
    if monthly_df.empty:
        return {
            'peak_order_month': 'N/A', 'peak_month': 'N/A', 'peak_orders': 0,
            'peak_rev_month': 'N/A', 'peak_revenue_month': 'N/A', 'peak_revenue': 0.0,
            'lowest_order_month': 'N/A', 'lowest_month': 'N/A', 'lowest_orders': 0,
            'lowest_rev_month': 'N/A', 'lowest_revenue': 0.0,
            'correlation': 0.0, 'corr_strength': 'neutral',
            'total_orders': 0, 'total_revenue': 0.0
        }
    peak_ord = monthly_df.loc[monthly_df['orders_count'].idxmax()]
    low_ord = monthly_df.loc[monthly_df['orders_count'].idxmin()]
    peak_rev = monthly_df.loc[monthly_df['revenue'].idxmax()]
    low_rev = monthly_df.loc[monthly_df['revenue'].idxmin()]
    corr = monthly_df['orders_count'].corr(monthly_df['revenue']) if len(monthly_df) > 1 else 0.0
    if pd.isna(corr):
        corr = 0.0
    
    if corr >= 0.7:
        corr_strength = "strong positive"
    elif corr >= 0.4:
        corr_strength = "moderate positive"
    elif corr > 0:
        corr_strength = "slight positive"
    else:
        corr_strength = "weak or inverse"
        
    return {
        'peak_order_month': str(peak_ord['year_month']),
        'peak_month': str(peak_ord['year_month']),
        'peak_orders': int(peak_ord['orders_count']),
        'peak_rev_month': str(peak_rev['year_month']),
        'peak_revenue_month': str(peak_rev['year_month']),
        'peak_revenue': float(peak_rev['revenue']),
        'lowest_order_month': str(low_ord['year_month']),
        'lowest_month': str(low_ord['year_month']),
        'lowest_orders': int(low_ord['orders_count']),
        'lowest_rev_month': str(low_rev['year_month']),
        'lowest_revenue': float(low_rev['revenue']),
        'correlation': float(corr),
        'corr_strength': corr_strength,
        'total_orders': int(monthly_df['orders_count'].sum()),
        'total_revenue': float(monthly_df['revenue'].sum())
    }

def get_weekday_statistics(weekday_df):
    """Computes weekday vs weekend ordering volume, shares, and spreads."""
    if weekday_df.empty or weekday_df['orders_count'].sum() == 0:
        return {
            'highest_day': 'N/A', 'highest_orders': 0, 'highest_share': 0.0,
            'lowest_day': 'N/A', 'lowest_orders': 0, 'lowest_share': 0.0,
            'weekday_total': 0, 'weekend_total': 0,
            'weekday_share': 0.0, 'weekend_share': 0.0,
            'difference': 0
        }
    top_day = weekday_df.sort_values('orders_count', ascending=False).iloc[0]
    bot_day = weekday_df.sort_values('orders_count', ascending=True).iloc[0]
    weekday_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekend_days = ['Saturday', 'Sunday']
    wk_total = weekday_df[weekday_df['weekday'].isin(weekday_days)]['orders_count'].sum()
    we_total = weekday_df[weekday_df['weekday'].isin(weekend_days)]['orders_count'].sum()
    total = weekday_df['orders_count'].sum()
    
    return {
        'highest_day': str(top_day['weekday']),
        'highest_orders': int(top_day['orders_count']),
        'highest_share': float(top_day['share_pct']),
        'lowest_day': str(bot_day['weekday']),
        'lowest_orders': int(bot_day['orders_count']),
        'lowest_share': float(bot_day['share_pct']),
        'weekday_total': int(wk_total),
        'weekend_total': int(we_total),
        'weekday_share': float((wk_total / total * 100) if total > 0 else 0.0),
        'weekend_share': float((we_total / total * 100) if total > 0 else 0.0),
        'difference': int(top_day['orders_count'] - bot_day['orders_count'])
    }

def get_payment_statistics(payment_df):
    """Computes payment instrument concentration, top methods, and values."""
    if payment_df.empty or payment_df['total_value'].sum() == 0:
        return {
            'largest_method': 'N/A', 'largest_value': 0.0, 'largest_share': 0.0,
            'second_method': 'N/A', 'second_value': 0.0, 'second_share': 0.0,
            'total_value': 0.0, 'top2_share': 0.0
        }
    sorted_df = payment_df.sort_values('total_value', ascending=False).reset_index(drop=True)
    p1 = sorted_df.iloc[0]
    p2 = sorted_df.iloc[1] if len(sorted_df) > 1 else p1
    tot = float(sorted_df['total_value'].sum())
    top2_share = float(p1['share_pct'] + (p2['share_pct'] if len(sorted_df) > 1 else 0.0))
    
    return {
        'largest_method': str(p1['payment_type_clean']),
        'largest_value': float(p1['total_value']),
        'largest_share': float(p1['share_pct']),
        'second_method': str(p2['payment_type_clean']) if len(sorted_df) > 1 else 'None',
        'second_value': float(p2['total_value']) if len(sorted_df) > 1 else 0.0,
        'second_share': float(p2['share_pct']) if len(sorted_df) > 1 else 0.0,
        'total_value': tot,
        'top2_share': top2_share
    }

def get_state_revenue_statistics(state_df, total_revenue=None):
    """Computes geographic revenue concentration across top states."""
    if state_df.empty or state_df['total_revenue'].sum() == 0:
        return {
            'top_state': 'N/A', 'top_revenue': 0.0, 'top_share': 0.0,
            'top2_state': 'N/A', 'top3_state': 'N/A',
            'top3_revenue': 0.0, 'top3_share': 0.0,
            'top5_share': 0.0, 'top10_revenue': 0.0, 'top10_share': 0.0
        }
    sorted_df = state_df.sort_values('total_revenue', ascending=False).reset_index(drop=True)
    tot = total_revenue if total_revenue is not None and total_revenue > 0 else float(sorted_df['total_revenue'].sum())
    s1 = sorted_df.iloc[0]
    s2 = sorted_df.iloc[1] if len(sorted_df) > 1 else s1
    s3 = sorted_df.iloc[2] if len(sorted_df) > 2 else s2
    
    top3_rev = float(sorted_df.head(3)['total_revenue'].sum())
    top5_rev = float(sorted_df.head(5)['total_revenue'].sum())
    top10_rev = float(sorted_df.head(10)['total_revenue'].sum())
    
    return {
        'top_state': str(s1['customer_state']),
        'top_revenue': float(s1['total_revenue']),
        'top_state_revenue': float(s1['total_revenue']),
        'top_share': float((s1['total_revenue'] / tot * 100) if tot > 0 else 0.0),
        'top2_state': str(s2['customer_state']),
        'top3_state': str(s3['customer_state']),
        'top3_revenue': top3_rev,
        'top3_share': float((top3_rev / tot * 100) if tot > 0 else 0.0),
        'top5_share': float((top5_rev / tot * 100) if tot > 0 else 0.0),
        'top10_revenue': top10_rev,
        'top10_share': float((top10_rev / tot * 100) if tot > 0 else 0.0)
    }

def get_order_status_statistics(non_deliv_df):
    """Computes breakdown of non-delivered orders and operational stages."""
    if non_deliv_df.empty or non_deliv_df['count'].sum() == 0:
        return {
            'largest_status': 'None', 'largest_count': 0, 'largest_share': 0.0,
            'cancelled_count': 0, 'cancelled_revenue': 0.0, 'cancelled_share': 0.0,
            'unavailable_count': 0, 'unavailable_revenue': 0.0, 'unavailable_share': 0.0,
            'total_count': 0, 'total_revenue_at_risk': 0.0
        }
    sorted_df = non_deliv_df.sort_values('count', ascending=False).reset_index(drop=True)
    top_s = sorted_df.iloc[0]
    total_cnt = int(sorted_df['count'].sum())
    tot_risk = float(sorted_df['revenue_at_risk'].sum())
    
    canc = sorted_df[sorted_df['order_status'] == 'canceled']
    canc_cnt = int(canc['count'].values[0]) if not canc.empty else 0
    canc_rev = float(canc['revenue_at_risk'].values[0]) if not canc.empty else 0.0
    canc_share = float(canc['share_pct'].values[0]) if not canc.empty else 0.0
    
    unavail = sorted_df[sorted_df['order_status'] == 'unavailable']
    unavail_cnt = int(unavail['count'].values[0]) if not unavail.empty else 0
    unavail_rev = float(unavail['revenue_at_risk'].values[0]) if not unavail.empty else 0.0
    unavail_share = float(unavail['share_pct'].values[0]) if not unavail.empty else 0.0
    
    return {
        'largest_status': str(top_s['order_status']),
        'largest_count': int(top_s['count']),
        'largest_share': float(top_s['share_pct']),
        'cancelled_count': canc_cnt,
        'cancelled_revenue': canc_rev,
        'cancelled_share': canc_share,
        'unavailable_count': unavail_cnt,
        'unavailable_revenue': unavail_rev,
        'unavailable_share': unavail_share,
        'total_count': total_cnt,
        'total_revenue_at_risk': tot_risk
    }

