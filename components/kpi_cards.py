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
