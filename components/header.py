import streamlit as st

def render_header(page_title, page_subtitle, active_filters=None):
    """
    Renders a unified top header with breadcrumb, live status, and active filter pills.
    """
    filters_html = ""
    if active_filters:
        pills = []
        for k, v in active_filters.items():
            if v and v != 'All':
                if isinstance(v, list) and len(v) > 0:
                    val_str = f"{k.title()}: {', '.join(map(str, v[:2]))}"
                    if len(v) > 2:
                        val_str += f" (+{len(v)-2})"
                    pills.append(f"<span class='bi-pill-badge bi-pill-active-filter'>{val_str}</span>")
                elif not isinstance(v, list):
                    pills.append(f"<span class='bi-pill-badge bi-pill-active-filter'>{k.title()}: {v}</span>")
        if pills:
            filters_html = "<div style='margin-top: 0.6rem; display: flex; flex-wrap: wrap; align-items: center;'><span style='font-size: 0.72rem; color: #64748b; margin-right: 0.5rem; text-transform: uppercase; font-weight: 600;'>Active Filters:</span>" + "".join(pills) + "</div>"

    header_html = f"""
    <div class="bi-header-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <div style="font-size: 0.75rem; color: #818cf8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; margin-bottom: 0.2rem;">
                    Olist Brazilian E-Commerce &bull; Business Intelligence Platform
                </div>
                <h1 class="bi-header-title">{page_title}</h1>
                <div class="bi-header-subtitle">{page_subtitle}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.25rem;">
                <span class="bi-pill-badge bi-pill-live">
                    <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #34d399; margin-right: 5px; animation: pulse 2s infinite;"></span>
                    Live Data Model
                </span>
            </div>
        </div>
        {filters_html}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
