import streamlit as st
import os
from analytics.data_loader import load_analytical_data, apply_global_filters
from analytics.sales import (
    get_executive_kpis,
    get_monthly_orders_and_revenue,
    get_orders_by_weekday,
    get_payment_method_distribution,
    get_top_states_by_revenue,
    get_non_delivered_orders
)
from analytics.insights import generate_sales_insights
from components.header import render_header
from components.kpi_cards import render_kpi_cards
from components.insight_cards import render_insight_card, render_summary_banner
from components.charts import (
    create_monthly_combo_chart,
    create_weekday_bar_chart,
    create_payment_donut_chart,
    create_horizontal_bar,
    create_non_delivered_donut
)
from utils.formatting import format_currency, format_number

def render_page_1():
    # Load CSS if not already loaded
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # Load Master Data
    orders_master, items_master, payments_master = load_analytical_data()
    
    # Get active filters from session state
    filters = st.session_state.get('filters', {})
    
    # Filter Data
    orders_df, items_df, payments_df = apply_global_filters(
        orders_master, items_master, payments_master, filters
    )
    
    # Render Header
    render_header(
        page_title="Business Performance & Sales Trends",
        page_subtitle="Executive overview answering: How is the overall business and sales volume performing?",
        active_filters=filters
    )
    
    # Compute KPIs
    kpis = get_executive_kpis(orders_df, items_df, payments_df)
    
    # Render KPI Cards
    render_kpi_cards([
        {
            'label': 'Total Orders',
            'value': format_number(kpis['total_orders']),
            'sub': 'All sales channels',
            'icon': '📦',
            'color': '#6366F1'
        },
        {
            'label': 'Total Revenue',
            'value': format_currency(kpis['total_revenue']),
            'sub': 'Gross transaction value',
            'icon': '💳',
            'color': '#10B981'
        },
        {
            'label': 'Unique Customers',
            'value': format_number(kpis['unique_customers']),
            'sub': 'Distinct buyer accounts',
            'icon': '👥',
            'color': '#38BDF8'
        },
        {
            'label': 'Avg Order Value',
            'value': format_currency(kpis['aov']),
            'sub': 'Per transaction basket',
            'icon': '📊',
            'color': '#F59E0B'
        },
        {
            'label': 'Products Sold',
            'value': format_number(kpis['products_sold']),
            'sub': 'Individual order items',
            'icon': '🏷️',
            'color': '#8B5CF6'
        }
    ])
    
    # Calculations for Visuals
    monthly_df = get_monthly_orders_and_revenue(orders_df)
    weekday_df = get_orders_by_weekday(orders_df)
    payment_df = get_payment_method_distribution(payments_df)
    state_df = get_top_states_by_revenue(orders_df, top_n=10)
    non_deliv_df = get_non_delivered_orders(orders_df)
    
    # Generate Insights
    insights = generate_sales_insights(kpis, monthly_df, weekday_df, payment_df, state_df, non_deliv_df)
    
    # Executive Summary Banner
    exec_summary = insights['executive_summary']
    render_summary_banner(
        title=exec_summary['title'],
        text=f"{exec_summary['finding']} {exec_summary['evidence']} {exec_summary['interpretation']}",
        icon="📋"
    )
    
    # Visual 1: Monthly Orders & Payment Value (Full Width)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 1 &bull; Monthly Orders & Payment Value</h3>
        <div class="chart-subtitle">Dual-axis chronological trend comparing transaction count (bars) and gross revenue (line).</div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_monthly = create_monthly_combo_chart(monthly_df)
    st.plotly_chart(fig_monthly, use_container_width=True)
    render_insight_card(insights['monthly_trend'])
    
    with st.expander("🔍 Deep Dive: Monthly Sales Trend Analysis"):
        st.markdown(f"""
        - **Growth Velocity:** Order volume scaled consistently throughout 2017, culminating in strong peak performance in late 2017 and mid-2018.
        - **Revenue Synchronization:** Gross payment values track order volume closely, indicating steady basket sizes rather than episodic high-ticket volatility.
        - **Seasonality & Promotional Drivers:** Notable spikes coincide with major retail promotional events (such as November Black Friday).
        """)
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 2: Visual 2 (Orders by Day of Week) & Visual 3 (Payment Method Distribution)
    col_w, col_p = st.columns(2)
    
    with col_w:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 2 &bull; Orders by Day of Week</h3>
            <div class="chart-subtitle">Distribution of order purchases from Monday to Sunday.</div>
        </div>
        """, unsafe_allow_html=True)
        fig_week = create_weekday_bar_chart(weekday_df)
        st.plotly_chart(fig_week, use_container_width=True)
        render_insight_card(insights['orders_by_weekday'])
        
    with col_p:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 3 &bull; Payment Method Distribution</h3>
            <div class="chart-subtitle">Breakdown of gross transaction revenue by payment instrument.</div>
        </div>
        """, unsafe_allow_html=True)
        fig_pmt = create_payment_donut_chart(payment_df)
        st.plotly_chart(fig_pmt, use_container_width=True)
        render_insight_card(insights['payment_distribution'])
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 3: Visual 4 (Revenue by State) & Visual 5 (Non-Delivered Orders by Status)
    col_s, col_nd = st.columns(2)
    
    with col_s:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 4 &bull; Revenue by Customer State — Top 10</h3>
            <div class="chart-subtitle">Gross revenue concentration among the top 10 Brazilian states.</div>
        </div>
        """, unsafe_allow_html=True)
        fig_state = create_horizontal_bar(state_df, 'customer_state', 'total_revenue', "Revenue by Customer State", "Revenue (R$)", color='#6366F1')
        st.plotly_chart(fig_state, use_container_width=True)
        render_insight_card(insights['revenue_by_state'])
        
    with col_nd:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 5 &bull; Non-Delivered Orders by Status</h3>
            <div class="chart-subtitle">Operational status breakdown for unfulfilled or in-transit orders.</div>
        </div>
        """, unsafe_allow_html=True)
        fig_nd = create_non_delivered_donut(non_deliv_df)
        st.plotly_chart(fig_nd, use_container_width=True)
        render_insight_card(insights['non_delivered_orders'], card_type="warning")

render_page_1()
