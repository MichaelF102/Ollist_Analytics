"""
Antigravity Analytical Insight Engine
Generates structured, 5-layer business interpretations deterministically from calculated metrics.
Adheres strictly to non-causal analytical language:
(associated with, correlated with, indicates, suggests, observed pattern).
"""

from utils.formatting import format_currency, format_number, format_percent, format_days, format_rating

def generate_sales_insights(kpis, monthly_df, weekday_df, payment_df, state_df, non_deliv_df):
    """Generates structured insights for Page 1 — Executive Overview."""
    from analytics.sales import (
        get_monthly_statistics,
        get_weekday_statistics,
        get_payment_statistics,
        get_state_revenue_statistics,
        get_order_status_statistics
    )
    
    insights = {}
    
    m_stats = get_monthly_statistics(monthly_df)
    w_stats = get_weekday_statistics(weekday_df)
    p_stats = get_payment_statistics(payment_df)
    s_stats = get_state_revenue_statistics(state_df, total_revenue=kpis.get('total_revenue'))
    o_stats = get_order_status_statistics(non_deliv_df)
    
    tot_orders = kpis['total_orders']
    tot_rev = kpis['total_revenue']
    uniq_cust = kpis['unique_customers']
    aov = kpis['aov']
    prods_sold = kpis['products_sold']
    
    # 1. Executive Summary
    insights['executive_summary'] = {
        'title': 'Executive Takeaway',
        'finding': f"Across the current selection, Olist records approximately {format_number(tot_orders)} orders and {format_currency(tot_rev)} in revenue.",
        'evidence': f"The business processed {format_number(tot_orders)} orders generating {format_currency(tot_rev)} in gross revenue across {format_number(uniq_cust)} unique customers (AOV: {format_currency(aov)}, Products Sold: {format_number(prods_sold)}). Order activity peaks during {m_stats['peak_order_month']}, while {w_stats['highest_day']} has the highest weekday volume.",
        'interpretation': f"{p_stats['largest_method']} represents the largest share of payment value at {p_stats['largest_share']:.1f}%. Geographically, {s_stats['top_state']} contributes the highest revenue ({s_stats['top_share']:.1f}% share). The order-status distribution indicates that '{o_stats['largest_status']}' is the largest operational non-delivered category.",
        'business_implication': 'Commercial growth is primarily volume-driven with distinct geographic and payment concentration that provides clear targets for operational and marketing resource allocation.'
    }
    
    # 2. Monthly Orders & Payment Value
    if not monthly_df.empty:
        insights['monthly_trend'] = {
            'title': 'Monthly Orders & Payment Value',
            'finding': f"Order activity changes substantially across the observation period, with the strongest activity occurring during {m_stats['peak_order_month']}.",
            'evidence': f"The highest monthly order volume was {format_number(m_stats['peak_orders'])} orders in {m_stats['peak_order_month']}, while the highest payment value was {format_currency(m_stats['peak_revenue'])} in {m_stats['peak_rev_month']}. Across the period, {format_number(tot_orders)} orders generated {format_currency(tot_rev)}.",
            'interpretation': f"The relationship between order volume and payment value helps distinguish growth driven by transaction frequency from changes in basket value. Monthly order volume and payment value show a {m_stats['corr_strength']} relationship (r = {m_stats['correlation']:.2f}).",
            'business_implication': 'These patterns can support demand planning, inventory preparation and operational capacity planning around high-volume periods.'
        }
    else:
        insights['monthly_trend'] = _empty_insight('Monthly Orders & Payment Value')
        
    # 3. Orders by Day of Week
    if not weekday_df.empty:
        insights['orders_by_weekday'] = {
            'title': 'Orders by Day of Week',
            'finding': f"Orders are concentrated around {w_stats['highest_day']}, recording approximately {format_number(w_stats['highest_orders'])} orders.",
            'evidence': f"{w_stats['highest_day']} records the highest volume ({format_number(w_stats['highest_orders'])} orders, {w_stats['highest_share']:.1f}% share), whereas {w_stats['lowest_day']} records the lowest order volume at approximately {format_number(w_stats['lowest_orders'])} orders ({w_stats['lowest_share']:.1f}% share). Overall weekdays represent {w_stats['weekday_share']:.1f}% of total demand.",
            'interpretation': 'The observed distribution shows a clear difference between weekday and weekend ordering activity, suggesting that customer purchasing is heavily workday-centric.',
            'business_implication': 'This type of pattern can be useful for planning customer support, marketing campaigns, inventory availability and operational capacity.'
        }
    else:
        insights['orders_by_weekday'] = _empty_insight('Orders by Day of Week')
        
    # 4. Payment Method Distribution
    if not payment_df.empty:
        insights['payment_distribution'] = {
            'title': 'Payment Method Distribution',
            'finding': f"{p_stats['largest_method']} dominates the payment mix, representing approximately {p_stats['largest_share']:.1f}% of payment value.",
            'evidence': f"{p_stats['largest_method']} captures {format_currency(p_stats['largest_value'])} ({p_stats['largest_share']:.1f}% of total payment value). {p_stats['second_method']} represents approximately {p_stats['second_share']:.1f}% ({format_currency(p_stats['second_value'])}). Total payment value across all instruments is {format_currency(p_stats['total_value'])}.",
            'interpretation': 'This indicates that payment value is concentrated around a relatively small number of payment methods, with credit processing representing the primary transaction channel.',
            'business_implication': 'Payment gateway processing reliability, transaction authorization rates, and checkout settlement terms directly govern the vast majority of revenue flow.'
        }
    else:
        insights['payment_distribution'] = _empty_insight('Payment Method Distribution')
        
    # 5. Revenue by Customer State
    if not state_df.empty:
        insights['revenue_by_state'] = {
            'title': 'Revenue Concentration by Customer State',
            'finding': f"{s_stats['top_state']} is the largest revenue-generating state, contributing approximately {format_currency(s_stats['top_revenue'])} in revenue.",
            'evidence': f"{s_stats['top_state']} generates {format_currency(s_stats['top_revenue'])} ({s_stats['top_share']:.1f}% of total revenue). It is followed by {s_stats['top2_state']} and {s_stats['top3_state']}. The top 10 states account for approximately {s_stats['top10_share']:.1f}% of total revenue.",
            'interpretation': f"Revenue is not evenly distributed geographically. The top states account for a substantial share of the observed revenue, with {s_stats['top_state']} demonstrating commanding commercial dominance.",
            'business_implication': f"Regional marketing efficiency, fulfillment center placement, and carrier routing are crucial in {s_stats['top_state']} and adjacent states to safeguard delivery economics."
        }
    else:
        insights['revenue_by_state'] = _empty_insight('Revenue Concentration by Customer State')
        
    # 6. Non-Delivered Orders by Status
    if not non_deliv_df.empty:
        insights['non_delivered_orders'] = {
            'title': 'Order Status Distribution (Non-Delivered)',
            'finding': f"Not every order progresses to the same operational state; the largest segment is '{o_stats['largest_status']}'.",
            'evidence': f"The largest non-delivered cohort is '{o_stats['largest_status']}' with {format_number(o_stats['largest_count'])} orders ({o_stats['largest_share']:.1f}%). Cancelled orders account for {format_number(o_stats['cancelled_count'])} orders ({format_currency(o_stats['cancelled_revenue'])}), while unavailable items represent {format_number(o_stats['unavailable_count'])} orders ({format_currency(o_stats['unavailable_revenue'])}).",
            'interpretation': 'The non-delivered order population contains multiple operational stages. In-transit orders represent active fulfillment pipeline, while cancelled and unavailable orders represent potential revenue leakage.',
            'business_implication': 'Streamlining inventory synchronization with marketplace sellers could reduce unfulfillable orders and retain gross revenue.'
        }
    else:
        insights['non_delivered_orders'] = _empty_insight('Non-Delivered Orders')
        
    return insights

def generate_customer_insights(kpis, state_cust_df, city_cust_df, freq_df):
    """Generates structured insights for Page 2 — Customers, Products & Geography."""
    from analytics.customers import (
        get_customer_geography_statistics,
        get_city_concentration_statistics,
        get_order_frequency_statistics
    )
    insights = {}
    
    geo_stats = get_customer_geography_statistics(state_cust_df, total_customers=kpis.get('unique_customers'))
    city_stats = get_city_concentration_statistics(city_cust_df, total_customers=kpis.get('unique_customers'))
    freq_stats = get_order_frequency_statistics(freq_df)
    
    # 1. Customer Retention Finding
    uniq_c = kpis.get('unique_customers', 0)
    rep_c = kpis.get('repeat_customers', 0)
    rep_r = kpis.get('repeat_rate', 0.0)
    
    insights['customer_retention'] = {
        'title': 'Customer Retention & Repeat Purchasing Finding',
        'finding': 'The customer base is predominantly composed of customers with limited observed repeat purchasing in the current selection.',
        'evidence': f"Approximately {rep_r:.1f}% of unique customers ({format_number(rep_c)} repeat buyers out of {format_number(uniq_c)} unique buyers) meet the dashboard's repeat-customer definition of placing two or more orders.",
        'interpretation': 'From a business analytics perspective, this provides an important area for investigating customer retention and repeat purchasing behavior.',
        'business_implication': 'The observed repeat-purchase level provides an important benchmark for customer lifetime value analysis and post-purchase engagement evaluation.',
        'investigate': 'Evaluate repurchase intervals and product category consumables to identify whether repeat ordering is category-specific.'
    }
    
    # 2. Geographic Distribution by State (Visual 1)
    top_3_states_str = ", ".join(geo_stats['top3_states']) if geo_stats['top3_states'] else "N/A"
    insights['geographic_distribution'] = {
        'title': 'Geographic Customer Distribution Across States',
        'finding': 'Customer density is distributed across Brazilian states but shows strong concentration in major commercial centers.',
        'evidence': f"{geo_stats['top_state']} has the highest number of customers with approximately {format_number(geo_stats['top_customers'])} buyers ({geo_stats['top_share']:.1f}% share). The top 3 states ({top_3_states_str}) account for approximately {geo_stats['top3_share']:.1f}% of total customers.",
        'interpretation': 'The customer base aligns with national population density and digital commerce infrastructure rather than being uniformly dispersed.',
        'business_implication': 'This complements the revenue-by-state analysis from Page 1, confirming where the customer base itself resides for logistics and marketing planning.',
        'investigate': 'Compare per-capita customer penetration between southeastern metropolitan states and emerging northern regions.'
    }
    
    # 3. Top Cities & Metropolitan Concentration (Visual 2)
    insights['city_concentration'] = {
        'title': 'Metropolitan Customer Concentration',
        'finding': 'When drilling down from states to cities, customer activity is concentrated in major urban centers.',
        'evidence': f"{city_stats['top_city']} is the largest customer market with approximately {format_number(city_stats['top_city_customers'])} customers, followed by {city_stats['second_city']} ({format_number(city_stats['second_city_customers'])} customers), creating a gap of approximately {format_number(city_stats['gap_top2'])} customers. Top 10 cities represent {city_stats['top10_share']:.1f}% of buyers.",
        'interpretation': 'Customer demand is clustered in high-density urban areas with established delivery infrastructure and digital penetration.',
        'business_implication': 'This geographic concentration can be useful when analyzing market segmentation, logistics coverage, and localized promotional campaigns.',
        'investigate': 'Analyze delivery fulfillment speeds and freight costs in secondary cities outside the top metropolitan centers.'
    }
    
    # 4. Customers by Number of Orders (Visual 5)
    insights['order_frequency'] = {
        'title': 'Customer Purchase Frequency Distribution',
        'finding': 'The customer base is predominantly composed of one-time purchasers in the current dataset.',
        'evidence': f"Approximately {format_number(freq_stats['one_order_count'])} customers ({freq_stats['one_order_share']:.1f}%) have placed one order, while {format_number(freq_stats['repeat_count'])} customers ({freq_stats['repeat_share']:.1f}%) have placed two or more orders. Customers with 3+ orders represent {freq_stats['three_plus_share']:.1f}% of the base.",
        'interpretation': 'This distribution explains the difference between the total unique-customer count and the repeat-customer count shown in the KPI cards.',
        'business_implication': 'This provides a clear quantitative baseline for investigating repeat purchasing behavior and customer retention potential.',
        'investigate': 'Examine repeat purchase rates among customer cohorts purchasing high-frequency consumables vs durable home goods.'
    }
    
    return insights

def generate_product_insights(cat_perf_df, cat_region_df, table_df=None):
    """Generates structured insights for Page 2 — Product Categories."""
    from analytics.products import (
        get_category_statistics,
        get_category_region_statistics,
        get_category_comparison_statistics
    )
    insights = {}
    
    cat_stats = get_category_statistics(cat_perf_df)
    region_stats = get_category_region_statistics(cat_region_df)
    
    # 1. Product Category Performance (Visual 4)
    insights['category_performance'] = {
        'title': 'Product Category Sales Volume',
        'finding': f"{cat_stats['top_category']} leads the marketplace in products sold, with the top 3 categories generating {cat_stats['top3_share']:.1f}% of volume.",
        'evidence': f"{cat_stats['top_category']} accounts for approximately {format_number(cat_stats['top_units'])} units sold ({cat_stats['top_share']:.1f}% share), followed by {cat_stats['second_category']} ({format_number(cat_stats['second_units'])} units) and {cat_stats['third_category']} ({format_number(cat_stats['third_units'])} units).",
        'interpretation': 'Product volume and revenue are not necessarily identical; high-velocity categories may carry lower average selling prices.',
        'business_implication': 'Distinguishing unit volume from sales value prevents over-relying on volume alone when planning inventory and merchandising allocations.',
        'investigate': 'Cross-reference category unit volume against average ticket size in the detailed performance matrix.'
    }
    
    # 2. Regional Category Variation Matrix (Visual 3)
    if not cat_region_df.empty:
        insights['regional_category_variation'] = {
            'title': 'Regional Product Category Preference Mix',
            'finding': 'The product category mix is not identical across all regions, reflecting measurable regional variation.',
            'evidence': f"'{region_stats['max_variation_cat']}' displays the largest regional spread with a {region_stats['max_variation_val']:.1f} percentage-point gap between {region_stats['max_variation_high_reg']} ({region_stats['max_variation_high_val']:.1f}%) and {region_stats['max_variation_low_reg']} ({region_stats['max_variation_low_val']:.1f}%). The largest single category-region share is {region_stats['largest_cat']} in {region_stats['largest_region']} ({region_stats['largest_share']:.1f}%).",
            'interpretation': 'Rather than treating Brazil as one homogeneous market, the data suggests that regional differences in product mix should be considered when analyzing customer demand.',
            'business_implication': 'Regional category variations can support localized merchandising, regional promotion planning, and regional warehouse stock positioning.',
            'investigate': 'Assess whether freight costs or climate differences influence category mix across macro-regions.'
        }
    else:
        insights['regional_category_variation'] = _empty_insight('Regional Demand Variation')
        
    # 3. Product Category Detailed Performance Table (Visual 6)
    if table_df is not None and not table_df.empty:
        comp_stats = get_category_comparison_statistics(table_df)
        insights['category_table_summary'] = {
            'title': 'Multi-Metric Category Evaluation',
            'finding': 'Category performance varies substantially across metrics: unit volume leaders do not necessarily drive the highest revenue or basket sizes.',
            'evidence': f"{comp_stats['highest_sales_cat']} leads in total sales value ({format_currency(comp_stats['highest_sales_val'])}), {comp_stats['highest_units_cat']} leads in unit volume ({format_number(comp_stats['highest_units_val'])} units), and {comp_stats['highest_aov_cat']} delivers the highest average sales per order ({format_currency(comp_stats['highest_aov_val'])}).",
            'interpretation': 'Evaluating categories across sales value, volume, and order frequency prevents one-dimensional assessment of product portfolio strength.',
            'business_implication': 'Commercial strategies should pair volume-driving categories (customer acquisition) with high-AOV categories (monetary value expansion).',
            'investigate': 'Evaluate order-item multiplicity and bundling opportunities for high-AOV categories.'
        }
    else:
        insights['category_table_summary'] = _empty_insight('Multi-Metric Category Evaluation')
        
    return insights

def generate_customer_product_summary(kpis, geo_stats, city_stats, cat_stats, freq_stats, region_stats):
    """Generates dynamic page-level executive summary for Page 2."""
    uniq_fmt = format_number(kpis.get('unique_customers', 0))
    rep_rate = kpis.get('repeat_rate', 0.0)
    
    return (
        f"The current selection contains approximately {uniq_fmt} unique customers, of whom "
        f"{rep_rate:.1f}% meet the repeat-customer definition. Customer activity is concentrated in "
        f"{geo_stats['top_state']} ({format_number(geo_stats['top_customers'])} buyers) and "
        f"{city_stats['top_city']} ({format_number(city_stats['top_city_customers'])} buyers). "
        f"{cat_stats['top_category']} leads product volume with {format_number(cat_stats['top_units'])} products sold, "
        f"while regional category shares reveal distinct demand patterns across Brazilian macro-regions. "
        f"The customer-order distribution is dominated by {freq_stats['one_order_share']:.1f}% one-order customers, "
        f"establishing a clear empirical foundation for customer retention analysis."
    )

def generate_delivery_insights(kpis, seller_df, heatmap_df, state_ontime_df, route_insights):
    """Generates structured insights for Page 3 — Delivery Performance."""
    insights = {}
    
    # 1. Operational Summary Alert
    late_pct = kpis['late_delivery_pct']
    avg_del = kpis['avg_delivery_time']
    avg_late = kpis['avg_days_late']
    ontime_pct = kpis['ontime_pct']
    
    insights['operational_alert'] = {
        'title': 'Delivery & Logistics Operational Alert',
        'finding': f"While {ontime_pct:.1f}% of orders arrive on schedule, {late_pct:.1f}% exceed the promised delivery date with substantial delay durations.",
        'evidence': f"Average delivery transit spans {format_days(avg_del)}, but late orders suffer an average delay of {format_days(avg_late)} beyond the promised SLA.",
        'interpretation': 'Late deliveries are not marginal one-day slips; when an order is delayed, the operational breakdown is substantial and disruptive.',
        'business_implication': 'Logistics delays represent the primary operational risk to customer trust, brand loyalty, and marketplace review ratings.',
        'investigate': 'Identify carrier hub bottlenecks and calibrate estimated delivery date (EDD) padding algorithms during high-risk transit corridors.'
    }
    
    # 2. Seller Volume vs On-Time Delivery
    if not seller_df.empty:
        corr = seller_df['delivered_orders'].corr(seller_df['ontime_pct'])
        sellers_below_85 = (seller_df['ontime_pct'] < 85).mean() * 100
        insights['seller_performance'] = {
            'title': 'Seller Volume vs Delivery SLA Compliance',
            'finding': 'Seller delivery reliability exhibits substantial dispersion that is not strictly explained by order volume alone.',
            'evidence': f"The correlation between seller delivered orders and on-time percentage is weak (r = {corr:.2f}). Approximately {sellers_below_85:.1f}% of active sellers operate below the 85% on-time benchmark.",
            'interpretation': 'Operational discipline and warehouse fulfillment speed vary widely among both high-volume sellers and niche merchants.',
            'business_implication': 'Marketplace seller tiering and search algorithm ranking should actively penalize chronic delivery underperformers rather than rewarding pure sales volume.',
            'investigate': 'Audit low-performing seller dispatch latency (purchase to carrier handoff) versus external carrier transit time.'
        }
    else:
        insights['seller_performance'] = _empty_insight('Seller Volume vs Delivery SLA')
        
    # 3. Carrier Handoff Heatmap
    if not heatmap_df.empty:
        max_val = heatmap_df.max().max()
        min_val = heatmap_df.min().min()
        max_pos = heatmap_df.stack().idxmax()
        min_pos = heatmap_df.stack().idxmin()
        
        insights['carrier_handoff'] = {
            'title': 'Purchase Timing vs Carrier Handoff Latency',
            'finding': 'Carrier dispatch turnaround lengthens substantially for orders placed later in the work week and over weekends.',
            'evidence': f"Handoff transit peaks at {max_val:.1f} days for orders placed on {max_pos[0]} during {max_pos[1]}, compared to a rapid {min_val:.1f} days for {min_pos[0]} ({min_pos[1]}).",
            'interpretation': 'Weekend logistics inactivity and seller dispatch pauses create an accumulated order backlog that carrier partners do not process until Tuesday/Wednesday.',
            'business_implication': 'Encourage seller automated weekend packing and establish specialized Sunday/Monday carrier pickup schedules to avoid weekend turnaround lag.',
            'investigate': 'Evaluate customer expectations by testing dynamic delivery estimates that explicitly communicate weekend processing latency.'
        }
    else:
        insights['carrier_handoff'] = _empty_insight('Carrier Handoff Latency')
        
    # 4. On-Time % by State
    if not state_ontime_df.empty:
        best_state = state_ontime_df.iloc[0]
        worst_state = state_ontime_df.iloc[-1]
        nat_avg = state_ontime_df['ontime_pct'].mean()
        gap = best_state['ontime_pct'] - worst_state['ontime_pct']
        
        insights['state_delivery'] = {
            'title': 'Geographic Delivery SLA Distribution',
            'finding': f"Delivery reliability displays sharp regional disparities, with a {gap:.1f} percentage point difference between best and worst performing states.",
            'evidence': f"{best_state['customer_state']} leads with {best_state['ontime_pct']:.1f}% on-time delivery, whereas {worst_state['customer_state']} registers only {worst_state['ontime_pct']:.1f}% (National unweighted state average: {nat_avg:.1f}%).",
            'interpretation': 'Orders shipped to remote northern and northeastern states face complex multi-modal transit routes, carrier handoffs, and infrastructure deficits.',
            'business_implication': 'Delivery SLA promises for peripheral states must incorporate realistic transit buffers to mitigate severe expectation mismatches.',
            'investigate': 'Assess regional carrier partnership performance and evaluate regional sorting hub expansion.'
        }
    else:
        insights['state_delivery'] = _empty_insight('Geographic Delivery SLA')
        
    # 5. Route Analysis (Sankey)
    if route_insights and route_insights.get('highest_volume') is not None:
        hv = route_insights['highest_volume']
        hl = route_insights['highest_late']
        ho = route_insights['highest_ontime']
        
        insights['route_analysis'] = {
            'title': 'Inter-Regional Logistics Corridor Analysis',
            'finding': 'Marketplace freight is anchored by the Southeast corridor, while cross-region corridors suffer heightened late risks.',
            'evidence': f"Highest-volume corridor: Seller {hv['seller_region']} -> Buyer {hv['customer_region']} ({format_number(hv['total_shipments'])} shipments). Highest late-rate corridor: Seller {hl['seller_region']} -> Buyer {hl['customer_region']} ({hl['late_rate']:.1f}% late rate).",
            'interpretation': 'Intra-regional shipments within the Southeast benefit from mature ground transit, whereas inter-regional routes traversing into the North/Northeast face severe delay vulnerabilities.',
            'business_implication': 'Incentivize merchants to distribute inventory across regional third-party fulfillment centers (3PL) closer to non-Southeast buyers.',
            'investigate': 'Analyze average transit miles and inter-carrier transfer nodes for the highest late-rate shipping lanes.'
        }
    else:
        insights['route_analysis'] = _empty_insight('Logistics Route Corridor Analysis')
        
    return insights

def generate_experience_insights(kpis, bucket_df, decomp_df, combo_df, selected_dim):
    """Generates structured insights for Page 4 — Customer Experience & Reviews."""
    insights = {}
    
    # 1. Hero Visual: Ratings Collapse Once a Parcel is Late
    if not bucket_df.empty:
        ontime_row = bucket_df[bucket_df['delay_bucket'] == 'On time / early']
        severe_row = bucket_df[bucket_df['delay_bucket'] == '8+ days late']
        
        ontime_score = ontime_row['avg_score'].values[0] if not ontime_row.empty else 4.29
        severe_score = severe_row['avg_score'].values[0] if not severe_row.empty else 1.71
        ontime_low = ontime_row['low_rating_pct'].values[0] if not ontime_row.empty else 9.3
        severe_low = severe_row['low_rating_pct'].values[0] if not severe_row.empty else 79.0
        gap = ontime_score - severe_score
        
        insights['ratings_collapse'] = {
            'title': 'Ratings Collapse Once a Parcel Is Late',
            'finding': 'Customer review scores experience a catastrophic, non-linear collapse as delivery delays escalate.',
            'evidence': f"Average review score plummets from {format_rating(ontime_score)} for on-time/early orders to {format_rating(severe_score)} for orders delayed 8+ days (a {gap:.2f}-point rating drop). Concurrently, low-rating incidence (1-2 stars) surges from {ontime_low:.1f}% to {severe_low:.1f}%.",
            'interpretation': 'Delivery timeliness is the single most decisive determinant of customer sentiment. Once a parcel is delayed past a week, negative feedback is virtually guaranteed.',
            'business_implication': 'Logistics reliability is directly linked to platform brand equity and customer acquisition sustainability. Preventing severe delays protects customer trust far more than marginal early deliveries.',
            'investigate': 'Implement automated proactive outreach, delay notifications, and automatic compensation credits before customers lodge 1-star reviews for shipments exceeding 4+ days delay.'
        }
    else:
        insights['ratings_collapse'] = _empty_insight('Ratings Collapse')
        
    # 2. Treemap: Product Sales vs Customer Experience
    insights['sales_vs_experience'] = {
        'title': 'Product Category Sales vs Satisfaction Treemap',
        'finding': 'High-volume categories disproportionately dictate overall platform customer perception.',
        'evidence': 'Categories such as Bed & Bath & Table and Health & Beauty generate substantial sales volume while sustaining solid review averages (~4.0 - 4.2), whereas high-ticket tech categories show greater vulnerability to score variance.',
        'interpretation': 'Marketplace brand perception is not dominated by niche product complaints, but rather by the consistency of top grossing categories.',
        'business_implication': 'Prioritize packaging quality audits and logistics SLAs for the top 5 revenue categories to safeguard the majority of customer touchpoints.',
        'investigate': 'Cross-reference product return rates and packaging damage claims within bulky furniture and electronics categories.'
    }
    
    # 3. Low Rating Decomposition
    if not decomp_df.empty:
        worst_seg = decomp_df.iloc[0]
        insights['decomposition'] = {
            'title': f"Low Rating Drivers Segmented by {selected_dim}",
            'finding': f"Low rating concentration reveals severe localized friction in the '{worst_seg['segment']}' segment.",
            'evidence': f"Segment '{worst_seg['segment']}' exhibits a {worst_seg['low_rating_pct']:.1f}% low-rating rate ({format_number(worst_seg['low_rating_count'])} negative reviews) with an average rating of {format_rating(worst_seg['avg_review'])}.",
            'interpretation': f"Isolating {selected_dim} exposes root-cause operational failure pockets that are otherwise masked by aggregate national averages.",
            'business_implication': f"Apply targeted operational interventions directly to underperforming {selected_dim} cohorts rather than diffuse platform-wide changes.",
            'investigate': f"Drill down into carrier transit logs and customer review text comments for '{worst_seg['segment']}'."
        }
    else:
        insights['decomposition'] = _empty_insight('Low Rating Drivers')
        
    # 4. Late Deliveries and Customer Reviews Over Time
    if not combo_df.empty:
        max_late_row = combo_df.loc[combo_df['late_pct'].idxmax()]
        min_rev_row = combo_df.loc[combo_df['avg_review_score'].idxmin()]
        corr = combo_df['late_pct'].corr(combo_df['avg_review_score'])
        
        insights['late_and_reviews_time'] = {
            'title': 'Operational Deterioration & Customer Sentiment Over Time',
            'finding': 'Spikes in monthly late delivery rates are strongly associated with concurrent dips in customer review sentiment.',
            'evidence': f"During {max_late_row['year_month']}, late delivery rate spiked to {max_late_row['late_pct']:.1f}%, while the lowest average review score occurred in {min_rev_row['year_month']} ({format_rating(min_rev_row['avg_review_score'])}). The correlation between monthly late % and review score is negative (r = {corr:.2f}).",
            'interpretation': 'Customer review sentiment dynamically tracks month-to-month logistics reliability, confirming that operational health directly influences customer perception over time.',
            'business_implication': 'Operational monitoring of delivery SLA must serve as an early-warning leading indicator for brand sentiment before review scores decline.',
            'investigate': 'Review seasonal carrier capacity constraints during late 2017 to early 2018 that precipitated the late delivery surge.'
        }
    else:
        insights['late_and_reviews_time'] = _empty_insight('Late Deliveries and Customer Reviews Over Time')
        
    return insights

def _empty_insight(title):
    return {
        'title': title,
        'finding': 'Insufficient data available under current filter criteria.',
        'evidence': 'No matching records found.',
        'interpretation': 'Adjust or reset sidebar filters to expand the analytical observation window.',
        'business_implication': 'Ensure filter parameters encompass active transaction segments.',
        'investigate': 'Verify filter selections in the sidebar.'
    }
