import streamlit as st

def render_kpi_cards(kpis):
    """
    Renders a row of modern, responsive KPI cards.
    kpis is a list of dicts:
    [
        {
            'label': 'Total Orders',
            'value': '99K',
            'sub': 'All sales channels',
            'color': '#6366F1'  # Indigo
        },
        ...
    ]
    """
    cols = st.columns(len(kpis))
    
    for idx, (col, kpi) in enumerate(zip(cols, kpis)):
        color = kpi.get('color', '#6366F1')
        label = kpi.get('label', '')
        value = kpi.get('value', '0')
        sub = kpi.get('sub', '')
        icon = kpi.get('icon', '')
        
        card_html = f"""
        <div class="kpi-card">
            <div>
                <div class="kpi-card-label">
                    <span>{label}</span>
                    <span>{icon}</span>
                </div>
                <div class="kpi-card-value" style="color: #ffffff;">{value}</div>
            </div>
            <div class="kpi-card-sub">
                <span>{sub}</span>
            </div>
            <div class="kpi-indicator-bar" style="background: {color};"></div>
        </div>
        """
        col.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 1.25rem;'></div>", unsafe_allow_html=True)

def render_metric_strip(metrics):
    """
    Renders a compact horizontal metric strip for charts.
    metrics is a list of dicts:
    [
        {'label': 'Peak Orders', 'value': '7.3K', 'sub': 'Nov 2017', 'color': '#38BDF8'},
        ...
    ]
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        color = m.get('color', '#6366F1')
        label = m.get('label', '')
        val = m.get('value', '')
        sub = m.get('sub', '')
        sub_html = f'<div style="font-size: 0.7rem; color: {color}; margin-top: 0.1rem; font-weight: 500;">{sub}</div>' if sub else ''
        html = f"""
        <div style="background: rgba(255, 255, 255, 0.025); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 8px; padding: 0.5rem 0.75rem; margin-bottom: 0.6rem;">
            <div style="font-size: 0.68rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin-top: 0.15rem; letter-spacing: -0.02em;">{val}</div>
            {sub_html}
        </div>
        """
        col.markdown(html, unsafe_allow_html=True)

