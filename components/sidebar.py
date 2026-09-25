import streamlit as st

def render_sidebar(orders_df, items_df):
    """
    Renders the unified global sidebar with platform branding, navigation info,
    global filters, and a reset button.
    Stores filter state in st.session_state so filters persist across pages.
    """
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-title">
                <span style="font-size: 1.4rem;">⚡</span> OLIST ANALYTICS
            </div>
            <div class="sidebar-sub">Executive Decision Support</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.75rem;'>Global Filters</h4>", unsafe_allow_html=True)
        
        # Initialize default filter state if not present
        if 'filters' not in st.session_state:
            st.session_state['filters'] = {
                'year': 'All',
                'quarter': 'All',
                'region': 'All',
                'state': 'All',
                'category': 'All',
                'status': 'All'
            }
            
        current_filters = st.session_state['filters']
        
        # 1. Year Filter
        available_years = ['All'] + sorted([int(y) for y in orders_df['year'].dropna().unique()])
        default_year_idx = available_years.index(current_filters.get('year', 'All')) if current_filters.get('year') in available_years else 0
        selected_year = st.selectbox("Order Year", available_years, index=default_year_idx, key="sb_year")
        
        # 2. Quarter Filter
        quarters = ['All', 'Q1', 'Q2', 'Q3', 'Q4']
        default_q_idx = quarters.index(current_filters.get('quarter', 'All')) if current_filters.get('quarter') in quarters else 0
        selected_quarter = st.selectbox("Quarter", quarters, index=default_q_idx, key="sb_quarter")
        
        # 3. Customer Region Filter
        regions = ['All', 'Central-West', 'North', 'Northeast', 'South', 'Southeast']
        default_reg_idx = regions.index(current_filters.get('region', 'All')) if current_filters.get('region') in regions else 0
        selected_region = st.selectbox("Customer Region", regions, index=default_reg_idx, key="sb_region")
        
        # 4. Customer State Filter
        all_states = sorted(orders_df['customer_state'].dropna().unique().tolist())
        selected_state = st.selectbox("Customer State", ['All'] + all_states, index=0 if current_filters.get('state') == 'All' else (all_states.index(current_filters.get('state')) + 1 if current_filters.get('state') in all_states else 0), key="sb_state")
        
        # 5. Product Category Filter
        top_cats = sorted(items_df['category_clean'].dropna().unique().tolist())
        selected_category = st.selectbox("Product Category", ['All'] + top_cats, index=0 if current_filters.get('category') == 'All' else (top_cats.index(current_filters.get('category')) + 1 if current_filters.get('category') in top_cats else 0), key="sb_cat")
        
        # 6. Order Status Filter
        statuses = ['All'] + sorted(orders_df['order_status'].dropna().unique().tolist())
        selected_status = st.selectbox("Order Status", statuses, index=0 if current_filters.get('status') == 'All' else (statuses.index(current_filters.get('status')) + 1 if current_filters.get('status') in statuses else 0), key="sb_status")
        
        # Update session state filters
        st.session_state['filters'] = {
            'year': selected_year,
            'quarter': selected_quarter,
            'region': selected_region,
            'state': selected_state,
            'category': selected_category,
            'status': selected_status
        }
        
        # Reset button
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("↺ Reset All Filters", use_container_width=True):
            st.session_state['filters'] = {
                'year': 'All',
                'quarter': 'All',
                'region': 'All',
                'state': 'All',
                'category': 'All',
                'status': 'All'
            }
            st.rerun()
            
        st.markdown("""
        <div style="margin-top: 1.5rem; padding: 0.85rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px;">
            <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Dataset Scope</div>
            <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 0.25rem;">
                99,441 Orders &bull; 112,650 Items<br>
                2016-09 to 2018-10
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    return st.session_state['filters']
