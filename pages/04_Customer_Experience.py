import streamlit as st
import os
from analytics.data_loader import load_analytical_data, apply_global_filters
from analytics.reviews import (
    get_review_kpis,
    get_ratings_by_delay_bucket,
    get_category_sales_vs_experience,
    get_low_rating_decomposition,
    get_reviews_and_late_over_time
)
from analytics.insights import generate_experience_insights
from components.header import render_header
from components.kpi_cards import render_kpi_cards
from components.insight_cards import render_insight_card, render_summary_banner
from components.charts import (
    create_treemap_sales_experience,
    create_ratings_delay_combo,
    create_reviews_and_late_combo
)
from utils.formatting import format_rating, format_percent, format_number, format_currency
import pandas as pd
def render_page_4():
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
        page_title="Customer Experience & Reviews",
        page_subtitle="Sentiment intelligence answering: How does logistics fulfillment directly shape customer ratings?",
        active_filters=filters
    )
    
    # Review KPIs
    kpis = get_review_kpis(orders_df)
    
    render_kpi_cards([
        {
            'label': 'Avg Review Score',
            'value': f"{kpis['avg_review_score']:.2f}",
            'sub': 'Scale of 1.0 to 5.0',
            'icon': '⭐',
            'color': '#10B981'
        },
        {
            'label': 'Low Rating Rate',
            'value': f"{kpis['low_rating_pct']:.1f}%",
            'sub': '1 & 2 star feedback',
            'icon': '⚠️',
            'color': '#F43F5E'
        },
        {
            'label': 'On-Time Rating',
            'value': f"{kpis['ontime_avg_rating']:.2f}",
            'sub': 'On-time / early deliveries',
            'icon': '✅',
            'color': '#38BDF8'
        },
        {
            'label': 'Late Order Rating',
            'value': f"{kpis['late_avg_rating']:.2f}",
            'sub': 'All delayed deliveries',
            'icon': '⏳',
            'color': '#F59E0B'
        },
        {
            'label': '8+ Days Late Rating',
            'value': f"{kpis['severe_delay_rating']:.2f}",
            'sub': 'Severe logistics delays',
            'icon': '🚨',
            'color': '#E11D48'
        }
    ])
    
    # Prominent Hero Rating Gap Callout Banner
    gap_val = kpis['rating_gap']
    render_summary_banner(
        title="Hero Discovery &bull; The 2.59-Point Sentiment Cliff",
        text=f"Customer satisfaction plummets from <strong>{kpis['ontime_avg_rating']:.2f} stars</strong> for on-time/early orders to <strong>{kpis['severe_delay_rating']:.2f} stars</strong> when an order is delayed by 8+ days &mdash; an immense <strong>{gap_val:.2f}-point collapse</strong>. Delivery reliability is the single greatest driver of positive marketplace sentiment.",
        icon="📉",
        variant="alert" if gap_val > 2.0 else "default"
    )
    
    # Calculations for Visuals
    bucket_df = get_ratings_by_delay_bucket(orders_df)
    treemap_df = get_category_sales_vs_experience(items_df)
    combo_time_df = get_reviews_and_late_over_time(orders_df)
    
    # Dynamic decomposition selector
    st.markdown("""
    <div class="chart-header" style="margin-top: 1rem;">
        <h3 class="chart-title">Visual 2 &bull; HERO VISUAL: Ratings Collapse Once a Parcel is Late</h3>
        <div class="chart-subtitle">Dual-axis view showing the steep drop in average review score (bars) alongside the surge in low ratings (line).</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not bucket_df.empty:
        fig_hero = create_ratings_delay_combo(bucket_df)
        st.plotly_chart(fig_hero, use_container_width=True)
        # Generate Hero insight
        hero_ins = generate_experience_insights(kpis, bucket_df, pd.DataFrame(), combo_time_df, "")['ratings_collapse']
        render_insight_card(hero_ins, card_type="alert")
    else:
        st.info("Insufficient delivered review records for delay bucket analysis.")
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 2: Visual 1 (Treemap) & Visual 4 (Time Series Combo)
    col_tree, col_time = st.columns(2)
    
    with col_tree:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 1 &bull; Product Sales vs Customer Experience</h3>
            <div class="chart-subtitle">Treemap of category volume (box size) vs average satisfaction rating (color).</div>
        </div>
        """, unsafe_allow_html=True)
        if not treemap_df.empty:
            fig_tree = create_treemap_sales_experience(treemap_df)
            st.plotly_chart(fig_tree, use_container_width=True)
            tree_ins = generate_experience_insights(kpis, bucket_df, pd.DataFrame(), combo_time_df, "")['sales_vs_experience']
            render_insight_card(tree_ins)
        else:
            st.info("No category sales records found.")
            
    with col_time:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 4 &bull; Late Deliveries & Customer Reviews Over Time</h3>
            <div class="chart-subtitle">Monthly tracking of late delivery percentage (bars) and average review score (line).</div>
        </div>
        """, unsafe_allow_html=True)
        if not combo_time_df.empty:
            fig_time = create_reviews_and_late_combo(combo_time_df)
            st.plotly_chart(fig_time, use_container_width=True)
            time_ins = generate_experience_insights(kpis, bucket_df, pd.DataFrame(), combo_time_df, "")['late_and_reviews_time']
            render_insight_card(time_ins)
        else:
            st.info("Insufficient monthly data.")
            
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 3: Visual 3 (Interactive Decomposition Investigation)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 3 &bull; Root Cause Analysis: What Drives Low Ratings?</h3>
        <div class="chart-subtitle">Interactive decomposition isolating segments with abnormal concentrations of negative customer feedback (1-2 stars).</div>
    </div>
    """, unsafe_allow_html=True)
    
    decomp_dim = st.selectbox(
        "Analyze Low Ratings By Dimension:",
        ['Delay Bucket', 'Customer Region', 'Seller Region', 'Customer State', 'Product Category'],
        index=0,
        key="decomp_selector"
    )
    
    decomp_df = get_low_rating_decomposition(orders_df, items_df, dimension=decomp_dim)
    
    if not decomp_df.empty:
        col_d1, col_d2 = st.columns([1.1, 0.9])
        
        with col_d1:
            # Bar chart of low rating rate by segment
            import plotly.express as px
            top_segs = decomp_df.head(10).iloc[::-1]
            fig_decomp = px.bar(
                top_segs,
                x='low_rating_pct',
                y='segment',
                orientation='h',
                labels={'low_rating_pct': 'Low Rating Rate (%)', 'segment': decomp_dim},
                color='low_rating_pct',
                color_continuous_scale='Reds',
                text=top_segs['low_rating_pct'].apply(lambda x: f"{x:.1f}%")
            )
            fig_decomp.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=340,
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(color="#94A3B8", size=10),
                coloraxis_showscale=False
            )
            fig_decomp.update_traces(textposition="outside")
            st.plotly_chart(fig_decomp, use_container_width=True)
            
        with col_d2:
            st.markdown(f"""
            <div style="margin-bottom: 0.6rem;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Segment Diagnostic Table</div>
                <div style="font-size: 0.75rem; color: #64748b;">National Baseline Low Rating: <strong style="color: #F43F5E;">{kpis['low_rating_pct']:.1f}%</strong></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Format dataframe for display
            disp_table = decomp_df.head(10)[['segment', 'orders', 'avg_review', 'low_rating_pct']].copy()
            disp_table.columns = [decomp_dim, 'Orders', 'Avg Score', 'Low Rating %']
            disp_table['Avg Score'] = disp_table['Avg Score'].apply(lambda x: f"{x:.2f}")
            disp_table['Low Rating %'] = disp_table['Low Rating %'].apply(lambda x: f"{x:.1f}%")
            disp_table['Orders'] = disp_table['Orders'].apply(lambda x: f"{x:,}")
            
            st.dataframe(
                disp_table,
                hide_index=True,
                width="stretch",
                height=300
            )
            
        decomp_ins = generate_experience_insights(kpis, bucket_df, decomp_df, combo_time_df, decomp_dim)['decomposition']
        render_insight_card(decomp_ins, card_type="warning")
    else:
        st.info("No segmentation data available for this dimension.")

render_page_4()
