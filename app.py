import os
import streamlit as st

st.set_page_config(
    page_title="Olist Business Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Global CSS
css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Pre-load analytical data to warm cache
from analytics.data_loader import load_analytical_data
from components.sidebar import render_sidebar
from components.header import render_header
from components.kpi_cards import render_kpi_cards
from components.insight_cards import render_summary_banner
from utils.formatting import format_currency, format_number

orders_master, items_master, payments_master = load_analytical_data()

# Render Global Sidebar Filters
filters = render_sidebar(orders_master, items_master)

def render_main_portal():
    """
    Main Landing Portal Page (app.py)
    Serves as the executive entry point, summarizing high-level KPIs, module navigation,
    project architecture, and team ownership.
    """
    render_header(
        page_title="Olist Business Intelligence Platform",
        page_subtitle="Executive decision-support system translating multi-page Power BI reports into dynamic analytical visual intelligence.",
        active_filters=filters
    )
    
    # Executive Welcome Banner
    render_summary_banner(
        title="Executive Analytics Portal &bull; Enterprise Telemetry",
        text="Welcome to the <strong>Olist Brazilian E-Commerce Analytics Platform</strong>. This application reproduces and extends four core Power BI dashboards with automated 4-layer analytical interpretation (Finding &bull; Evidence &bull; Business Interpretation &bull; Operational Implication) powered by actual transaction data across 99,441 orders.",
        icon="⚡",
        variant="default"
    )
    
    # Platform High-Level KPIs
    tot_rev = orders_master['total_payment'].sum()
    tot_orders = len(orders_master)
    uniq_cust = orders_master['customer_unique_id'].nunique()
    delivered = orders_master[orders_master['is_delivered']]
    ontime_pct = (1.0 - (delivered['is_late'].sum() / len(delivered))) * 100
    rev_with_score = orders_master['review_score'].dropna()
    avg_score = rev_with_score.mean()
    
    render_kpi_cards([
        {
            'label': 'Total Gross Revenue',
            'value': format_currency(tot_rev),
            'sub': 'All sales channels (2016-2018)',
            'icon': '💳',
            'color': '#10B981'
        },
        {
            'label': 'Total Orders',
            'value': format_number(tot_orders),
            'sub': 'Completed transactions',
            'icon': '📦',
            'color': '#6366F1'
        },
        {
            'label': 'Unique Buyers',
            'value': format_number(uniq_cust),
            'sub': 'Registered customer base',
            'icon': '👥',
            'color': '#38BDF8'
        },
        {
            'label': 'On-Time Delivery Rate',
            'value': f"{ontime_pct:.1f}%",
            'sub': 'Orders meeting estimated SLA',
            'icon': '✅',
            'color': '#F59E0B'
        },
        {
            'label': 'Avg Review Score',
            'value': f"{avg_score:.2f} ⭐",
            'sub': 'Customer satisfaction index',
            'icon': '⭐',
            'color': '#8B5CF6'
        }
    ])
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 1.5rem 0 2rem 0;'>", unsafe_allow_html=True)
    
    # Module Portals & Team Ownership Section
    st.markdown("""
    <div class="chart-header" style="margin-bottom: 1.25rem;">
        <h3 class="chart-title" style="font-size: 1.3rem;">Analytical Dashboards & Team Ownership</h3>
        <div class="chart-subtitle">Explore each specialized business intelligence module or inspect the balanced project work distribution.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #131d33 0%, #0f172a 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; padding: 1.35rem; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">
                    📊 Page 1 &bull; Executive Overview
                </div>
                <span style="font-size: 0.72rem; padding: 0.2rem 0.6rem; border-radius: 9999px; background: rgba(99, 102, 241, 0.2); color: #a5b4fc; font-weight: 700;">
                    Michael Fernandes (Roll No: 06)
                </span>
            </div>
            <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 600; margin-top: 0.3rem;">
                Core Question: "How is the overall business and sales volume performing?"
            </div>
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin-top: 0.6rem;">
                Recreates the commercial overview: 99K orders, R$ 16.01M revenue, dual-axis monthly transaction growth, Monday demand peaks, payment method concentration (Credit Card 78.3%), and state-level revenue concentration.
            </div>
        </div>
        
        <div style="background: linear-gradient(145deg, #131d33 0%, #0f172a 100%); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 1.35rem; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">
                    👥 Page 2 &bull; Customer & Product Intelligence
                </div>
                <span style="font-size: 0.72rem; padding: 0.2rem 0.6rem; border-radius: 9999px; background: rgba(56, 189, 248, 0.2); color: #7dd3fc; font-weight: 700;">
                    Michael Fernandes (Roll No: 06)
                </span>
            </div>
            <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 600; margin-top: 0.3rem;">
                Core Question: "Who buys, what sells, and where are customers located?"
            </div>
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin-top: 0.6rem;">
                Deep dives into geographic demand: Brazil state choropleth map, Top 10 cities led by São Paulo (~15K buyers), category demand matrix across 5 macro-regions, category rankings, and the critical ~3.1% repeat customer bottleneck alert.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #131d33 0%, #0f172a 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1.35rem; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">
                    🚚 Page 3 &bull; Delivery Performance & Logistics
                </div>
                <span style="font-size: 0.72rem; padding: 0.2rem 0.6rem; border-radius: 9999px; background: rgba(16, 185, 129, 0.2); color: #6ee7b7; font-weight: 700;">
                    Nisarg Shah (Roll No: 05)
                </span>
            </div>
            <div style="font-size: 0.82rem; color: #34d399; font-weight: 600; margin-top: 0.3rem;">
                Core Question: "Where are delivery friction points occurring?"
            </div>
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin-top: 0.6rem;">
                Analyzes operational efficiency: 12.56 days avg delivery time, 10.6 days average delay, seller SLA compliance scatter with 85% reference line, carrier dispatch handoff heatmap, and an inter-regional Sankey diagram (Buyer Region &rarr; Seller Region &rarr; Outcome).
            </div>
        </div>
        
        <div style="background: linear-gradient(145deg, #131d33 0%, #0f172a 100%); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 12px; padding: 1.35rem; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">
                    ⭐ Page 4 &bull; Customer Experience & Reviews
                </div>
                <span style="font-size: 0.72rem; padding: 0.2rem 0.6rem; border-radius: 9999px; background: rgba(244, 63, 94, 0.2); color: #fda4af; font-weight: 700;">
                    Nisarg Shah (Roll No: 05)
                </span>
            </div>
            <div style="font-size: 0.82rem; color: #fda4af; font-weight: 600; margin-top: 0.3rem;">
                Core Question: "How does delivery performance directly shape customer satisfaction?"
            </div>
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin-top: 0.6rem;">
                Features the Hero Discovery: 2.59-point rating collapse from on-time (4.29) to 8+ days late (1.70), product sales vs review score treemap, interactive multi-dimensional root-cause diagnostic selector, and monthly operational correlation tracking.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Team & Work Distribution Callout Card
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 1.35rem; margin-top: 0.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
            <div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 0.5rem;">
                    <span>⚖️</span> Work Distribution & Project Governance
                </div>
                <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 0.25rem;">
                    Balanced 50% &bull; 50% project execution between <strong>Michael Fernandes (ID: 2509006, Roll: 06)</strong> and <strong>Nisarg Shah (ID: 2509005, Roll: 05)</strong> across both Power BI report creation and Streamlit full-stack implementation.
                </div>
            </div>
            <div>
                <span style="font-size: 0.78rem; font-weight: 700; color: #10B981; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.4rem 0.85rem; border-radius: 8px;">
                    Equal 50% / 50% Ownership
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Setup Navigation with app.py as Main Page (default=True)
pages = [
    st.Page(render_main_portal, title="00 Main Portal", icon="⚡", default=True),
    st.Page("pages/01_Executive_Overview.py", title="01 Executive Overview", icon="📊"),
    st.Page("pages/02_Customer_Product_Intelligence.py", title="02 Customer & Products", icon="👥"),
    st.Page("pages/03_Delivery_Analytics.py", title="03 Delivery Analytics", icon="🚚"),
    st.Page("pages/04_Customer_Experience.py", title="04 Customer Experience", icon="⭐"),
    st.Page("pages/05_Work_Distribution.py", title="05 Work Distribution", icon="⚖️")
]

nav = st.navigation(pages)
nav.run()
