import pandas as pd
import numpy as np

def get_delivery_kpis(orders_df):
    delivered = orders_df[orders_df['is_delivered']].copy()
    total_delivered = len(delivered)
    
    if total_delivered == 0:
        return {
            'avg_delivery_time': 0.0,
            'avg_days_late': 0.0,
            'late_delivery_pct': 0.0,
            'ontime_pct': 0.0,
            'total_delivered': 0
        }
        
    avg_delivery_time = delivered['deliv_time_days'].dropna().mean()
    late_orders = delivered[delivered['is_late']]
    avg_days_late = late_orders['cal_late_days'].dropna().mean() if not late_orders.empty else 0.0
    late_pct = (len(late_orders) / total_delivered * 100)
    ontime_pct = 100.0 - late_pct
    
    return {
        'avg_delivery_time': avg_delivery_time,
        'avg_days_late': avg_days_late,
        'late_delivery_pct': late_pct,
        'ontime_pct': ontime_pct,
        'total_delivered': total_delivered
    }

def get_seller_volume_vs_ontime(items_df, min_orders=5):
    """
    Computes delivered order volume and on-time rate per seller.
    Only considers delivered orders.
    """
    if items_df.empty:
        return pd.DataFrame(columns=['seller_id', 'delivered_orders', 'ontime_pct', 'late_orders'])
    
    deliv_items = items_df[items_df['is_delivered']].copy()
    if deliv_items.empty:
        return pd.DataFrame()
        
    seller_stats = deliv_items.groupby('seller_id').agg(
        delivered_orders=('order_id', 'nunique'),
        late_orders=('is_late', lambda x: x.sum())
    ).reset_index()
    
    # Filter to sellers with at least min_orders to prevent 1-order noise
    seller_stats = seller_stats[seller_stats['delivered_orders'] >= min_orders].copy()
    seller_stats['ontime_pct'] = (1.0 - (seller_stats['late_orders'] / seller_stats['delivered_orders'])) * 100
    seller_stats['ontime_pct'] = seller_stats['ontime_pct'].clip(0, 100)
    
    return seller_stats

def get_carrier_handoff_heatmap(orders_df):
    """
    Computes average carrier handoff days by purchase weekday and purchase time window.
    """
    valid = orders_df.dropna(subset=['weekday', 'purchase_time_window', 'carrier_handoff_days']).copy()
    if valid.empty:
        return pd.DataFrame()
        
    pivot = valid.pivot_table(
        index='weekday',
        columns='purchase_time_window',
        values='carrier_handoff_days',
        aggfunc='mean',
        observed=False
    )
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_cols = ['00-03', '04-07', '08-11', '12-15', '16-19', '20-23']
    
    pivot = pivot.reindex(index=weekday_order, columns=time_cols)
    return pivot.round(1)

def get_ontime_by_state(orders_df):
    """
    Computes on-time percentage by customer state.
    """
    delivered = orders_df[orders_df['is_delivered']].copy()
    if delivered.empty:
        return pd.DataFrame(columns=['customer_state', 'delivered_count', 'ontime_pct', 'late_pct'])
        
    state_perf = delivered.groupby('customer_state').agg(
        delivered_count=('order_id', 'count'),
        late_count=('is_late', 'sum')
    ).reset_index()
    
    state_perf['ontime_pct'] = (1.0 - (state_perf['late_count'] / state_perf['delivered_count'])) * 100
    state_perf['late_pct'] = 100.0 - state_perf['ontime_pct']
    state_perf = state_perf.sort_values('ontime_pct', ascending=False).reset_index(drop=True)
    return state_perf

def get_sankey_route_data(items_df):
    """
    Generates data for Sankey diagram: Buyer Region -> Seller Region -> Delivery Outcome
    And computes route analytics (highest volume route, highest late rate route, highest on-time route).
    """
    if items_df.empty:
        return pd.DataFrame(), {}
        
    valid = items_df[
        (items_df['customer_region'] != 'Other') & 
        (items_df['seller_region'] != 'Other') & 
        items_df['delivery_outcome'].notna()
    ].copy()
    
    # Route level stats: Buyer Region -> Seller Region
    routes = valid.groupby(['customer_region', 'seller_region', 'delivery_outcome']).size().reset_index(name='count')
    
    # Route performance analysis
    route_agg = valid.groupby(['customer_region', 'seller_region']).agg(
        total_shipments=('order_id', 'count'),
        late_shipments=('is_late', 'sum'),
        ontime_shipments=('delivery_outcome', lambda x: (x == 'On time').sum())
    ).reset_index()
    
    route_agg['late_rate'] = (route_agg['late_shipments'] / route_agg['total_shipments'] * 100)
    route_agg['ontime_rate'] = (route_agg['ontime_shipments'] / route_agg['total_shipments'] * 100)
    
    # Identify key routes (filter min 100 shipments for statistical significance)
    sig_routes = route_agg[route_agg['total_shipments'] >= 100]
    if not sig_routes.empty:
        highest_volume = sig_routes.sort_values('total_shipments', ascending=False).iloc[0]
        highest_late = sig_routes.sort_values('late_rate', ascending=False).iloc[0]
        highest_ontime = sig_routes.sort_values('ontime_rate', ascending=False).iloc[0]
    else:
        highest_volume = route_agg.sort_values('total_shipments', ascending=False).iloc[0] if not route_agg.empty else None
        highest_late = highest_volume
        highest_ontime = highest_volume
        
    route_insights = {
        'highest_volume': highest_volume,
        'highest_late': highest_late,
        'highest_ontime': highest_ontime
    }
    
    return routes, route_insights
