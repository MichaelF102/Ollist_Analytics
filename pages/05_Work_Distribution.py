import streamlit as st
import os
import pandas as pd
from components.header import render_header
from components.insight_cards import render_summary_banner

def render_page_5():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    render_header(
        page_title="Work Distribution & Team Contributions",
        page_subtitle="Equal project ownership (50% - 50%) across Power BI visualization design, DAX modeling, and Streamlit engineering.",
        active_filters={}
    )
    
    # Summary Banner
    render_summary_banner(
        title="Project Execution & Equal Division of Work",
        text="The project is divided equally between <strong>Michael Fernandes (Roll No: 06, ID: 2509006)</strong> and <strong>Nisarg Shah (Roll No: 05, ID: 2509005)</strong>. Both members contributed equally across Power BI report engineering, DAX formulation, Python data modeling, Plotly visual design, and Streamlit full-stack implementation.",
        icon="⚖️",
        variant="default"
    )
    
    # Progress / Balance Indicators
    progress_html = """<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
<span style="font-size: 0.85rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase;">Overall Work Distribution Balance</span>
<span style="font-size: 0.85rem; font-weight: 800; color: #10B981;">50% &bull; 50% Equal Split</span>
</div>
<div style="display: flex; height: 10px; border-radius: 5px; overflow: hidden; background: #1e293b;">
<div style="width: 50%; background: linear-gradient(90deg, #6366f1, #38bdf8);" title="Michael Fernandes (50%)"></div>
<div style="width: 50%; background: linear-gradient(90deg, #10b981, #f59e0b);" title="Nisarg Shah (50%)"></div>
</div>
<div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8; margin-top: 0.4rem;">
<span>Michael Fernandes &bull; Pages 1 & 2 (50%)</span>
<span>Nisarg Shah &bull; Pages 3 & 4 (50%)</span>
</div>
</div>"""
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Team Member Profiles
    col_m, col_n = st.columns(2)
    
    with col_m:
        michael_html = """<div style="background: linear-gradient(145deg, #131d33 0%, #0f172a 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 14px; padding: 1.5rem; height: 100%;">
<div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
<div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(99, 102, 241, 0.2); border: 1px solid #6366f1; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">👨‍💻</div>
<div>
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #ffffff;">Michael Fernandes</h3>
<div style="font-size: 0.8rem; color: #38bdf8; font-weight: 600;">Student ID: 2509006 &bull; Roll No: 06</div>
</div>
</div>
<div style="display: inline-block; padding: 0.25rem 0.65rem; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 6px; font-size: 0.75rem; color: #a5b4fc; font-weight: 700; margin-bottom: 1rem; text-transform: uppercase;">Module Ownership: Pages 1 & 2</div>
<div style="margin-bottom: 1rem;">
<div style="font-size: 0.82rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.35rem;">📊 Page 1 &bull; Executive Overview (Business Performance & Sales Trends)</div>
<div style="font-size: 0.78rem; color: #94a3b8; line-height: 1.5;">High-level commercial telemetry answering <em>"How is the business performing?"</em> through gross revenue, basket size, purchasing cadence, and operational leakages.</div>
</div>
<div style="margin-bottom: 1rem;">
<div style="font-size: 0.82rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.35rem;">👥 Page 2 &bull; Customer & Product Intelligence (Customers, Products & Geography)</div>
<div style="font-size: 0.78rem; color: #94a3b8; line-height: 1.5;">Demographic and merchandise diagnostics answering <em>"Who buys, what sells, and where are customers concentrated?"</em>, uncovering the ~3.1% repeat customer bottleneck.</div>
</div>
<hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 1rem 0;">
<div style="font-size: 0.78rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase; margin-bottom: 0.5rem;">Key Technical Deliverables:</div>
<ul style="font-size: 0.78rem; color: #cbd5e1; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
<li><strong>Power BI Dashboard:</strong> Built Page 1 & Page 2 visuals, DAX KPI cards (99K Orders, 16.01M Revenue, 96K Customers, 160.99 AOV), monthly combo chart, weekday bar chart, payment donut, Brazil choropleth map, regional crosstab matrix, and category performance ranking tables.</li>
<li><strong>Streamlit Architecture:</strong> Designed core project structure, data caching pipeline (<code>preprocess.py</code>, <code>analytics/data_loader.py</code>), global sidebar filtering, and custom CSS design system (<code>assets/style.css</code>).</li>
<li><strong>Analytics Engines:</strong> Authored <code>analytics/sales.py</code>, <code>analytics/customers.py</code>, <code>analytics/products.py</code>, and formatted category table components.</li>
</ul>
</div>"""
        st.markdown(michael_html, unsafe_allow_html=True)
        
    with col_n:
        nisarg_html = """<div style="background: linear-gradient(145deg, #131d33 0%, #0f172a 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 14px; padding: 1.5rem; height: 100%;">
<div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
<div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">👨‍💻</div>
<div>
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #ffffff;">Nisarg Shah</h3>
<div style="font-size: 0.8rem; color: #34d399; font-weight: 600;">Student ID: 2509005 &bull; Roll No: 05</div>
</div>
</div>
<div style="display: inline-block; padding: 0.25rem 0.65rem; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; font-size: 0.75rem; color: #6ee7b7; font-weight: 700; margin-bottom: 1rem; text-transform: uppercase;">Module Ownership: Pages 3 & 4</div>
<div style="margin-bottom: 1rem;">
<div style="font-size: 0.82rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.35rem;">🚚 Page 3 &bull; Delivery Performance & Logistics Analytics</div>
<div style="font-size: 0.78rem; color: #94a3b8; line-height: 1.5;">Supply chain telemetry answering <em>"Where are delivery problems occurring and how efficiently are orders fulfilled?"</em> across carrier handoffs, seller reliability, and inter-regional corridors.</div>
</div>
<div style="margin-bottom: 1rem;">
<div style="font-size: 0.82rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.35rem;">⭐ Page 4 &bull; Customer Experience & Reviews</div>
<div style="font-size: 0.78rem; color: #94a3b8; line-height: 1.5;">Customer feedback and sentiment analytics answering <em>"How does logistics fulfillment directly shape review scores?"</em>, uncovering the dramatic 2.59-point sentiment cliff.</div>
</div>
<hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 1rem 0;">
<div style="font-size: 0.78rem; font-weight: 700; color: #6ee7b7; text-transform: uppercase; margin-bottom: 0.5rem;">Key Technical Deliverables:</div>
<ul style="font-size: 0.78rem; color: #cbd5e1; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
<li><strong>Power BI Dashboard:</strong> Built Page 3 & Page 4 visuals, DAX measures for 12.56-day delivery time, 10.6-day delay, 6.8% late rate, seller scatter plot with 85% SLA line, carrier handoff matrix, inter-regional Sankey diagram, sales vs rating treemap, delay bucket combo chart, and decomposition tree.</li>
<li><strong>Streamlit Architecture:</strong> Authored interactive Plotly Sankey diagram, carrier handoff 2D heatmap, hero visual combo chart, and interactive multi-dimensional segment diagnostic tool with dynamic dropdown switching.</li>
<li><strong>Analytics Engines:</strong> Developed <code>analytics/delivery.py</code>, <code>analytics/reviews.py</code>, route corridor analysis, and the automated 4-layer analytical Insight Engine (<code>analytics/insights.py</code>).</li>
</ul>
</div>"""
        st.markdown(nisarg_html, unsafe_allow_html=True)
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Detailed Task & Responsibility Matrix Table
    table_header_html = """<div class="chart-header">
<h3 class="chart-title">Comprehensive Responsibility Matrix</h3>
<div class="chart-subtitle">Side-by-side mapping of project domains, Power BI design, and Streamlit implementation.</div>
</div>"""
    st.markdown(table_header_html, unsafe_allow_html=True)
    
    matrix_data = [
        {"Domain": "Business Performance & Sales Trends", "Owner": "Michael Fernandes (Roll No: 06)", "Power BI Deliverable": "KPI Cards, Monthly Orders & Revenue, Day of Week, Payment Method Donut, Top 10 States, Non-Delivered Orders", "Streamlit Deliverable": "Page 1 Executive Overview, analytics/sales.py, Dual-axis combo chart, horizontal bars, donut charts"},
        {"Domain": "Customers, Products & Geography", "Owner": "Michael Fernandes (Roll No: 06)", "Power BI Deliverable": "Customer retention DAX (~3.1%), Brazil state map, Top 10 cities, Category regional matrix heatmap, Category table", "Streamlit Deliverable": "Page 2 Customer Intelligence, analytics/customers.py, analytics/products.py, Category Table, Brazil GeoJSON map"},
        {"Domain": "Delivery Performance & Logistics", "Owner": "Nisarg Shah (Roll No: 05)", "Power BI Deliverable": "Delivery SLA measures (12.56d avg, 10.6d late, 6.8% late), Seller volume vs SLA scatter, Carrier handoff matrix, Regional Sankey flow", "Streamlit Deliverable": "Page 3 Delivery Analytics, analytics/delivery.py, Plotly Sankey diagram, Carrier handoff heatmap, Seller scatter plot"},
        {"Domain": "Customer Experience & Reviews", "Owner": "Nisarg Shah (Roll No: 05)", "Power BI Deliverable": "Review score KPIs (4.09 avg, 14.7% low), Sales vs Review treemap, Hero visual delay buckets (4.29 to 1.70), Low rating decomposition tree", "Streamlit Deliverable": "Page 4 Customer Experience, analytics/reviews.py, Hero visual combo chart, Dynamic root-cause diagnostic selector, Treemap"},
        {"Domain": "Platform Framework & Architecture", "Owner": "Joint / Equal (50% - 50%)", "Power BI Deliverable": "Shared star-schema data model, relationships, shared date table, theme styling", "Streamlit Deliverable": "Fast Parquet preprocessing cache, global multi-filter sidebar engine, dark modern BI CSS styling, automated Insight Engine"}
    ]
    
    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix, hide_index=True, width="stretch")

render_page_5()
