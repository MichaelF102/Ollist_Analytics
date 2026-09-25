import streamlit as st
import os
from analytics.data_loader import load_analytical_data, apply_global_filters
from analytics.delivery import (
    get_delivery_kpis,
    get_seller_volume_vs_ontime,
    get_carrier_handoff_heatmap,
    get_ontime_by_state,
    get_sankey_route_data
)
from analytics.insights import generate_delivery_insights
from components.header import render_header
from components.kpi_cards import render_kpi_cards
from components.insight_cards import render_insight_card, render_summary_banner
from components.charts import (
    create_seller_scatter_chart,
    create_carrier_heatmap,
    create_brazil_map,
    create_sankey_diagram
)
from utils.formatting import format_days, format_number, format_percent

def render_page_3():
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
        page_title="Delivery Performance & Logistics Analytics",
        page_subtitle="Logistics intelligence answering: How efficiently are orders delivered and where are operational friction points?",
        active_filters=filters
    )
    
    # Delivery KPIs
    kpis = get_delivery_kpis(orders_df)
    
    render_kpi_cards([
        {
            'label': 'Avg Delivery Time',
            'value': format_days(kpis['avg_delivery_time']),
            'sub': 'Purchase to customer door',
            'icon': '⏱️',
            'color': '#38BDF8'
        },
        {
            'label': 'Avg Days Late',
            'value': format_days(kpis['avg_days_late']),
            'sub': 'For delayed shipments',
            'icon': '⚠️',
            'color': '#F43F5E'
        },
        {
            'label': 'Late Delivery %',
            'value': f"{kpis['late_delivery_pct']:.1f}%",
            'sub': 'Missed estimated SLA',
            'icon': '🚨',
            'color': '#F59E0B'
        },
        {
            'label': 'On-Time Delivery %',
            'value': f"{kpis['ontime_pct']:.1f}%",
            'sub': 'Met or beat promised SLA',
            'icon': '✅',
            'color': '#10B981'
        },
        {
            'label': 'Delivered Orders',
            'value': format_number(kpis['total_delivered']),
            'sub': 'Completed parcel deliveries',
            'icon': '📦',
            'color': '#6366F1'
        }
    ])
    
    # Calculations for Visuals
    seller_df = get_seller_volume_vs_ontime(items_df, min_orders=5)
    heatmap_df = get_carrier_handoff_heatmap(orders_df)
    state_ontime_df = get_ontime_by_state(orders_df)
    routes_df, route_insights = get_sankey_route_data(items_df)
    
    # Insights
    deliv_insights = generate_delivery_insights(kpis, seller_df, heatmap_df, state_ontime_df, route_insights)
    
    # Operational Alert Banner
    op_alert = deliv_insights['operational_alert']
    render_summary_banner(
        title=op_alert['title'],
        text=f"{op_alert['finding']} {op_alert['evidence']} {op_alert['interpretation']}",
        icon="🚚",
        variant="alert" if kpis['late_delivery_pct'] > 5.0 else "default"
    )
    
    # Row 1: Visual 1 (Seller Volume vs On-Time) & Visual 2 (Carrier Handoff Heatmap)
    col_s, col_h = st.columns(2)
    
    with col_s:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 1 &bull; Seller Volume vs On-Time Delivery %</h3>
            <div class="chart-subtitle">Delivered order volume plotted against on-time compliance rate per merchant.</div>
        </div>
        """, unsafe_allow_html=True)
        if not seller_df.empty:
            fig_seller = create_seller_scatter_chart(seller_df)
            st.plotly_chart(fig_seller, use_container_width=True)
            render_insight_card(deliv_insights['seller_performance'])
        else:
            st.info("No seller data meets the criteria.")
            
    with col_h:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 2 &bull; Purchase Timing vs Carrier Handoff (Days)</h3>
            <div class="chart-subtitle">Average days elapsed from purchase to carrier pickup across weekdays and time windows.</div>
        </div>
        """, unsafe_allow_html=True)
        if not heatmap_df.empty:
            fig_h = create_carrier_heatmap(heatmap_df)
            st.plotly_chart(fig_h, use_container_width=True)
            render_insight_card(deliv_insights['carrier_handoff'], card_type="warning")
        else:
            st.info("Insufficient timestamp records for carrier handoff analysis.")
            
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 2: Visual 3 (On-Time % by State Map)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 3 &bull; On-Time Delivery % by Customer State</h3>
        <div class="chart-subtitle">State-level delivery SLA compliance across Brazil.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_map, col_stats = st.columns([1.2, 0.8])
    with col_map:
        if not state_ontime_df.empty:
            fig_state_map = create_brazil_map(state_ontime_df, 'ontime_pct', "On-Time % by State", color_scale="Greens", is_percent=True)
            st.plotly_chart(fig_state_map, use_container_width=True)
        else:
            st.info("No geographic delivery data available.")
            
    with col_stats:
        if not state_ontime_df.empty:
            best_st = state_ontime_df.iloc[0]
            worst_st = state_ontime_df.iloc[-1]
            med_val = state_ontime_df['ontime_pct'].median()
            nat_val = state_ontime_df['ontime_pct'].mean()
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 1.25rem;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Geographic SLA Benchmarks</div>
                <div style="margin-top: 1rem; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 0.5rem;">
                    <span style="color: #cbd5e1;">Top Performing State:</span>
                    <strong style="color: #10B981;">{best_st['customer_state']} ({best_st['ontime_pct']:.1f}%)</strong>
                </div>
                <div style="margin-top: 0.6rem; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 0.5rem;">
                    <span style="color: #cbd5e1;">Median State On-Time:</span>
                    <strong style="color: #38BDF8;">{med_val:.1f}%</strong>
                </div>
                <div style="margin-top: 0.6rem; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 0.5rem;">
                    <span style="color: #cbd5e1;">National State Average:</span>
                    <strong style="color: #F59E0B;">{nat_val:.1f}%</strong>
                </div>
                <div style="margin-top: 0.6rem; display: flex; justify-content: space-between;">
                    <span style="color: #cbd5e1;">Lowest Performing State:</span>
                    <strong style="color: #F43F5E;">{worst_st['customer_state']} ({worst_st['ontime_pct']:.1f}%)</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        render_insight_card(deliv_insights['state_delivery'])
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 3: Visual 4 (Buyer Region -> Seller Region -> Delivery Outcome Sankey)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 4 &bull; Buyer Region &rarr; Seller Region &rarr; Delivery Outcome (Sankey)</h3>
        <div class="chart-subtitle">Inter-regional logistics freight flows tracing origin trade routes to final fulfillment status.</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not routes_df.empty:
        fig_sankey = create_sankey_diagram(routes_df)
        st.plotly_chart(fig_sankey, use_container_width=True)
        render_insight_card(deliv_insights['route_analysis'])
        
        # Route Analysis Cards
        if route_insights and route_insights.get('highest_volume') is not None:
            hv = route_insights['highest_volume']
            hl = route_insights['highest_late']
            ho = route_insights['highest_ontime']
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; padding: 0.85rem;">
                    <div style="font-size: 0.72rem; color: #a5b4fc; font-weight: 700; text-transform: uppercase;">Highest-Volume Route</div>
                    <div style="font-size: 1rem; font-weight: 800; color: #ffffff; margin-top: 0.2rem;">Seller {hv['seller_region']} &rarr; Buyer {hv['customer_region']}</div>
                    <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 0.2rem;">{format_number(hv['total_shipments'])} shipments ({hv['ontime_rate']:.1f}% on-time)</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 8px; padding: 0.85rem;">
                    <div style="font-size: 0.72rem; color: #fda4af; font-weight: 700; text-transform: uppercase;">Highest Late-Rate Route</div>
                    <div style="font-size: 1rem; font-weight: 800; color: #ffffff; margin-top: 0.2rem;">Seller {hl['seller_region']} &rarr; Buyer {hl['customer_region']}</div>
                    <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 0.2rem;">{hl['late_rate']:.1f}% late rate ({format_number(hl['late_shipments'])} delayed)</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 0.85rem;">
                    <div style="font-size: 0.72rem; color: #6ee7b7; font-weight: 700; text-transform: uppercase;">Highest On-Time Route</div>
                    <div style="font-size: 1rem; font-weight: 800; color: #ffffff; margin-top: 0.2rem;">Seller {ho['seller_region']} &rarr; Buyer {ho['customer_region']}</div>
                    <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 0.2rem;">{ho['ontime_rate']:.1f}% on-time ({format_number(ho['ontime_shipments'])} on-time)</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No inter-regional logistics flows available.")

render_page_3()
