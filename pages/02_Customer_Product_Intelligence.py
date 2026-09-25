import streamlit as st
import os
from analytics.data_loader import load_analytical_data, apply_global_filters
from analytics.customers import (
    get_customer_kpis,
    get_customers_by_state,
    get_top_cities_by_customers,
    get_customers_by_order_frequency
)
from analytics.products import (
    get_product_category_performance,
    get_category_performance_table,
    get_category_share_by_region
)
from analytics.insights import generate_customer_insights, generate_product_insights
from components.header import render_header
from components.kpi_cards import render_kpi_cards
from components.insight_cards import render_insight_card, render_summary_banner
from components.charts import (
    create_brazil_map,
    create_horizontal_bar,
    create_category_matrix_heatmap,
    create_order_frequency_bar
)
from components.tables import render_category_performance_table
from utils.formatting import format_number, format_percent

def render_page_2():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # Load Master Data
    orders_master, items_master, payments_master = load_analytical_data()
    filters = st.session_state.get('filters', {})
    
    # Filter Data
    orders_df, items_df, payments_df = apply_global_filters(
        orders_master, items_master, payments_master, filters
    )
    
    # Render Header
    render_header(
        page_title="Customers, Products & Geography",
        page_subtitle="Customer intelligence answering: Who buys, what sells, and where are customers concentrated?",
        active_filters=filters
    )
    
    # Customer KPIs
    kpis = get_customer_kpis(orders_df, items_df)
    
    render_kpi_cards([
        {
            'label': 'Unique Customers',
            'value': format_number(kpis['unique_customers']),
            'sub': 'Distinct buyer accounts',
            'icon': '👥',
            'color': '#38BDF8'
        },
        {
            'label': 'Repeat Customers',
            'value': format_number(kpis['repeat_customers']),
            'sub': '>= 2 orders placed',
            'icon': '🔄',
            'color': '#6366F1'
        },
        {
            'label': 'Repeat Customer Rate',
            'value': f"{kpis['repeat_rate']:.1f}%",
            'sub': 'Repeat / Unique buyers',
            'icon': '🎯',
            'color': '#F59E0B'
        },
        {
            'label': 'Unique Products',
            'value': format_number(kpis['unique_products']),
            'sub': 'SKU catalogue depth',
            'icon': '📦',
            'color': '#10B981'
        },
        {
            'label': 'Unique Categories',
            'value': str(kpis['unique_categories']),
            'sub': 'Merchandise departments',
            'icon': '🗂️',
            'color': '#8B5CF6'
        },
        {
            'label': 'Products Sold',
            'value': format_number(kpis['products_sold']),
            'sub': 'Total units dispatched',
            'icon': '🏷️',
            'color': '#EC4899'
        }
    ])
    
    # Calculations for Visuals
    state_cust_df = get_customers_by_state(orders_df)
    city_cust_df = get_top_cities_by_customers(orders_df, top_n=10)
    freq_df = get_customers_by_order_frequency(orders_df)
    cat_perf_df = get_product_category_performance(items_df, top_n=10)
    cat_region_matrix = get_category_share_by_region(items_df, top_n=9)
    table_df = get_category_performance_table(items_df, top_n=15)
    
    # Insights
    cust_insights = generate_customer_insights(kpis, state_cust_df, city_cust_df, freq_df)
    prod_insights = generate_product_insights(cat_perf_df, cat_region_matrix)
    
    # Top Retention Callout Banner
    retention_ins = cust_insights['customer_retention']
    render_summary_banner(
        title="Key Retention Finding &bull; The ~3.1% Single-Purchase Bottleneck",
        text=f"The marketplace demonstrates a <strong>{kpis['repeat_rate']:.1f}% Repeat Customer Rate</strong> ({format_number(kpis['repeat_customers'])} repeat buyers out of {format_number(kpis['unique_customers'])} unique buyers). The customer base is heavily weighted toward one-time purchasers, creating an immense post-purchase retention opportunity.",
        icon="⚡",
        variant="amber"
    )
    
    # Row 1: Visual 1 (Brazil Map) & Visual 2 (Top 10 Cities)
    col_map, col_city = st.columns([1.1, 0.9])
    
    with col_map:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 1 &bull; Unique Customers by State</h3>
            <div class="chart-subtitle">Geographic customer density across Brazilian states (UF).</div>
        </div>
        """, unsafe_allow_html=True)
        fig_map = create_brazil_map(state_cust_df, 'customer_count', "Unique Customers by State", color_scale="Blues")
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col_city:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 2 &bull; Top 10 Cities by Number of Customers</h3>
            <div class="chart-subtitle">Leading metropolitan areas by unique customer count.</div>
        </div>
        """, unsafe_allow_html=True)
        fig_city = create_horizontal_bar(city_cust_df, 'customer_city', 'customer_count', "Top 10 Cities", "Unique Customers", color='#38BDF8')
        st.plotly_chart(fig_city, use_container_width=True)
        
    render_insight_card(cust_insights['city_concentration'])
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 2: Visual 3 (Category Share by Region Heatmap)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 3 &bull; Category Share by Region</h3>
        <div class="chart-subtitle">Product category preference mix across the five Brazilian macro-regions (% column share).</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not cat_region_matrix.empty:
        fig_matrix = create_category_matrix_heatmap(cat_region_matrix)
        st.plotly_chart(fig_matrix, use_container_width=True)
        render_insight_card(prod_insights['regional_category_variation'])
    else:
        st.info("Insufficient category regional data under active filters.")
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 3: Visual 4 (Product Category Performance) & Visual 5 (Order Frequency)
    col_cat, col_freq = st.columns(2)
    
    with col_cat:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 4 &bull; Product Category Performance</h3>
            <div class="chart-subtitle">Top 10 categories ranked by total products sold.</div>
        </div>
        """, unsafe_allow_html=True)
        fig_cat = create_horizontal_bar(cat_perf_df, 'category_clean', 'products_sold', "Top Categories", "Products Sold", color='#6366F1')
        st.plotly_chart(fig_cat, use_container_width=True)
        render_insight_card(prod_insights['category_performance'])
        
    with col_freq:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 5 &bull; Customers by Number of Orders</h3>
            <div class="chart-subtitle">Distribution of customers across purchase count cohorts.</div>
        </div>
        """, unsafe_allow_html=True)
        fig_freq = create_order_frequency_bar(freq_df)
        st.plotly_chart(fig_freq, use_container_width=True)
        render_insight_card(cust_insights['order_frequency'], card_type="warning")
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 4: Visual 6 (Product Category Performance Table)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 6 &bull; Product Category Detailed Performance Matrix</h3>
        <div class="chart-subtitle">Exhaustive financial and transactional metrics for top categories with gross totals.</div>
    </div>
    """, unsafe_allow_html=True)
    
    render_category_performance_table(table_df)

render_page_2()
