import math

def format_number(val, decimals=1):
    """Formats large numbers into K, M, B representation."""
    if val is None or math.isnan(val):
        return "N/A"
    abs_val = abs(val)
    if abs_val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.{decimals}f}B"
    elif abs_val >= 1_000_000:
        return f"{val / 1_000_000:.{decimals}f}M"
    elif abs_val >= 1_000:
        return f"{val / 1_000:.{decimals}f}K"
    else:
        return f"{val:,.0f}" if isinstance(val, int) or val.is_integer() else f"{val:.{decimals}f}"

def format_currency(val, currency="R$", decimals=2):
    """Formats monetary figures with currency prefix and compact notation if large."""
    if val is None or math.isnan(val):
        return "N/A"
    abs_val = abs(val)
    if abs_val >= 1_000_000:
        return f"{currency} {val / 1_000_000:.2f}M"
    elif abs_val >= 10_000:
        return f"{currency} {val / 1_000:.1f}K"
    else:
        return f"{currency} {val:,.2f}"

def format_exact_currency(val, currency="R$"):
    """Formats exact monetary values with thousand separators."""
    if val is None or math.isnan(val):
        return "N/A"
    return f"{currency} {val:,.2f}"

def format_percent(val, decimals=1, is_ratio=True):
    """Formats percentages. If is_ratio is True, 0.068 -> 6.8%."""
    if val is None or math.isnan(val):
        return "N/A"
    num = val * 100 if is_ratio else val
    return f"{num:.{decimals}f}%"

def format_days(val, decimals=2):
    """Formats duration in days."""
    if val is None or math.isnan(val):
        return "N/A"
    return f"{val:.{decimals}f} days"

def format_rating(val, decimals=2):
    """Formats rating scores."""
    if val is None or math.isnan(val):
        return "N/A"
    return f"{val:.{decimals}f}"
