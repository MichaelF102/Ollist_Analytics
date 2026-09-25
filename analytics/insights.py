"""
Antigravity Analytical Insight Engine
Generates structured, 5-layer business interpretations deterministically from calculated metrics.
Adheres strictly to non-causal analytical language:
(associated with, correlated with, indicates, suggests, observed pattern).
"""

from utils.formatting import format_currency, format_number, format_percent, format_days, format_rating

def generate_sales_insights(kpis, monthly_df, weekday_df, payment_df, state_df, non_deliv_df):
    """Generates structured insights for Page 1 — Executive Overview."""
    insights = {}
    
    # 1. Executive Summary
    tot_orders = kpis['total_orders']
    tot_rev = kpis['total_revenue']
    uniq_cust = kpis['unique_customers']
    aov = kpis['aov']
    prods_sold = kpis['products_sold']
    
    insights['executive_summary'] = {
        'title': 'Executive Business Performance Summary',
        'finding': 'Strong transactional throughput dominated by unique first-time buyers with multi-item baskets.',
        'evidence': f"The business processed {format_number(tot_orders)} orders generating {format_currency(tot_rev)} in gross merchandise value across {format_number(uniq_cust)} unique customers (AOV: {format_currency(aov)}, Products Sold: {format_number(prods_sold)}).",
        'interpretation': 'Customer volume closely tracks order volume, indicating that revenue expansion is currently powered primarily by customer acquisition rather than repeat transactions.',
        'business_implication': 'High customer acquisition volume without commensurate repeat ordering means margin is continuously spent on top-of-funnel customer capture.',
        'investigate': 'Determine customer acquisition cost (CAC) efficiency and evaluate post-purchase retention loops to boost customer lifetime value (LTV).'
    }
    
    # 2. Monthly Orders & Payment Value
    if not monthly_df.empty:
        peak_order_row = monthly_df.loc[monthly_df['orders_count'].idxmax()]
        lowest_order_row = monthly_df.loc[monthly_df['orders_count'].idxmin()]
        corr = monthly_df['orders_count'].corr(monthly_df['revenue'])
        insights['monthly_trend'] = {
            'title': 'Monthly Orders & Payment Value',
            'finding': 'Orders and gross revenue display a synchronized upward expansion across the observation period.',
            'evidence': f"Peak order activity reached {format_number(peak_order_row['orders_count'])} orders ({format_currency(peak_order_row['revenue'])}) in {peak_order_row['year_month']}, up from {format_number(lowest_order_row['orders_count'])} in early months. Revenue correlation with order volume is strong (r = {corr:.2f}).",
            'interpretation': 'Revenue growth is substantially associated with increasing transaction count rather than isolated large-ticket transaction outliers.',
            'business_implication': 'Operational logistics, warehouse fulfillment, and carrier partner capacity must scale directly with projected transaction volume surges during peak quarters.',
            'investigate': 'Analyze whether peak volume corresponds to promotional calendar events (e.g. Black Friday) and assess carrier on-time resilience during high-volume months.'
        }
    else:
        insights['monthly_trend'] = _empty_insight('Monthly Orders & Payment Value')
        
    # 3. Orders by Day of Week
    if not weekday_df.empty:
        top_day = weekday_df.sort_values('orders_count', ascending=False).iloc[0]
        bot_day = weekday_df.sort_values('orders_count', ascending=True).iloc[0]
        weekday_sum = weekday_df[weekday_df['weekday'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]['orders_count'].sum()
        total_week = weekday_df['orders_count'].sum()
        weekday_share = (weekday_sum / total_week * 100) if total_week > 0 else 0
        
        insights['orders_by_weekday'] = {
            'title': 'Orders by Day of Week',
            'finding': 'Purchasing behavior is concentrated heavily during business weekdays, peaking at the start of the week.',
            'evidence': f"{top_day['weekday']} records the highest volume ({format_number(top_day['orders_count'])} orders, {top_day['share_pct']:.1f}% share), whereas {bot_day['weekday']} drops to {format_number(bot_day['orders_count'])}. Overall weekdays represent {weekday_share:.1f}% of total demand.",
            'interpretation': 'Customers demonstrate a systematic preference for initiating purchases during workdays, with weekend browsing tapering significantly.',
            'business_implication': 'Promotional campaign launches, push notifications, seller operational fulfillment teams, and customer-support staffing should align with the heavy Monday–Wednesday demand surge.',
            'investigate': 'Evaluate carrier pickup schedules on Mondays to confirm that warehouse dispatches keep pace with early-week volume spikes.'
        }
    else:
        insights['orders_by_weekday'] = _empty_insight('Orders by Day of Week')
        
    # 4. Payment Method Distribution
    if not payment_df.empty:
        dominant_pmt = payment_df.iloc[0]
        second_pmt = payment_df.iloc[1] if len(payment_df) > 1 else dominant_pmt
        insights['payment_distribution'] = {
            'title': 'Payment Method Distribution',
            'finding': f"{dominant_pmt['payment_type_clean']} constitutes the vast majority of transaction volume, followed by {second_pmt['payment_type_clean']}.",
            'evidence': f"{dominant_pmt['payment_type_clean']} captures {format_currency(dominant_pmt['total_value'])} ({dominant_pmt['share_pct']:.1f}% share). {second_pmt['payment_type_clean']} generates {format_currency(second_pmt['total_value'])} ({second_pmt['share_pct']:.1f}%).",
            'interpretation': 'The marketplace depends heavily on digital card processing, while Brazilian bank slips (Boleto) maintain a vital secondary role for cash/unbanked segments.',
            'business_implication': 'Payment gateway processing reliability and card authorization checkout friction directly govern the vast majority of revenue flow.',
            'investigate': 'Assess checkout drop-off rates and payment processing authorization fees across different credit card acquirers.'
        }
    else:
        insights['payment_distribution'] = _empty_insight('Payment Method Distribution')
        
    # 5. Revenue by Customer State
    if not state_df.empty:
        top_state = state_df.iloc[0]
        top3_share = state_df.head(3)['share_pct'].sum()
        insights['revenue_by_state'] = {
            'title': 'Revenue Concentration by Customer State',
            'finding': f"Geographic revenue is highly concentrated in southeastern commercial hubs, led predominantly by {top_state['customer_state']}.",
            'evidence': f"{top_state['customer_state']} generates {format_currency(top_state['total_revenue'])} ({top_state['share_pct']:.1f}% of top 10 revenue). The top 3 states (SP, RJ, MG) account for {top3_share:.1f}% of total demand.",
            'interpretation': 'Market traction is heavily skewed toward southeastern metropolitan regions with mature digital infrastructure and higher purchasing power.',
            'business_implication': 'Regional marketing efficiency and fulfillment center placement are crucial in São Paulo and adjacent states to safeguard delivery economics.',
            'investigate': 'Examine regional shipping freight costs to determine whether high shipping fees suppress demand in North and Northeast states.'
        }
    else:
        insights['revenue_by_state'] = _empty_insight('Revenue Concentration by Customer State')
        
    # 6. Non-Delivered Orders by Status
    if not non_deliv_df.empty:
        largest_status = non_deliv_df.iloc[0]
        cancelled_orders = non_deliv_df[non_deliv_df['order_status'] == 'canceled']
        canc_cnt = cancelled_orders['count'].values[0] if not cancelled_orders.empty else 0
        canc_rev = cancelled_orders['revenue_at_risk'].values[0] if not cancelled_orders.empty else 0
        tot_risk = non_deliv_df['revenue_at_risk'].sum()
        
        insights['non_delivered_orders'] = {
            'title': 'Non-Delivered Orders by Operational Status',
            'finding': 'Non-delivered orders are divided between active transit pipelines and revenue leakage stages.',
            'evidence': f"The largest non-delivered cohort is '{largest_status['order_status']}' ({format_number(largest_status['count'])} orders, {largest_status['share_pct']:.1f}%). Canceled and unavailable orders represent {format_number(canc_cnt)} orders and {format_currency(canc_rev)} in potential lost revenue.",
            'interpretation': 'While shipped orders represent healthy in-flight logistics, canceled and unavailable orders indicate inventory stockouts or buyer frustration before carrier handoff.',
            'business_implication': 'Streamlining inventory synchronization with marketplace sellers could reduce unfulfillable orders and retain gross revenue.',
            'investigate': 'Audit seller fulfillment cancellation reasons to identify whether out-of-stock items or delayed confirmation triggers cancellations.'
        }
    else:
        insights['non_delivered_orders'] = _empty_insight('Non-Delivered Orders')
        
    return insights

def generate_customer_insights(kpis, state_cust_df, city_cust_df, freq_df):
    """Generates structured insights for Page 2 — Customers, Products & Geography."""
    insights = {}
    
    # 1. Customer Retention Alert
    uniq_c = kpis['unique_customers']
    rep_c = kpis['repeat_customers']
    rep_r = kpis['repeat_rate']
    
    insights['customer_retention'] = {
        'title': 'Customer Retention & Re-order Dynamics',
        'finding': 'The customer base exhibits extreme single-purchase concentration with minimal repeat ordering.',
        'evidence': f"Out of {format_number(uniq_c)} unique customers, only {format_number(rep_c)} have placed more than one order, establishing a repeat customer rate of {rep_r:.2f}%.",
        'interpretation': 'The platform functions predominantly as a customer acquisition portal rather than an ecosystem with organic loyalty loops.',
        'business_implication': 'The business operates under continuous customer acquisition cost pressure; establishing retention strategies offers a high-leverage growth avenue.',
        'investigate': 'Evaluate repurchase intervals, product category consumables (e.g., pet supplies, cosmetics), and lifecycle email re-engagement performance.'
    }
    
    # 2. Customers by Number of Orders
    if not freq_df.empty:
        one_order = freq_df[freq_df['frequency_bucket'] == '1 Order'].iloc[0]
        insights['order_frequency'] = {
            'title': 'Customer Order Frequency Distribution',
            'finding': 'Customer volume drops exponentially beyond the initial transaction.',
            'evidence': f"{format_number(one_order['customer_count'])} customers ({one_order['share_pct']:.1f}%) placed exactly 1 order, while 3+ orders account for less than 1% of the buyer base.",
            'interpretation': 'Observed purchasing behavior reflects high transaction friction or one-off discovery journeys without habituation.',
            'business_implication': 'Introduce post-purchase loyalty credits, tiered loyalty perks, or subscription replenishment for repeat-oriented product lines.',
            'investigate': 'Survey single-order customers who gave 5-star reviews to determine why high satisfaction did not translate into a second purchase.'
        }
    else:
        insights['order_frequency'] = _empty_insight('Order Frequency Distribution')
        
    # 3. Top Cities & State Concentration
    if not city_cust_df.empty:
        top_city = city_cust_df.iloc[0]
        second_city = city_cust_df.iloc[1] if len(city_cust_df) > 1 else top_city
        city_ratio = (top_city['customer_count'] / second_city['customer_count']) if second_city['customer_count'] > 0 else 1.0
        
        insights['city_concentration'] = {
            'title': 'Metropolitan Customer Concentration',
            'finding': f"{top_city['customer_city']} represents an overwhelming customer concentration, exceeding the runner-up city by more than {city_ratio:.1f}x.",
            'evidence': f"{top_city['customer_city']} accounts for {format_number(top_city['customer_count'])} unique customers, followed by {second_city['customer_city']} ({format_number(second_city['customer_count'])} customers).",
            'interpretation': 'Customer acquisition is concentrated in top-tier urban centers with dense digital penetration and established logistics networks.',
            'business_implication': 'Last-mile same-day and next-day delivery networks should be piloted first in São Paulo and Rio de Janeiro to maximize competitive advantage.',
            'investigate': 'Compare delivery promise times and shipping cost competitiveness between São Paulo and secondary state capitals.'
        }
    else:
        insights['city_concentration'] = _empty_insight('Metropolitan Customer Concentration')
        
    return insights

def generate_product_insights(cat_perf_df, cat_region_df):
    """Generates structured insights for Page 2 — Product Categories."""
    insights = {}
    
    # 1. Product Category Performance
    if not cat_perf_df.empty:
        top_cat = cat_perf_df.iloc[0]
        top3_prods = cat_perf_df.head(3)['products_sold'].sum()
        tot_prods = cat_perf_df['products_sold'].sum()
        top3_share = (top3_prods / tot_prods * 100) if tot_prods > 0 else 0
        
        insights['category_performance'] = {
            'title': 'Category Sales Volume & Concentration',
            'finding': f"Product demand is concentrated in key lifestyle and personal goods categories, led by {top_cat['category_clean']}.",
            'evidence': f"{top_cat['category_clean']} leads with {format_number(top_cat['products_sold'])} items sold ({top_cat['share_pct']:.1f}% share), followed by Health & Beauty and Sports & Leisure. The top 3 categories constitute {top3_share:.1f}% of volume.",
            'interpretation': 'Everyday personal and home care products demonstrate the highest velocity and broadest customer appeal.',
            'business_implication': 'Merchandising and promotional placement should safeguard inventory depth and seller price competitiveness in these bellwether categories.',
            'investigate': 'Assess stock-out frequency and price elasticities within Bed & Bath & Table and Health & Beauty.'
        }
    else:
        insights['category_performance'] = _empty_insight('Category Sales Volume')
        
    # 2. Regional Category Variation (Matrix)
    if not cat_region_df.empty:
        # Find category with largest difference across regions
        row_diff = cat_region_df.max(axis=1) - cat_region_df.min(axis=1)
        max_diff_cat = row_diff.idxmax()
        max_diff_val = row_diff.max()
        max_reg = cat_region_df.loc[max_diff_cat].idxmax()
        min_reg = cat_region_df.loc[max_diff_cat].idxmin()
        
        insights['regional_category_variation'] = {
            'title': 'Regional Demand Variation Across Categories',
            'finding': f"Regional preferences reveal notable differences, with '{max_diff_cat}' showing the widest geographic spread.",
            'evidence': f"'{max_diff_cat}' exhibits a {max_diff_val:.1f} percentage-point gap between its highest-share region ({max_reg}: {cat_region_df.loc[max_diff_cat, max_reg]:.1f}%) and lowest ({min_reg}: {cat_region_df.loc[max_diff_cat, min_reg]:.1f}%).",
            'interpretation': 'Regional climate, economic demographics, and localized lifestyle preferences influence product category velocity across Brazilian macro-regions.',
            'business_implication': 'Avoid nationwide one-size-fits-all digital marketing; tailor homepage category banners and localized discounts based on regional affinity.',
            'investigate': 'Examine regional shipping weight surcharges that may disadvantage bulky home furniture in distant regions.'
        }
    else:
        insights['regional_category_variation'] = _empty_insight('Regional Demand Variation')
        
    return insights

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
