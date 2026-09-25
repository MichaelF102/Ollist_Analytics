import streamlit as st

def render_insight_card(insight_dict, card_type="default"):
    """
    Renders the 4-layer insight card:
    1. Visual Title & Tag
    2. Key Finding
    3. Evidence
    4. Interpretation + Business Implication
    """
    if not insight_dict:
        return
        
    title = insight_dict.get('title', 'Analytical Insight')
    finding = insight_dict.get('finding', '')
    evidence = insight_dict.get('evidence', '')
    interpretation = insight_dict.get('interpretation', '')
    implication = insight_dict.get('business_implication', '')
    
    cls_type = ""
    if card_type == "alert":
        cls_type = "alert"
    elif card_type == "success":
        cls_type = "success"
    elif card_type == "warning":
        cls_type = "warning"
        
    card_html = f"""
    <div class="insight-card-wrapper {cls_type}">
        <div class="insight-header">
            <span class="insight-tag">
                <span>💡</span> {title}
            </span>
            <span style="font-size: 0.7rem; color: #64748b; font-weight: 500;">AUTOMATED INSIGHT</span>
        </div>
        <div class="insight-finding">
            {finding}
        </div>
        <div class="insight-evidence">
            <strong style="color: #38bdf8;">DATA EVIDENCE:</strong> {evidence}
        </div>
        <div class="insight-grid">
            <div>
                <div class="insight-block-label">🧠 Business Interpretation</div>
                <div class="insight-block-content">{interpretation}</div>
            </div>
            <div>
                <div class="insight-block-label">⚡ Operational Implication</div>
                <div class="insight-block-content">{implication}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_summary_banner(title, text, icon="📊", variant="default"):
    """Renders a prominent top callout banner."""
    color_map = {
        "default": ("rgba(99, 102, 241, 0.12)", "rgba(99, 102, 241, 0.3)", "#a5b4fc"),
        "alert": ("rgba(244, 63, 94, 0.12)", "rgba(244, 63, 94, 0.3)", "#fda4af"),
        "success": ("rgba(16, 185, 129, 0.12)", "rgba(16, 185, 129, 0.3)", "#6ee7b7"),
        "amber": ("rgba(245, 158, 11, 0.12)", "rgba(245, 158, 11, 0.3)", "#fcd34d")
    }
    bg, border, text_color = color_map.get(variant, color_map["default"])
    
    html = f"""
    <div class="summary-banner" style="background: {bg}; border-color: {border};">
        <div class="summary-banner-title" style="color: {text_color};">
            <span>{icon}</span> {title}
        </div>
        <div class="summary-banner-body">
            {text}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
