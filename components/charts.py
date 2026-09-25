import os
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.formatting import format_currency, format_number

# Color Palette Constants
COLOR_INDIGO = "#6366F1"
COLOR_CYAN = "#38BDF8"
COLOR_EMERALD = "#10B981"
COLOR_AMBER = "#F59E0B"
COLOR_ROSE = "#F43F5E"
COLOR_VIOLET = "#8B5CF6"
COLOR_SLATE = "#334155"
COLOR_MUTED = "#64748B"

FONT_FAMILY = "Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"

def apply_chart_theme(fig, height=380, show_legend=False):
    """Applies unified dark theme styling to Plotly figures."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=35, b=25),
        height=height,
        font=dict(family=FONT_FAMILY, color="#94A3B8", size=11),
        showlegend=show_legend,
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=12,
            font_family=FONT_FAMILY,
            font_color="#F8FAFC",
            bordercolor="rgba(255,255,255,0.15)"
        )
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        tickfont=dict(color="#94A3B8", size=10),
        title_font=dict(color="#94A3B8", size=11)
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.05)",
        zeroline=False,
        tickfont=dict(color="#94A3B8", size=10),
        title_font=dict(color="#94A3B8", size=11)
    )
    return fig

# ----------------- PAGE 1 CHARTS -----------------

def create_monthly_combo_chart(monthly_df):
    """Page 1 Visual 1: Monthly Orders (Bars) & Payment Value (Line)"""
    fig = go.Figure()
    
    # Bars for Orders
    fig.add_trace(go.Bar(
        x=monthly_df['year_month'],
        y=monthly_df['orders_count'],
        name="Orders",
        marker=dict(color=COLOR_INDIGO, opacity=0.85, cornerradius=4),
        yaxis="y1",
        hovertemplate="<b>%{x}</b><br>Orders: %{y:,.0f}<extra></extra>"
    ))
    
    # Line for Revenue
    fig.add_trace(go.Scatter(
        x=monthly_df['year_month'],
        y=monthly_df['revenue'],
        name="Payment Value (R$)",
        mode="lines+markers",
        line=dict(color=COLOR_AMBER, width=2.5),
        marker=dict(size=5, color=COLOR_AMBER),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Revenue: R$ %{y:,.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        yaxis=dict(
            title="Monthly Orders",
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)"
        ),
        yaxis2=dict(
            title="Revenue (R$)",
            overlaying="y",
            side="right",
            showgrid=False,
            tickprefix="R$ "
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#CBD5E1", size=10)
        )
    )
    return apply_chart_theme(fig, height=380, show_legend=True)

def create_weekday_bar_chart(weekday_df):
    """Page 1 Visual 2: Orders by Day of Week"""
    # Color top day distinctively
    max_orders = weekday_df['orders_count'].max()
    colors = [COLOR_CYAN if o == max_orders else COLOR_INDIGO for o in weekday_df['orders_count']]
    
    fig = go.Figure(go.Bar(
        x=weekday_df['weekday'],
        y=weekday_df['orders_count'],
        marker=dict(color=colors, cornerradius=4),
        text=[f"{v/1000:.1f}K" if v >= 1000 else str(v) for v in weekday_df['orders_count']],
        textposition="outside",
        textfont=dict(color="#CBD5E1", size=10),
        hovertemplate="<b>%{x}</b><br>Orders: %{y:,.0f}<br>Share: %{customdata:.1f}%<extra></extra>",
        customdata=weekday_df['share_pct']
    ))
    
    fig.update_layout(
        xaxis=dict(title="Day of Week"),
        yaxis=dict(title="Orders", showgrid=True)
    )
    return apply_chart_theme(fig, height=340)

def create_payment_donut_chart(payment_df):
    """Page 1 Visual 3: Payment Method Distribution"""
    palette = [COLOR_CYAN, COLOR_INDIGO, COLOR_AMBER, COLOR_EMERALD, COLOR_ROSE]
    
    tot_val = payment_df['total_value'].sum()
    center_text = f"<b>{format_currency(tot_val)}</b><br><span style='font-size: 10px; color: #94A3B8;'>Total Volume</span>"
    
    fig = go.Figure(go.Pie(
        labels=payment_df['payment_type_clean'],
        values=payment_df['total_value'],
        hole=0.62,
        marker=dict(colors=palette, line=dict(color="#0B0F19", width=2)),
        textinfo="percent",
        textposition="inside",
        textfont=dict(color="#FFFFFF", size=10, family=FONT_FAMILY),
        hovertemplate="<b>%{label}</b><br>Value: R$ %{value:,.2f}<br>Share: %{percent}<extra></extra>"
    ))
    
    fig.add_annotation(
        text=center_text,
        x=0.5, y=0.5,
        font=dict(size=14, color="#FFFFFF", family=FONT_FAMILY),
        showarrow=False
    )
    
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(color="#CBD5E1", size=11)
        )
    )
    return apply_chart_theme(fig, height=340, show_legend=True)

def create_horizontal_bar(df, y_col, x_col, title, x_label="Revenue (R$)", color=COLOR_INDIGO):
    """Visual for Horizontal Bars (Top States, Top Cities, etc.)"""
    # Reverse so top is at top of vertical axis
    plot_df = df.iloc[::-1].copy()
    
    fig = go.Figure(go.Bar(
        x=plot_df[x_col],
        y=plot_df[y_col],
        orientation="h",
        marker=dict(color=color, cornerradius=3),
        hovertemplate="<b>%{y}</b><br>Total: %{x:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        xaxis=dict(title=x_label),
        yaxis=dict(title="")
    )
    return apply_chart_theme(fig, height=340)

def create_non_delivered_donut(non_deliv_df):
    """Page 1 Visual 5: Non-Delivered Orders by Status"""
    palette = [COLOR_CYAN, COLOR_ROSE, COLOR_AMBER, COLOR_VIOLET, COLOR_EMERALD, COLOR_SLATE]
    tot_cnt = non_deliv_df['count'].sum()
    center_text = f"<b>{format_number(tot_cnt)}</b><br><span style='font-size: 10px; color: #94A3B8;'>Non-Delivered</span>"
    
    fig = go.Figure(go.Pie(
        labels=non_deliv_df['order_status'],
        values=non_deliv_df['count'],
        hole=0.62,
        marker=dict(colors=palette, line=dict(color="#0B0F19", width=2)),
        textinfo="percent",
        textposition="inside",
        textfont=dict(color="#FFFFFF", size=10),
        hovertemplate="<b>Status: %{label}</b><br>Orders: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
    ))
    
    fig.add_annotation(
        text=center_text,
        x=0.5, y=0.5,
        font=dict(size=14, color="#FFFFFF", family=FONT_FAMILY),
        showarrow=False
    )
    
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(color="#CBD5E1", size=10)
        )
    )
    return apply_chart_theme(fig, height=340, show_legend=True)

# ----------------- PAGE 2 CHARTS -----------------

def create_brazil_map(state_df, value_col, title, color_scale="Blues", is_percent=False):
    """
    Renders Brazil Choropleth Map using local GeoJSON.
    """
    geojson_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'brazil_geo.json')
    with open(geojson_path, 'r', encoding='utf-8') as f:
        brazil_geo = json.load(f)
        
    hover_fmt = "%{z:.1f}%" if is_percent else "%{z:,.0f}"
    
    fig = go.Figure(go.Choropleth(
        geojson=brazil_geo,
        locations=state_df['customer_state'],
        z=state_df[value_col],
        featureidkey="properties.sigla",
        colorscale=color_scale,
        marker_line_color="rgba(255,255,255,0.2)",
        marker_line_width=0.75,
        colorbar=dict(
            title=dict(text="", font=dict(color="#CBD5E1", size=10)),
            tickfont=dict(color="#94A3B8", size=9),
            thickness=10,
            len=0.7
        ),
        hovertemplate="<b>State: %{location}</b><br>Value: " + hover_fmt + "<extra></extra>"
    ))
    
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_category_matrix_heatmap(matrix_df):
    """Page 2 Visual 3: Category Share by Region Matrix Heatmap"""
    fig = px.imshow(
        matrix_df,
        labels=dict(x="Region", y="Category", color="Share %"),
        x=matrix_df.columns,
        y=matrix_df.index,
        color_continuous_scale="Blues",
        text_auto=".1f"
    )
    
    fig.update_layout(
        height=420,
        coloraxis_colorbar=dict(
            title="Share %",
            thickness=10,
            len=0.7,
            tickfont=dict(color="#94A3B8", size=9)
        )
    )
    fig.update_traces(textfont=dict(size=10, color="#FFFFFF"))
    return apply_chart_theme(fig, height=420)

def create_order_frequency_bar(freq_df):
    """Page 2 Visual 5: Customers by Number of Orders"""
    colors = [COLOR_CYAN, COLOR_INDIGO, COLOR_VIOLET, COLOR_SLATE]
    
    fig = go.Figure(go.Bar(
        x=freq_df['frequency_bucket'],
        y=freq_df['customer_count'],
        marker=dict(color=colors[:len(freq_df)], cornerradius=4),
        text=[f"{v/1000:.1f}K" if v >= 1000 else str(v) for v in freq_df['customer_count']],
        textposition="outside",
        textfont=dict(color="#CBD5E1", size=11),
        hovertemplate="<b>%{x}</b><br>Customers: %{y:,.0f}<br>Share: %{customdata:.2f}%<extra></extra>",
        customdata=freq_df['share_pct']
    ))
    
    fig.update_layout(
        xaxis=dict(title="Order Frequency Bucket"),
        yaxis=dict(title="Customer Count", showgrid=True)
    )
    return apply_chart_theme(fig, height=340)

# ----------------- PAGE 3 CHARTS -----------------

def create_seller_scatter_chart(seller_df):
    """Page 3 Visual 1: Seller Volume vs On-Time Delivery"""
    fig = go.Figure()
    
    # Scatter points
    fig.add_trace(go.Scatter(
        x=seller_df['delivered_orders'],
        y=seller_df['ontime_pct'],
        mode="markers",
        marker=dict(
            size=7,
            color=COLOR_CYAN,
            opacity=0.65,
            line=dict(width=0.5, color="#FFFFFF")
        ),
        hovertemplate="<b>Seller ID:</b> %{customdata}<br>Delivered Orders: %{x:,.0f}<br>On-Time Rate: %{y:.1f}%<extra></extra>",
        customdata=seller_df['seller_id'].str[:8] + "..."
    ))
    
    # Reference Line at 85% On-Time
    fig.add_hline(
        y=85,
        line_dash="dash",
        line_color="#F43F5E",
        line_width=1.5,
        annotation_text="85% Benchmark SLA",
        annotation_position="bottom right",
        annotation_font=dict(color="#FDA4AF", size=10)
    )
    
    fig.update_layout(
        xaxis=dict(title="Seller Orders Delivered", showgrid=True),
        yaxis=dict(title="On-Time Delivery %", range=[30, 105], showgrid=True)
    )
    return apply_chart_theme(fig, height=360)

def create_carrier_heatmap(pivot_df):
    """Page 3 Visual 2: Purchase Timing vs Carrier Handoff Heatmap"""
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Purchase Time Window", y="Purchase Weekday", color="Handoff Days"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="Reds",
        text_auto=".1f"
    )
    
    fig.update_layout(
        height=360,
        coloraxis_colorbar=dict(
            title="Days",
            thickness=10,
            len=0.7,
            tickfont=dict(color="#94A3B8", size=9)
        )
    )
    fig.update_traces(textfont=dict(size=10, color="#FFFFFF"))
    return apply_chart_theme(fig, height=360)

def create_sankey_diagram(routes_df):
    """
    Page 3 Visual 4: Buyer Region -> Seller Region -> Delivery Outcome Sankey
    """
    if routes_df.empty:
        return go.Figure()
        
    buyer_nodes = [f"Buyer: {r}" for r in sorted(routes_df['customer_region'].unique())]
    seller_nodes = [f"Seller: {r}" for r in sorted(routes_df['seller_region'].unique())]
    outcome_nodes = sorted(routes_df['delivery_outcome'].unique())
    
    all_nodes = buyer_nodes + seller_nodes + outcome_nodes
    node_map = {name: i for i, name in enumerate(all_nodes)}
    
    # 1. Flow: Buyer -> Seller
    b_to_s = routes_df.groupby(['customer_region', 'seller_region'])['count'].sum().reset_index()
    sources = [node_map[f"Buyer: {r['customer_region']}"] for _, r in b_to_s.iterrows()]
    targets = [node_map[f"Seller: {r['seller_region']}"] for _, r in b_to_s.iterrows()]
    values = b_to_s['count'].tolist()
    
    # 2. Flow: Seller -> Outcome
    s_to_o = routes_df.groupby(['seller_region', 'delivery_outcome'])['count'].sum().reset_index()
    sources += [node_map[f"Seller: {r['seller_region']}"] for _, r in s_to_o.iterrows()]
    targets += [node_map[r['delivery_outcome']] for _, r in s_to_o.iterrows()]
    values += s_to_o['count'].tolist()
    
    # Node colors
    node_colors = []
    for n in all_nodes:
        if "Buyer:" in n:
            node_colors.append(COLOR_INDIGO)
        elif "Seller:" in n:
            node_colors.append(COLOR_CYAN)
        elif n == "On time":
            node_colors.append(COLOR_EMERALD)
        elif n == "Late":
            node_colors.append(COLOR_ROSE)
        else:
            node_colors.append(COLOR_AMBER)
            
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=18,
            line=dict(color="#0B0F19", width=0.5),
            label=all_nodes,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(148, 163, 184, 0.15)"
        )
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=15, r=15, t=25, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color="#CBD5E1", size=11)
    )
    return fig

# ----------------- PAGE 4 CHARTS -----------------

def create_treemap_sales_experience(treemap_df):
    """Page 4 Visual 1: Treemap Product Sales vs Customer Experience"""
    fig = px.treemap(
        treemap_df,
        path=['category_clean'],
        values='product_sales',
        color='avg_review_score',
        color_continuous_scale="RdYlGn",
        range_color=[3.5, 4.5],
        hover_data=['products_sold']
    )
    
    fig.update_traces(
        textinfo="label+value",
        hovertemplate="<b>%{label}</b><br>Sales: R$ %{value:,.2f}<br>Avg Rating: %{color:.2f}<extra></extra>"
    )
    
    fig.update_layout(
        height=380,
        margin=dict(l=5, r=5, t=10, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title="Avg Review",
            thickness=10,
            len=0.7,
            tickfont=dict(color="#94A3B8", size=9)
        )
    )
    return fig

def create_ratings_delay_combo(bucket_df):
    """
    Page 4 HERO VISUAL: Ratings Collapse Once a Parcel is Late
    Bars: Average Review Score
    Line: Low Rating %
    """
    fig = go.Figure()
    
    # Bars for Avg Score
    fig.add_trace(go.Bar(
        x=bucket_df['delay_bucket'],
        y=bucket_df['avg_score'],
        name="Avg Review Score",
        marker=dict(
            color=[COLOR_EMERALD, COLOR_CYAN, COLOR_AMBER, COLOR_ROSE],
            cornerradius=4
        ),
        text=[f"{s:.2f}" for s in bucket_df['avg_score']],
        textposition="outside",
        textfont=dict(color="#CBD5E1", size=11, family=FONT_FAMILY),
        yaxis="y1",
        hovertemplate="<b>%{x}</b><br>Avg Score: %{y:.2f}<extra></extra>"
    ))
    
    # Line for Low Rating %
    fig.add_trace(go.Scatter(
        x=bucket_df['delay_bucket'],
        y=bucket_df['low_rating_pct'],
        name="Low Rating % (1-2 Stars)",
        mode="lines+markers",
        line=dict(color="#F43F5E", width=3, dash="dot"),
        marker=dict(size=8, color="#F43F5E"),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Low Rating Rate: %{y:.1f}%<extra></extra>"
    ))
    
    fig.update_layout(
        yaxis=dict(
            title="Average Review Score (1-5)",
            range=[0, 5.2],
            showgrid=True
        ),
        yaxis2=dict(
            title="Low Rating %",
            range=[0, 100],
            overlaying="y",
            side="right",
            ticksuffix="%",
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
            font=dict(color="#CBD5E1", size=10)
        )
    )
    return apply_chart_theme(fig, height=360, show_legend=True)

def create_reviews_and_late_combo(time_df):
    """
    Page 4 Visual 4: Late Deliveries & Customer Reviews Over Time
    Bars: Late Delivery %
    Line: Average Review Score
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=time_df['year_month'],
        y=time_df['late_pct'],
        name="Late Delivery %",
        marker=dict(color=COLOR_INDIGO, opacity=0.8, cornerradius=3),
        yaxis="y1",
        hovertemplate="<b>%{x}</b><br>Late Orders: %{y:.1f}%<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=time_df['year_month'],
        y=time_df['avg_review_score'],
        name="Avg Review Score",
        mode="lines+markers",
        line=dict(color=COLOR_CYAN, width=2.5),
        marker=dict(size=5, color=COLOR_CYAN),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Avg Score: %{y:.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        yaxis=dict(
            title="Late Delivery %",
            ticksuffix="%",
            showgrid=True
        ),
        yaxis2=dict(
            title="Avg Review Score",
            range=[3.0, 5.0],
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
            font=dict(color="#CBD5E1", size=10)
        )
    )
    return apply_chart_theme(fig, height=360, show_legend=True)
