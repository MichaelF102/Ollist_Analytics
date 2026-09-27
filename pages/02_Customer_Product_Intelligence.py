import streamlit as st
import os
from analytics.data_loader import load_analytical_data, apply_global_filters
from analytics.customers import (
    get_customer_kpis,
    get_customers_by_state,
    get_top_cities_by_customers,
    get_customers_by_order_frequency,
    get_customer_geography_statistics,
    get_city_concentration_statistics,
    get_order_frequency_statistics
)
from analytics.products import (
    get_product_category_performance,
    get_category_performance_table,
    get_category_share_by_region,
    get_category_statistics,
    get_category_region_statistics,
    get_category_comparison_statistics
)
from analytics.insights import (
    generate_customer_insights,
    generate_product_insights,
    generate_customer_product_summary
)
from components.header import render_header
from components.kpi_cards import render_kpi_cards, render_metric_strip
from components.insight_cards import render_insight_card, render_summary_banner
from components.charts import (
    create_brazil_map,
    create_horizontal_bar,
    create_category_matrix_heatmap,
    create_order_frequency_bar
)
from components.tables import render_category_performance_table
from utils.formatting import format_currency, format_number, format_percent

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
    
    # Top Control Bar: Header & Presentation Mode Toggle
    head_col, toggle_col = st.columns([0.75, 0.25])
    with head_col:
        render_header(
            page_title="Customers, Products & Geography",
            page_subtitle="Customer intelligence answering: Who buys, where are they located, what do they buy, and do they return?",
            active_filters=filters
        )
    with toggle_col:
        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
        presentation_mode = st.toggle(
            "🎤 Presentation Mode",
            value=st.session_state.get('presentation_mode', False),
            key="pres_mode_p2",
            help="Enable presenter talking points, expanded analytical narratives, and presentation prompts."
        )
        st.session_state['presentation_mode'] = presentation_mode
        if presentation_mode:
            st.caption("Active: Presenter guidance & narrative scripts enabled.")
            
    # Customer & Product KPIs
    kpis = get_customer_kpis(orders_df, items_df)
    
    # 1. PAGE OPENING — PRESENTATION STORY
    uniq_fmt = format_number(kpis['unique_customers'])
    rep_fmt = format_number(kpis['repeat_customers'])
    prods_fmt = format_number(kpis['unique_products'])
    cats_fmt = str(kpis['unique_categories'])
    
    with st.expander("🎯 Customer & Product Story • Behavioral & Geographic Intelligence", expanded=True):
        st.markdown(f"""
        <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6;">
            <p style="margin-bottom: 0.5rem; font-weight: 600; color: #f8fafc;">
                "Page 2 moves from business performance to customer and product intelligence. 
                Instead of asking how much Olist sells, we now ask who is buying, where they are located, 
                what categories they purchase, and whether customers are coming back."
            </p>
            <p style="margin: 0; color: #94a3b8;">
                We currently have approximately <strong style="color: #38bdf8;">{uniq_fmt} unique customers</strong>, 
                <strong style="color: #6366f1;">{rep_fmt} repeat customers</strong>, 
                <strong style="color: #10b981;">{prods_fmt} unique products</strong> and 
                <strong style="color: #8b5cf6;">{cats_fmt} product categories</strong> represented in the active selection.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 2. KPI SECTION — CUSTOMER & PRODUCT SCALE
    render_kpi_cards([
        {
            'label': 'Unique Customers',
            'value': uniq_fmt,
            'sub': f'Approx. {uniq_fmt} buyers in selection',
            'icon': '👥',
            'color': '#38BDF8'
        },
        {
            'label': 'Repeat Customers',
            'value': rep_fmt,
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
            'value': prods_fmt,
            'sub': 'SKU catalogue depth',
            'icon': '📦',
            'color': '#10B981'
        },
        {
            'label': 'Unique Categories',
            'value': cats_fmt,
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
    
    if presentation_mode:
        st.info(
            f"🎤 **Presenter Talking Point &bull; Customer & Product Scale:** "
            f"There are approximately {uniq_fmt} unique customers in the current selection, representing the overall buyer base. "
            f"Approximately {rep_fmt} customers meet the dashboard's repeat-customer definition of placing two or more orders. "
            f"The repeat-customer rate ({kpis['repeat_rate']:.1f}%) provides a view of how frequently customers return after their initial purchase. "
            f"The observed repeat-purchase level provides an important area for customer-retention analysis. "
            f"On the catalogue side, the marketplace contains approximately {prods_fmt} unique products across {cats_fmt} distinct product categories, "
            f"accounting for approximately {format_number(kpis['products_sold'])} individual product units sold."
        )
        
    # Statistical Calculations for Visuals
    state_cust_df = get_customers_by_state(orders_df)
    city_cust_df = get_top_cities_by_customers(orders_df, top_n=10)
    freq_df = get_customers_by_order_frequency(orders_df)
    cat_perf_df = get_product_category_performance(items_df, top_n=10)
    cat_region_matrix = get_category_share_by_region(items_df, top_n=9)
    table_df = get_category_performance_table(items_df, top_n=15)
    
    # Statistical Summary Objects
    geo_stats = get_customer_geography_statistics(state_cust_df, total_customers=kpis.get('unique_customers'))
    city_stats = get_city_concentration_statistics(city_cust_df, total_customers=kpis.get('unique_customers'))
    freq_stats = get_order_frequency_statistics(freq_df)
    cat_stats = get_category_statistics(cat_perf_df)
    region_stats = get_category_region_statistics(cat_region_matrix)
    comp_stats = get_category_comparison_statistics(table_df)
    
    # Structured Insights
    cust_insights = generate_customer_insights(kpis, state_cust_df, city_cust_df, freq_df)
    prod_insights = generate_product_insights(cat_perf_df, cat_region_matrix, table_df=table_df)
    
    # 3. KEY CUSTOMER RETENTION FINDING BANNER
    render_summary_banner(
        title="Key Customer Retention Finding",
        text=(
            f"Approximately <strong>{kpis['repeat_rate']:.1f}% of unique customers</strong> "
            f"({rep_fmt} repeat buyers out of {uniq_fmt} unique buyers) meet the repeat-customer definition. "
            f"The customer base is predominantly composed of customers with limited observed repeat purchasing in the current selection. "
            f"From a business analytics perspective, this provides an important area for investigating customer retention and repeat purchasing behavior."
        ),
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
        
        # Key Numbers Strip for Visual 1
        render_metric_strip([
            {'label': 'Top State', 'value': geo_stats['top_state'], 'sub': f"{format_number(geo_stats['top_customers'])} buyers", 'color': '#38BDF8'},
            {'label': 'Top State Share', 'value': f"{geo_stats['top_share']:.1f}%", 'sub': 'Of total customer base', 'color': '#10B981'},
            {'label': 'Top 3 Share', 'value': f"{geo_stats['top3_share']:.1f}%", 'sub': f"{', '.join(geo_stats['top3_states'][:3])}", 'color': '#F59E0B'},
            {'label': 'Top 5 Share', 'value': f"{geo_stats['top5_share']:.1f}%", 'sub': f"{geo_stats['top5_share']:.1f}% concentration", 'color': '#8B5CF6'}
        ])
        
        fig_map = create_brazil_map(state_cust_df, 'customer_count', "Unique Customers by State", color_scale="Blues")
        st.plotly_chart(fig_map, use_container_width=True)
        render_insight_card(cust_insights['geographic_distribution'])
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Customer Geography:** "
                f"The map allows us to move from customer volume to customer geography. "
                f"{geo_stats['top_state']} has the highest number of customers with approximately {format_number(geo_stats['top_customers'])} customers ({geo_stats['top_share']:.1f}% share). "
                f"The customer base is distributed across multiple Brazilian states, but customer concentration is stronger in major population and commercial regions, "
                f"with the top 3 states accounting for approximately {geo_stats['top3_share']:.1f}% of buyers. "
                f"This complements the revenue-by-state analysis from Page 1: Page 1 showed where revenue comes from, while Page 2 helps us understand where customers themselves are located."
            )
        
    with col_city:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 2 &bull; Top 10 Cities by Number of Customers</h3>
            <div class="chart-subtitle">Leading metropolitan areas by unique customer count.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Numbers Strip for Visual 2
        render_metric_strip([
            {'label': 'Top City', 'value': city_stats['top_city'], 'sub': f"{format_number(city_stats['top_city_customers'])} buyers", 'color': '#38BDF8'},
            {'label': 'Runner-Up City', 'value': city_stats['second_city'], 'sub': f"{format_number(city_stats['second_city_customers'])} buyers", 'color': '#6366F1'},
            {'label': 'Gap vs #2', 'value': format_number(city_stats['gap_top2']), 'sub': f"{city_stats['ratio_top2']:.1f}x concentration", 'color': '#EC4899'},
            {'label': 'Top 10 Share', 'value': f"{city_stats['top10_share']:.1f}%", 'sub': 'Of urban customer base', 'color': '#10B981'}
        ])
        
        fig_city = create_horizontal_bar(city_cust_df, 'customer_city', 'customer_count', "Top 10 Cities", "Unique Customers", color='#38BDF8')
        st.plotly_chart(fig_city, use_container_width=True)
        render_insight_card(cust_insights['city_concentration'])
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; City Concentration:** "
                f"When we drill down from states to cities, {city_stats['top_city']} becomes the largest customer market, with approximately {format_number(city_stats['top_city_customers'])} customers. "
                f"{city_stats['second_city']} follows with approximately {format_number(city_stats['second_city_customers'])} customers. "
                f"The gap between the largest and second-largest cities is approximately {format_number(city_stats['gap_top2'])} customers ({city_stats['ratio_top2']:.1f}x ratio). "
                f"This indicates that customer activity is concentrated in major urban centers. "
                f"This type of geographic concentration can be useful when analyzing market segmentation, logistics coverage and targeted campaigns."
            )
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 2: Visual 3 (Category Share by Region Heatmap)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 3 &bull; Category Share by Region</h3>
        <div class="chart-subtitle">Product category preference mix across the five Brazilian macro-regions (% column share).</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not cat_region_matrix.empty:
        # Key Numbers Strip for Visual 3
        render_metric_strip([
            {'label': 'Peak Category-Region', 'value': region_stats['largest_cat'], 'sub': f"{region_stats['largest_region']} ({region_stats['largest_share']:.1f}%)", 'color': '#38BDF8'},
            {'label': 'Peak Share', 'value': f"{region_stats['largest_share']:.1f}%", 'sub': 'Highest regional mix', 'color': '#10B981'},
            {'label': 'Widest Regional Spread', 'value': region_stats['max_variation_cat'], 'sub': f"{region_stats['max_variation_val']:.1f} pts gap", 'color': '#F59E0B'},
            {'label': 'Lowest Category-Region', 'value': region_stats['lowest_cat'], 'sub': f"{region_stats['lowest_region']} ({region_stats['lowest_share']:.1f}%)", 'color': '#94A3B8'}
        ])
        
        fig_matrix = create_category_matrix_heatmap(cat_region_matrix)
        st.plotly_chart(fig_matrix, use_container_width=True)
        render_insight_card(prod_insights['regional_category_variation'])
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Regional Product Mix:** "
                f"This matrix answers a more detailed question: does product-category preference change depending on the region? "
                f"Each column represents a Brazilian macro-region, while the rows represent product categories. "
                f"The category mix is not identical across all regions. '{region_stats['max_variation_cat']}' displays the highest regional variation "
                f"with a {region_stats['max_variation_val']:.1f} percentage-point gap between its highest-share region ({region_stats['max_variation_high_reg']}: {region_stats['max_variation_high_val']:.1f}%) "
                f"and lowest ({region_stats['max_variation_low_reg']}: {region_stats['max_variation_low_val']:.1f}%). "
                f"Rather than treating Brazil as one homogeneous market, the data suggests that regional differences in product mix should be considered when analyzing customer demand."
            )
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
        
        # Key Numbers Strip for Visual 4
        render_metric_strip([
            {'label': 'Top Category', 'value': cat_stats['top_category'], 'sub': f"{format_number(cat_stats['top_units'])} units", 'color': '#6366F1'},
            {'label': 'Second Category', 'value': cat_stats['second_category'], 'sub': f"{format_number(cat_stats['second_units'])} units", 'color': '#38BDF8'},
            {'label': 'Top 3 Share', 'value': f"{cat_stats['top3_share']:.1f}%", 'sub': f"{format_number(cat_stats['top3_units'])} units", 'color': '#10B981'},
            {'label': 'Top 10 Share', 'value': f"{cat_stats['top10_share']:.1f}%", 'sub': f"{format_number(cat_stats['top10_units'])} units", 'color': '#F59E0B'}
        ])
        
        fig_cat = create_horizontal_bar(cat_perf_df, 'category_clean', 'products_sold', "Top Categories", "Products Sold", color='#6366F1')
        st.plotly_chart(fig_cat, use_container_width=True)
        render_insight_card(prod_insights['category_performance'])
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Product Category Demand:** "
                f"Now we move from geography to product demand. "
                f"{cat_stats['top_category']} is the largest category in terms of products sold, with approximately {format_number(cat_stats['top_units'])} units. "
                f"It is followed by {cat_stats['second_category']} ({format_number(cat_stats['second_units'])} units) and {cat_stats['third_category']} ({format_number(cat_stats['third_units'])} units). "
                f"However, product volume and revenue are not necessarily the same thing. "
                f"A category can sell many units while having a lower average selling price. "
                f"This is an important analytical distinction, which we will examine further in the detailed table below."
            )
        
    with col_freq:
        st.markdown("""
        <div class="chart-header">
            <h3 class="chart-title">Visual 5 &bull; Customers by Number of Orders</h3>
            <div class="chart-subtitle">Distribution of customers across purchase count cohorts.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Numbers Strip for Visual 5
        render_metric_strip([
            {'label': '1 Order Buyers', 'value': format_number(freq_stats['one_order_count']), 'sub': f"{freq_stats['one_order_share']:.1f}% share", 'color': '#38BDF8'},
            {'label': '2+ Orders (Repeat)', 'value': format_number(freq_stats['repeat_count']), 'sub': f"{freq_stats['repeat_share']:.1f}% share", 'color': '#F59E0B'},
            {'label': '3+ Orders', 'value': format_number(freq_stats['three_plus_count']), 'sub': f"{freq_stats['three_plus_share']:.1f}% share", 'color': '#10B981'},
            {'label': 'Repeat Share', 'value': f"{freq_stats['repeat_share']:.1f}%", 'sub': 'Empirical benchmark', 'color': '#8B5CF6'}
        ])
        
        fig_freq = create_order_frequency_bar(freq_df)
        st.plotly_chart(fig_freq, use_container_width=True)
        render_insight_card(cust_insights['order_frequency'], card_type="warning")
        
        if presentation_mode:
            st.info(
                f"🎤 **Presenter Talking Point &bull; Purchase Frequency:** "
                f"This is one of the most important customer-behavior visuals on the page. "
                f"Approximately {format_number(freq_stats['one_order_count'])} customers ({freq_stats['one_order_share']:.1f}%) have placed one order. "
                f"Approximately {format_number(freq_stats['repeat_count'])} customers ({freq_stats['repeat_share']:.1f}%) have placed two or more orders. "
                f"Customers with three or more orders represent approximately {freq_stats['three_plus_share']:.1f}% of the observed customer base. "
                f"The customer base is predominantly composed of one-time purchasers in the current dataset. "
                f"This helps explain the difference between the total unique-customer count and the repeat-customer count shown in the KPI cards. "
                f"This provides a clear area for investigating customer retention and repeat purchasing behavior."
            )
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Row 4: Visual 6 (Product Category Performance Table)
    st.markdown("""
    <div class="chart-header">
        <h3 class="chart-title">Visual 6 &bull; Product Category Detailed Performance Matrix</h3>
        <div class="chart-subtitle">Exhaustive financial and transactional metrics for top categories with gross totals.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Numbers Strip for Visual 6 (Multi-Metric Leaders)
    render_metric_strip([
        {'label': 'Highest Sales Value', 'value': comp_stats['highest_sales_cat'], 'sub': format_currency(comp_stats['highest_sales_val']), 'color': '#10B981'},
        {'label': 'Highest Unit Volume', 'value': comp_stats['highest_units_cat'], 'sub': f"{format_number(comp_stats['highest_units_val'])} units", 'color': '#6366F1'},
        {'label': 'Highest Avg / Order', 'value': comp_stats['highest_aov_cat'], 'sub': format_currency(comp_stats['highest_aov_val']), 'color': '#F59E0B'},
        {'label': 'Highest Order Count', 'value': comp_stats['highest_orders_cat'], 'sub': f"{format_number(comp_stats['highest_orders_val'])} orders", 'color': '#38BDF8'}
    ])
    
    render_category_performance_table(table_df)
    render_insight_card(prod_insights['category_table_summary'])
    
    if presentation_mode:
        st.info(
            f"🎤 **Presenter Talking Point &bull; Multi-Metric Category Comparison:** "
            f"The final visual brings together several product metrics. "
            f"For each category, we can compare product sales, average sales per order, products sold and number of orders. "
            f"This table is useful because it prevents us from looking at category performance through only one metric. "
            f"Instead, we can distinguish between sales value, volume and order frequency. "
            f"Notice that the category leading in sales value ({comp_stats['highest_sales_cat']}: {format_currency(comp_stats['highest_sales_val'])}) "
            f"is distinct from the highest average ticket category ({comp_stats['highest_aov_cat']}: {format_currency(comp_stats['highest_aov_val'])}) "
            f"and unit volume leader ({comp_stats['highest_units_cat']}: {format_number(comp_stats['highest_units_val'])} units). "
            f"Do not assume the same category leads every metric; this multi-dimensional assessment is vital for commercial strategy."
        )
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)
    
    # 4. PAGE-LEVEL EXECUTIVE SUMMARY
    page_summary_text = generate_customer_product_summary(
        kpis, geo_stats, city_stats, cat_stats, freq_stats, region_stats
    )
    render_summary_banner(
        title="Customer & Product Intelligence Summary",
        text=page_summary_text,
        icon="📋",
        variant="blue"
    )
    
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # 5. PAGE TRANSITION TO PAGE 3
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    ">
        <div style="font-size: 0.85rem; font-weight: 700; color: #818cf8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.35rem;">
            ➡️ From Customer Intelligence to Delivery Performance
        </div>
        <div style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.6; margin-bottom: 0.5rem;">
            Page 2 shows us who the customers are, where they are located, what categories generate product volume, and how frequently customers order.
            However, understanding customer and product demand is only one side of the marketplace.
            The next question is: <em>how efficiently are those orders actually being delivered across Brazil?</em>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_nav_l, col_nav_btn = st.columns([0.7, 0.3])
    with col_nav_btn:
        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
        if st.button("Continue to Delivery Analytics →", use_container_width=True, type="primary"):
            st.switch_page("pages/03_Delivery_Analytics.py")

render_page_2()
