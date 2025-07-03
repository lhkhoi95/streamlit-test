import streamlit as st

def get_status_color(color):
    """Helper function to get the appropriate color for status badges"""
    colors = {
        "green": "#22c55e",
        "red": "#ef4444", 
        "orange": "#f97316",
        "blue": "#3b82f6",
        "purple": "#8b5cf6",
        "yellow": "#ECC244"
    }
    return colors.get(color, "#22c55e")

def get_text_color(bg_color):
    """Calculate if text should be white or dark based on background color brightness"""
    # Remove # from hex color
    hex_color = bg_color.lstrip('#')
    
    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Calculate luminance using relative luminance formula
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # Return white for dark backgrounds, dark for light backgrounds
    return "#ffffff" if luminance < 0.5 else "#1f2937"

def performance_card(title, score, subtitle, status_text, status_color, ranking_text):
    """
    Create a custom performance card component
    
    Args:
        title: Main title of the card
        score: Large score number (e.g., "0.92")
        subtitle: Subtitle below the score (e.g., "Performance Score")
        status_text: Status badge text (e.g., "Meets Expectations")
        status_color: Color for the status badge ("green", "red", "orange", etc.)
        ranking_text: Additional ranking information
    """
    stat_color = get_status_color(status_color)
    text_color = get_text_color(stat_color)
    
    # Generate a unique class name to avoid CSS conflicts
    import random
    card_id = f"card-{random.randint(1000, 9999)}"
    
    # Custom CSS for the card
    card_css = f"""
    <style>
    .performance-card-{card_id} {{
        background: #374151;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 4px 6px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #3b82f6;
        margin: 8px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    .performance-card-{card_id} .card-title {{
        font-size: 16px;
        font-weight: 600;
        color: #f9fafb;
        margin-bottom: 16px;
        line-height: 1.3;
    }}
    
    .performance-card-{card_id} .card-score {{
        font-size: 48px;
        font-weight: 800;
        color: #ef4444;
        margin: 8px 0;
        line-height: 1;
        letter-spacing: -0.02em;
    }}
    
    .performance-card-{card_id} .card-subtitle {{
        font-size: 14px;
        color: #d1d5db;
        margin-bottom: 16px;
        font-weight: 500;
    }}
    
    .performance-card-{card_id} .status-badge {{
        background-color: {stat_color} !important;
        color: {text_color};
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin: 12px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        width: fit-content;
    }}
    
    .performance-card-{card_id} .ranking-text {{
        font-size: 13px;
        color: #d1d5db;
        margin-top: auto;
        line-height: 1.4;
    }}
    </style>
    """
   
    
    # HTML structure for the card
    card_html = f"""
    {card_css}
    <div class="performance-card-{card_id}">
        <div>
            <div class="card-title">{title}</div>
            <div class="card-score">{score}</div>
            <div class="card-subtitle">{subtitle}</div>
            <div class="status-badge">{status_text}</div>
        </div>
        <div class="ranking-text">{ranking_text}</div>
    </div>
    """
    
    # Render the card
    st.markdown(card_html, unsafe_allow_html=True)
