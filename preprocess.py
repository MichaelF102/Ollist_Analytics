import os
import pandas as pd
import numpy as np

STATE_TO_REGION = {
    'AC': 'North', 'AP': 'North', 'AM': 'North', 'PA': 'North', 'RO': 'North', 'RR': 'North', 'TO': 'North',
    'AL': 'Northeast', 'BA': 'Northeast', 'CE': 'Northeast', 'MA': 'Northeast', 'PB': 'Northeast',
    'PE': 'Northeast', 'PI': 'Northeast', 'RN': 'Northeast', 'SE': 'Northeast',
    'DF': 'Central-West', 'GO': 'Central-West', 'MT': 'Central-West', 'MS': 'Central-West',
    'ES': 'Southeast', 'MG': 'Southeast', 'RJ': 'Southeast', 'SP': 'Southeast',
    'PR': 'South', 'RS': 'South', 'SC': 'South'
}

CATEGORY_MAP_CLEAN = {
    'bed_bath_table': 'Bed & Bath & Table',
    'health_beauty': 'Health & Beauty',
    'sports_leisure': 'Sports & Leisure',
    'furniture_decor': 'Furniture & Decor',
    'computers_accessories': 'Computers & Accessories',
    'housewares': 'Housewares',
    'watches_gifts': 'Watches & Gifts',
    'telephony': 'Telephony',
    'garden_tools': 'Garden & Tools',
    'auto': 'Auto',
    'toys': 'Toys',
    'cool_stuff': 'Cool & Stuff',
    'perfumery': 'Perfumery',
    'baby': 'Baby',
    'electronics': 'Electronics',
    'stationery': 'Stationery',
    'fashion_bags_accessories': 'Fashion Bags & Accessories',
    'pet_shop': 'Pet Shop',
    'office_furniture': 'Office Furniture',
    'luggage_accessories': 'Luggage & Accessories'
}

def clean_category_name(cat_eng, cat_raw):
    if pd.isna(cat_eng) and pd.isna(cat_raw):
        return 'Other / Uncategorized'
    key = str(cat_eng if pd.notna(cat_eng) else cat_raw).strip().lower()
    if key in CATEGORY_MAP_CLEAN:
        return CATEGORY_MAP_CLEAN[key]
    # General title-casing
    return key.replace('_', ' ').title()

def preprocess_and_cache(raw_dir='data/raw', processed_dir='data/processed'):
    os.makedirs(processed_dir, exist_ok=True)
    print("Loading raw CSV files...")
    orders = pd.read_csv(os.path.join(raw_dir, 'olist_orders_dataset.csv'))
    customers = pd.read_csv(os.path.join(raw_dir, 'olist_customers_dataset.csv'))
    items = pd.read_csv(os.path.join(raw_dir, 'olist_order_items_dataset.csv'))
    payments = pd.read_csv(os.path.join(raw_dir, 'olist_order_payments_dataset.csv'))
    reviews = pd.read_csv(os.path.join(raw_dir, 'olist_order_reviews_dataset.csv'))
    products = pd.read_csv(os.path.join(raw_dir, 'olist_products_dataset.csv'))
    sellers = pd.read_csv(os.path.join(raw_dir, 'olist_sellers_dataset.csv'))
    trans = pd.read_csv(os.path.join(raw_dir, 'product_category_name_translation.csv'))

    print("Processing timestamps and calendar fields...")
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date']
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')

    orders['purchase_date'] = orders['order_purchase_timestamp'].dt.date
    orders['year'] = orders['order_purchase_timestamp'].dt.year
    orders['quarter'] = 'Q' + orders['order_purchase_timestamp'].dt.quarter.astype(str)
    orders['year_quarter'] = orders['year'].astype(str) + '-' + orders['quarter']
    orders['month'] = orders['order_purchase_timestamp'].dt.month
    orders['year_month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
    orders['weekday'] = orders['order_purchase_timestamp'].dt.day_name()
    orders['purchase_hour'] = orders['order_purchase_timestamp'].dt.hour
    
    # 4-hour time windows
    bins = [-1, 3, 7, 11, 15, 19, 24]
    labels = ['00-03', '04-07', '08-11', '12-15', '16-19', '20-23']
    orders['purchase_time_window'] = pd.cut(orders['purchase_hour'], bins=bins, labels=labels)

    # Delivery performance calculations
    orders['deliv_time_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400.0
    orders['carrier_handoff_days'] = (orders['order_delivered_carrier_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400.0
    
    # Calendar days late
    orders['cal_late_days'] = (orders['order_delivered_customer_date'].dt.floor('d') - orders['order_estimated_delivery_date'].dt.floor('d')).dt.days
    
    orders['is_delivered'] = orders['order_status'] == 'delivered'
    orders['is_late'] = orders['is_delivered'] & (orders['cal_late_days'] > 0)
    
    def calc_outcome(row):
        if row['order_status'] != 'delivered':
            return 'Not delivered'
        elif row['cal_late_days'] > 0:
            return 'Late'
        else:
            return 'On time'
    orders['delivery_outcome'] = orders.apply(calc_outcome, axis=1)

    def calc_delay_bucket(row):
        if not row['is_delivered']:
            return 'Not Delivered'
        days = row['cal_late_days']
        if pd.isna(days) or days <= 0:
            return 'On time / early'
        elif days <= 3:
            return '1-3 days late'
        elif days <= 7:
            return '4-7 days late'
        else:
            return '8+ days late'
    orders['delay_bucket'] = orders.apply(calc_delay_bucket, axis=1)

    print("Merging customer details...")
    orders = orders.merge(customers[['customer_id', 'customer_unique_id', 'customer_city', 'customer_state']], on='customer_id', how='left')
    orders['customer_region'] = orders['customer_state'].map(STATE_TO_REGION).fillna('Other')

    print("Aggregating order payments...")
    order_pmt = payments.groupby('order_id').agg(
        total_payment=('payment_value', 'sum'),
        payment_installments=('payment_installments', 'max'),
        payment_types_count=('payment_type', 'nunique')
    ).reset_index()
    # Find dominant payment method for each order
    pmt_dominant = payments.sort_values('payment_value', ascending=False).drop_duplicates('order_id')[['order_id', 'payment_type']]
    pmt_dominant.rename(columns={'payment_type': 'primary_payment_type'}, inplace=True)
    order_pmt = order_pmt.merge(pmt_dominant, on='order_id', how='left')

    orders = orders.merge(order_pmt, on='order_id', how='left')
    orders['total_payment'] = orders['total_payment'].fillna(0.0)
    orders['primary_payment_type'] = orders['primary_payment_type'].fillna('not_defined')

    print("Aggregating reviews...")
    # Some orders have multiple reviews, we take average review score
    order_rev = reviews.groupby('order_id').agg(
        review_score=('review_score', 'mean'),
        reviews_count=('review_id', 'count')
    ).reset_index()
    orders = orders.merge(order_rev, on='order_id', how='left')
    orders['is_low_rating'] = orders['review_score'] <= 2

    # Map product category names
    print("Processing products and translations...")
    prod = products.merge(trans, on='product_category_name', how='left')
    prod['category_clean'] = prod.apply(lambda r: clean_category_name(r['product_category_name_english'], r['product_category_name']), axis=1)

    print("Processing items master...")
    items_master = items.merge(
        orders[['order_id', 'customer_id', 'customer_unique_id', 'order_status', 
                'order_purchase_timestamp', 'year', 'quarter', 'year_quarter', 'month', 'year_month',
                'weekday', 'purchase_hour', 'purchase_time_window', 'cal_late_days', 'is_delivered', 
                'is_late', 'delivery_outcome', 'delay_bucket', 'customer_city', 'customer_state', 
                'customer_region', 'review_score', 'is_low_rating']],
        on='order_id', how='left'
    )
    items_master = items_master.merge(
        prod[['product_id', 'category_clean', 'product_weight_g']],
        on='product_id', how='left'
    )
    items_master['category_clean'] = items_master['category_clean'].fillna('Other / Uncategorized')

    items_master = items_master.merge(
        sellers[['seller_id', 'seller_city', 'seller_state']],
        on='seller_id', how='left'
    )
    items_master['seller_region'] = items_master['seller_state'].map(STATE_TO_REGION).fillna('Other')

    # Payments master with order details
    print("Processing payments master...")
    payments_master = payments.merge(
        orders[['order_id', 'order_status', 'year', 'quarter', 'year_month', 'customer_state', 'customer_region']],
        on='order_id', how='left'
    )

    # Standardize payment type labels
    pmt_name_map = {
        'credit_card': 'Credit Card',
        'boleto': 'Boleto',
        'voucher': 'Voucher',
        'debit_card': 'Debit Card',
        'not_defined': 'Not Defined'
    }
    payments_master['payment_type_clean'] = payments_master['payment_type'].map(lambda x: pmt_name_map.get(str(x).lower(), str(x).title()))
    orders['primary_payment_clean'] = orders['primary_payment_type'].map(lambda x: pmt_name_map.get(str(x).lower(), str(x).title()))

    print("Saving processed Parquet files...")
    orders.to_parquet(os.path.join(processed_dir, 'orders_master.parquet'), index=False)
    items_master.to_parquet(os.path.join(processed_dir, 'items_master.parquet'), index=False)
    payments_master.to_parquet(os.path.join(processed_dir, 'payments_master.parquet'), index=False)
    print("Preprocessing completed successfully!")

if __name__ == '__main__':
    preprocess_and_cache()
