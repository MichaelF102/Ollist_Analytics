import streamlit as st
import os
from analytics.data_loader import load_analytical_data, apply_global_filters
from analytics.sales import (
    get_executive_kpis,
    get_monthly_orders_and_revenue,
    get_orders_by_weekday,
    get_payment_method_distribution,
    get_top_states_by_revenue,
    get_non_delivered_orders,
    get_monthly_statistics,
    get_weekday_statistics,
    get_payment_statistics,
    get_state_revenue_statistics,
    get_order_status_statistics
)
from analytics.insights import generate_sales_insights
from components.header import render_header
from components.kpi_cards import render_kpi_cards, render_metric_strip
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
    
    # Top Control Bar: Header & Presentation Mode Toggle
    head_col, toggle_col = st.columns([0.75, 0.25])
    with head_col:
        render_header(
            page_title="Business Performance & Sales Trends",
            page_subtitle="Executive overview answering: How is the overall business and sales volume performing?",
            active_filters=filters
        )
    with toggle_col:
        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
        presentation_mode = st.toggle(
            "🎤 Presentation Mode",
            value=False,
            help="Enable presenter talking points, expanded analytical narratives, and presentation prompts."
        )
        if presentation_mode:
            st.caption("Active: Presenter guidance & narrative scripts enabled.")
    
    # Compute KPIs
    kpis = get_executive_kpis(orders_df, items_df, payments_df)
    
    # 1. EXECUTIVE STORY PRESENTATION INTRODUCTION
    tot_orders_fmt = format_number(kpis['total_orders'])
    tot_rev_fmt = format_currency(kpis['total_revenue'])
    
    with st.expander("🎯 Executive Story &bull; Business Performance Narrative", expanded=True):
        st.markdown(f"""
        <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6;">
            <p style="margin-bottom: 0.5rem; font-weight: 600; color: #f8fafc;">
                "I’ll start with the overall business performance of Olist. This page answers four important questions: 
                <em>How much are we selling? How frequently are customers ordering? Where is the revenue coming from? And what patterns can we see in the business over time?</em>"
            </p>
            <p style="margin: 0; color: #94a3b8;">
                The dashboard covers approximately <strong style="color: #38bdf8;">{tot_orders_fmt} orders</strong> and generates around <strong style="color: #10b981;">{tot_rev_fmt} in revenue</strong>, 
                giving us a high-level view of the commercial performance of the platform across the active selection.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 2. KPI CARDS — BUSINESS SCALE
    orders_per_cust = (kpis['total_orders'] / kpis['unique_customers']) if kpis['unique_customers'] > 0 else 0.0
    items_per_order = (kpis['products_sold'] / kpis['total_orders']) if kpis['total_orders'] > 0 else 0.0
    
    render_kpi_cards([
        {
            'label': 'Total Orders',
            'value': format_number(kpis['total_orders']),
            'sub': f'Approx. {tot_orders_fmt} orders in selection',
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
            'sub': f'{orders_per_cust:.2f} orders / buyer',
            'icon': '👥',
            'color': '#38BDF8'
        },
        {
            'label': 'Avg Order Value',
            'value': format_currency(kpis['aov']),
            'sub': 'Typical transaction benchmark',
            'icon': '📊',
            'color': '#F59E0B'
        },
        {
            'label': 'Products Sold',
            'value': format_number(kpis['products_sold']),
            'sub': f'{items_per_order:.2f} items / order',
            'icon': '🏷️',
            'color': '#8B5CF6'
        }
    ])
    
    if presentation_mode:
        st.info(
            f"🎤 **Presenter Talking Point &bull; Business Scale:** "
            f"We have approximately {tot_orders_fmt} orders, representing the transaction volume covered by the current selection. "
            f"These orders generated approximately {tot_rev_fmt} in total payment value across approximately {format_number(kpis['unique_customers'])} unique customers. "
            f"The average order value is approximately {format_currency(kpis['aov'])}, providing a benchmark for the value of a typical transaction. "
            f"Meanwhile, approximately {format_number(kpis['products_sold'])} individual order items were sold. "
            f"Products sold exceeds total orders ({items_per_order:.2f} items/order) because a single order may contain multiple items. "
            f"The relationship between orders and unique customers ({orders_per_cust:.2f} orders/customer) indicates the extent of repeat purchasing in the dataset."
        )
    
    # Statistical Calculations for Visuals
    monthly_df = get_monthly_orders_and_revenue(orders_df)
    weekday_df = get_orders_by_weekday(orders_df)
    payment_df = get_payment_method_distribution(payments_df)
    state_df = get_top_states_by_revenue(orders_df, top_n=10)
    non_deliv_df = get_non_delivered_orders(orders_df)
    
    # Statistical Summary Objects
    m_stats = get_monthly_statistics(monthly_df)
    w_stats = get_weekday_statistics(weekday_df)
    p_stats = get_payment_statistics(payment_df)
    s_stats = get_state_revenue_statistics(state_df, total_revenue=kpis.get('total_revenue'))
    o_stats = get_order_status_statistics(non_deliv_df)
    
    # Generate Insights
    insights = generate_sales_insights(kpis, monthly_df, weekday_df, payment_df, state_df, non_deliv_df)
    
    # 3. VISUAL 1 — MONTHLY ORDERS AND PAYMENT VALUE
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 1 &bull; Monthly Orders & Payment Value</h3>
        <div class="chart-subtitle">Monthly transaction volume and payment value across the observation period.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Numbers Strip for Visual 1
    render_metric_strip([
        {'label': 'Peak Orders', 'value': format_number(m_stats['peak_orders']), 'sub': m_stats['peak_order_month'], 'color': '#38BDF8'},
        {'label': 'Peak Revenue', 'value': format_currency(m_stats['peak_revenue']), 'sub': m_stats['peak_rev_month'], 'color': '#10B981'},
        {'label': 'Lowest Activity', 'value': format_number(m_stats['lowest_orders']), 'sub': m_stats['lowest_order_month'], 'color': '#F59E0B'},
        {'label': 'Orders/Rev Correlation', 'value': f"{m_stats['correlation']:.2f}", 'sub': m_stats['corr_strength'].title(), 'color': '#A855F7'}
    ])
    
    fig_monthly = create_monthly_combo_chart(monthly_df)
    st.plotly_chart(fig_monthly, use_container_width=True)
    render_insight_card(insights['monthly_trend'])
    
    # Dynamic Deep Dive (no hard-coded claims)
    with st.expander("🔍 Deep Dive: Monthly Sales Trend Analysis", expanded=presentation_mode):
        st.markdown(f"""
        - **Peak Month:** **{m_stats['peak_order_month']}** recorded the highest monthly order volume ({format_number(m_stats['peak_orders'])} orders).
        - **Peak Revenue Month:** **{m_stats['peak_rev_month']}** generated the highest monthly payment value ({format_currency(m_stats['peak_revenue'])}).
        - **Lowest Activity:** **{m_stats['lowest_order_month']}** had the lowest recorded monthly orders ({format_number(m_stats['lowest_orders'])} orders).
        - **Order/Revenue Relationship:** Monthly order volume and payment value demonstrate a **{m_stats['corr_strength']} relationship** (r = {m_stats['correlation']:.2f}). This indicates that revenue expansion across the timeline is substantially associated with increasing transaction volume.
        """)
        
    if presentation_mode:
        st.info(
            f"🎤 **Presenter Talking Point &bull; Time-Based Patterns:** "
            f"Order activity changes substantially across the observation period, with the strongest activity occurring during {m_stats['peak_order_month']}. "
            f"The highest monthly volume reached {format_number(m_stats['peak_orders'])} orders in {m_stats['peak_order_month']}, while highest payment value reached {format_currency(m_stats['peak_revenue'])} in {m_stats['peak_rev_month']}. "
            f"The close relationship between order volume and revenue (r = {m_stats['correlation']:.2f}) indicates that sales growth is driven by expanding transaction frequency rather than isolated high-ticket transactions."
        )
        
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
        
        # Key Numbers Strip for Visual 2
        render_metric_strip([
            {'label': 'Highest Day', 'value': w_stats['highest_day'], 'sub': f"{format_number(w_stats['highest_orders'])} orders", 'color': '#38BDF8'},
            {'label': 'Lowest Day', 'value': w_stats['lowest_day'], 'sub': f"{format_number(w_stats['lowest_orders'])} orders", 'color': '#F43F5E'},
            {'label': 'Weekday Total', 'value': format_number(w_stats['weekday_total']), 'sub': f"{w_stats['weekday_share']:.1f}% share", 'color': '#10B981'},
            {'label': 'Weekend Total', 'value': format_number(w_stats['weekend_total']), 'sub': f"{w_stats['weekend_share']:.1f}% share", 'color': '#F59E0B'}
        ])
        
        fig_week = create_weekday_bar_chart(weekday_df)
        st.plotly_chart(fig_week, use_container_width=True)
        render_insight_card(insights['orders_by_weekday'])
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Weekly Timing:** "
                f"Next, I looked at when customers are ordering. Orders are concentrated around {w_stats['highest_day']}, recording approximately {format_number(w_stats['highest_orders'])} orders, "
                f"while {w_stats['lowest_day']} records the lowest order volume at approximately {format_number(w_stats['lowest_orders'])}. "
                f"The observed distribution shows a clear difference between weekday ({w_stats['weekday_share']:.1f}%) and weekend ({w_stats['weekend_share']:.1f}%) ordering activity. "
                f"This type of pattern can be useful for planning customer support, marketing campaigns, inventory availability and operational capacity."
            )
        
    with col_p:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 3 &bull; Payment Method Distribution</h3>
            <div class="chart-subtitle">Breakdown of gross transaction revenue by payment instrument.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Numbers Strip for Visual 3
        render_metric_strip([
            {'label': 'Largest Method', 'value': p_stats['largest_method'], 'sub': f"{p_stats['largest_share']:.1f}% of GMV", 'color': '#38BDF8'},
            {'label': 'Largest Revenue', 'value': format_currency(p_stats['largest_value']), 'sub': 'Primary channel', 'color': '#10B981'},
            {'label': 'Second Method', 'value': p_stats['second_method'], 'sub': f"{p_stats['second_share']:.1f}% share", 'color': '#F59E0B'},
            {'label': 'Top 2 Concentration', 'value': f"{p_stats['top2_share']:.1f}%", 'sub': 'Combined share', 'color': '#A855F7'}
        ])
        
        fig_pmt = create_payment_donut_chart(payment_df)
        st.plotly_chart(fig_pmt, use_container_width=True)
        render_insight_card(insights['payment_distribution'])
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Payment Mix:** "
                f"Examining payment behavior, {p_stats['largest_method']} dominates the payment mix, representing approximately {p_stats['largest_share']:.1f}% of payment value ({format_currency(p_stats['largest_value'])}). "
                f"{p_stats['second_method']} represents approximately {p_stats['second_share']:.1f}%. "
                f"This indicates that payment value is concentrated around a relatively small number of payment methods, making gateway reliability and card authorization critical to revenue flow."
            )
        
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
        
        # Key Numbers Strip for Visual 4
        render_metric_strip([
            {'label': 'Top State', 'value': s_stats['top_state'], 'sub': f"{s_stats['top_share']:.1f}% of total", 'color': '#38BDF8'},
            {'label': 'Top Revenue', 'value': format_currency(s_stats['top_revenue']), 'sub': 'State leader', 'color': '#10B981'},
            {'label': 'Top 3 Share', 'value': f"{s_stats['top3_share']:.1f}%", 'sub': f"{s_stats['top_state']}, {s_stats['top2_state']}, {s_stats['top3_state']}", 'color': '#F59E0B'},
            {'label': 'Top 10 Share', 'value': f"{s_stats['top10_share']:.1f}%", 'sub': 'Of total revenue', 'color': '#A855F7'}
        ])
        
        fig_state = create_horizontal_bar(state_df, 'customer_state', 'total_revenue', "Revenue by Customer State", "Revenue (R$)", color='#6366F1')
        st.plotly_chart(fig_state, use_container_width=True)
        render_insight_card(insights['revenue_by_state'])
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Geography:** "
                f"The next question is where the money is coming from geographically. {s_stats['top_state']} is the largest revenue-generating state, contributing approximately {format_currency(s_stats['top_revenue'])} in revenue, followed by {s_stats['top2_state']} and {s_stats['top3_state']}. "
                f"Revenue is not evenly distributed geographically; the top 10 states account for approximately {s_stats['top10_share']:.1f}% of total observed revenue."
            )
        
    with col_nd:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 5 &bull; Order Status Distribution</h3>
            <div class="chart-subtitle">Operational status breakdown for unfulfilled or in-transit orders.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Numbers Strip for Visual 5
        render_metric_strip([
            {'label': 'Largest Status', 'value': o_stats['largest_status'].title(), 'sub': f"{o_stats['largest_share']:.1f}% share", 'color': '#38BDF8'},
            {'label': 'In-Transit Count', 'value': format_number(o_stats['largest_count']), 'sub': 'Active orders', 'color': '#10B981'},
            {'label': 'Cancelled Orders', 'value': format_number(o_stats['cancelled_count']), 'sub': format_currency(o_stats['cancelled_revenue']), 'color': '#F43F5E'},
            {'label': 'Unavailable Stock', 'value': format_number(o_stats['unavailable_count']), 'sub': format_currency(o_stats['unavailable_revenue']), 'color': '#F59E0B'}
        ])
        
        fig_nd = create_non_delivered_donut(non_deliv_df)
        st.plotly_chart(fig_nd, use_container_width=True)
        render_insight_card(insights['non_delivered_orders'], card_type="warning")
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Operational Status:** "
                f"Finally, I want to look at the operational side of the business. Not every order progresses to the same operational state. This chart breaks down the order population by status. "
                f"The largest segment is '{o_stats['largest_status']}' ({format_number(o_stats['largest_count'])} orders, {o_stats['largest_share']:.1f}%), while cancelled ({format_number(o_stats['cancelled_count'])}) and unavailable ({format_number(o_stats['unavailable_count'])}) orders represent important sources of potential revenue leakage."
            )
            
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # 9. PAGE-LEVEL EXECUTIVE SUMMARY / TAKEAWAY
    exec_summary = insights['executive_summary']
    render_summary_banner(
        title=f"📋 {exec_summary['title']}",
        text=f"{exec_summary['finding']} {exec_summary['evidence']} {exec_summary['interpretation']} {exec_summary['business_implication']}",
        icon="📊",
        variant="default"
    )
    
    # 12. FINAL PAGE TRANSITION TO CUSTOMER INTELLIGENCE
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(56, 189, 248, 0.08) 100%); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 12px; padding: 1.35rem; margin-top: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
            <div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 0.5rem;">
                    <span>➡️</span> From Business Performance to Customer Intelligence
                </div>
                <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 0.35rem; line-height: 1.5;">
                    So far, we have established the commercial scale of the business, the timing of customer orders, payment behavior, geographic revenue concentration and order-status distribution.<br>
                    <strong>The next question is:</strong> <em>Who are these customers, what are they buying, and how is purchasing behavior distributed across Brazil?</em>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
    if st.button("Continue to Customer & Product Intelligence →", use_container_width=True, type="primary"):
        st.switch_page("pages/02_Customer_Product_Intelligence.py")

render_page_1()
