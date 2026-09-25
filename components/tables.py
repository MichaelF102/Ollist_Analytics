import streamlit as st
import pandas as pd
from utils.formatting import format_currency, format_number, format_percent

def render_category_performance_table(table_df):
    """
    Renders a formatted analytical table for Product Category Performance
    with totals row and compact monetary/volume formatting.
    """
    if table_df.empty:
        st.info("No category data available for current selection.")
        return
        
    # Calculate Totals
    tot_sales = table_df['product_sales'].sum()
    tot_prods = table_df['products_sold'].sum()
    tot_orders = table_df['orders'].sum()
    overall_avg_sales = (tot_sales / tot_orders) if tot_orders > 0 else 0
    
    # Format display DataFrame
    display_df = pd.DataFrame()
    display_df['Category'] = table_df['category_clean']
    display_df['Product Sales'] = table_df['product_sales'].apply(lambda x: format_currency(x, decimals=2))
    display_df['Avg Sales / Order'] = table_df['avg_sales_per_order'].apply(lambda x: format_currency(x, decimals=2))
    display_df['Products Sold'] = table_df['products_sold'].apply(lambda x: f"{x:,}")
    display_df['Orders'] = table_df['orders'].apply(lambda x: f"{x:,}")
    display_df['Revenue Share'] = table_df['revenue_share'].apply(lambda x: f"{x:.1f}%")
    
    # Append Total row
    totals_row = pd.DataFrame([{
        'Category': 'TOTAL / OVERALL',
        'Product Sales': format_currency(tot_sales, decimals=2),
        'Avg Sales / Order': format_currency(overall_avg_sales, decimals=2),
        'Products Sold': f"{tot_prods:,}",
        'Orders': f"{tot_orders:,}",
        'Revenue Share': '100.0%'
    }])
    
    display_df = pd.concat([display_df, totals_row], ignore_index=True)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=min(480, (len(display_df) + 1) * 35 + 40)
    )
