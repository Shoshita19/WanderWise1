import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import math
from datetime import datetime

# ReportLab imports for professional PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ==========================================
# 1. STREAMLIT APP CONFIGURATION & CSS
# ==========================================
st.set_page_config(
    page_title="WanderWise – Smart India Travel Planner",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    /* Global Typography & Palette */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Header & Tagline Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0e7490 0%, #0369a1 50%, #0f172a 100%);
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(14, 116, 144, 0.25);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.35rem;
        color: #ffffff;
    }
    .hero-tagline {
        font-size: 1.15rem;
        color: #e0f2fe;
        font-weight: 500;
        margin-bottom: 0.75rem;
    }
    .hero-badges {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-top: 0.8rem;
    }
    .hero-pill {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    /* Step progress bar */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 0.85rem 1.25rem;
        overflow-x: auto;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.86rem;
        font-weight: 600;
        color: #64748b;
        white-space: nowrap;
    }
    .step-item.active {
        color: #0e7490;
    }
    .step-item.completed {
        color: #059669;
    }
    .step-num {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        background: #e2e8f0;
        color: #475569;
    }
    .step-item.active .step-num {
        background: #0e7490;
        color: white;
    }
    .step-item.completed .step-num {
        background: #059669;
        color: white;
    }
    
    /* Destination Cards */
    .dest-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .dest-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }
    .dest-card-header {
        padding: 1.25rem 1.4rem;
        border-bottom: 1px solid #f1f5f9;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .dest-card-body {
        padding: 1.25rem 1.4rem;
    }
    .match-badge {
        background: #dcfce7;
        color: #166534;
        font-weight: 700;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        border: 1px solid #bbf7d0;
    }
    
    /* Budget Status Pill */
    .status-pill-within {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
        padding: 0.45rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }
    .status-pill-slightly-over {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
        padding: 0.45rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }
    .status-pill-over {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
        padding: 0.45rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }
    
    /* Summary Metric Cards */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0f172a;
    }
    
    /* Itinerary Timeline Cards */
    .day-box {
        background: #ffffff;
        border-left: 4px solid #0e7490;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 0 12px 12px 0;
        padding: 1.25rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .day-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0e7490;
        margin-bottom: 0.6rem;
        display: flex;
        justify-content: space-between;
    }
    
    /* Print media query */
    @media print {
        .stButton, .stDownloadButton, .step-indicator, .stSidebar, header, footer {
            display: none !important;
        }
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# 2. DATA LOADING & HELPERS
# ==========================================
@st.cache_data
def load_destinations():
    # Attempt loading from local or relative paths
    search_paths = [
        "destinations.csv",
        "data/destinations.csv",
        "modules/data/destinations.csv",
        os.path.join(os.path.dirname(__file__), "destinations.csv")
    ]
    for path in search_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                return df
            except Exception as e:
                continue
    # Fallback minimal dataset if file is absent
    st.error("destinations.csv not found. Please ensure destinations.csv is in the project folder.")
    return pd.DataFrame()


def format_inr(amount):
    """Format number into Indian Rupee string: e.g. ₹ 24,500"""
    try:
        val = int(round(amount))
        # Format in Indian grouping style if needed or standard comma
        s = f"{val:,}"
        return f"₹{s}"
    except:
        return f"₹{amount}"


# Initialize session state variables
if "step" not in st.session_state:
    st.session_state.step = 1

if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {
        "budget": 25000,
        "duration": 4,
        "interests": ["Mountains", "Nature"],
        "starting_city": "Delhi",
        "travellers": 2
    }

if "selected_destination" not in st.session_state:
    st.session_state.selected_destination = None

if "cost_breakdown" not in st.session_state:
    st.session_state.cost_breakdown = None


# ==========================================
# 3. RECOMMENDATION ENGINE (STEP 2)
# ==========================================
def score_destinations(df, user_prefs):
    """
    Ranks Indian destinations based on:
    - User travel interests overlap (up to 50 pts)
    - Budget feasibility for group & duration (up to 35 pts)
    - Duration suitability match (up to 15 pts)
    """
    if df.empty:
        return []

    user_interests = set(user_prefs["interests"])
    budget = user_prefs["budget"]
    duration = user_prefs["duration"]
    travellers = user_prefs["travellers"]

    scored_list = []

    for _, row in df.iterrows():
        # Parse interests
        dest_interests = [i.strip() for i in str(row.get("interests", "")).split(",")]
        matching_interests = user_interests.intersection(set(dest_interests))

        # Interest Score (0 to 50)
        if len(user_interests) > 0:
            interest_ratio = len(matching_interests) / len(user_interests)
            interest_score = interest_ratio * 50
        else:
            interest_score = 30
            matching_interests = set(dest_interests[:2])

        # Estimated total base trip cost for group
        daily_cost = float(row.get("estimated_daily_cost", 2000))
        transport_base = float(row.get("transport_cost", 1500))
        estimated_trip_total = (daily_cost * duration * travellers) + (transport_base * travellers)

        # Budget Feasibility Score (0 to 35)
        if budget >= estimated_trip_total:
            budget_score = 35
        elif budget >= estimated_trip_total * 0.85:
            budget_score = 25
        elif budget >= estimated_trip_total * 0.70:
            budget_score = 15
        else:
            budget_score = 5

        # Duration Match Score (0 to 15)
        suggested_days = float(row.get("suggested_days", 4))
        day_diff = abs(duration - suggested_days)
        duration_score = max(0, 15 - (day_diff * 3))

        # Total Match Score
        total_score = min(98, max(58, int(round(interest_score + budget_score + duration_score))))

        # Explanation for recommendation
        if matching_interests:
            why_recommended = f"Matches your chosen interests in **{', '.join(matching_interests)}**."
        else:
            why_recommended = f"Offers prominent scenic highlights in {row.get('state', 'India')}."

        scored_list.append({
            "data": row.to_dict(),
            "score": total_score,
            "estimated_trip_total": estimated_trip_total,
            "matching_interests": list(matching_interests),
            "why_recommended": why_recommended
        })

    # Sort descending by match score
    scored_list.sort(key=lambda x: x["score"], reverse=True)
    return scored_list[:3]  # Return top 3


# ==========================================
# 4. COST ESTIMATION ENGINE (STEP 3)
# ==========================================
def calculate_trip_costs(dest_dict, user_prefs):
    """
    Breaks down expenses into 6 realistic categories:
    1. Intercity Transportation
    2. Accommodation
    3. Food & Beverages
    4. Local Transportation
    5. Sightseeing & Activities
    6. Miscellaneous & Contingency
    """
    duration = user_prefs["duration"]
    travellers = user_prefs["travellers"]
    budget = user_prefs["budget"]

    # Destination specific rates
    trans_base = float(dest_dict.get("transport_cost", 1500))
    hotel_base = float(dest_dict.get("accommodation_cost", 1500))
    food_base = float(dest_dict.get("food_cost", 600))
    local_base = float(dest_dict.get("local_transport_cost", 500))
    sight_base = float(dest_dict.get("sightseeing_cost", 400))

    # Calculate itemized costs
    # Rooms required: 1 room for 1-2 people, 2 rooms for 3-4, etc.
    rooms_needed = math.ceil(travellers / 2)
    nights = max(1, duration - 1)

    transport_total = trans_base * travellers
    accommodation_total = hotel_base * nights * rooms_needed
    food_total = food_base * duration * travellers
    local_transport_total = local_base * duration
    sightseeing_total = sight_base * duration * travellers

    subtotal = (
        transport_total
        + accommodation_total
        + food_total
        + local_transport_total
        + sightseeing_total
    )

    # Miscellaneous / Contingency: ~7% of subtotal
    misc_total = int(round(subtotal * 0.07))
    total_estimated_cost = int(round(subtotal + misc_total))

    per_person_cost = int(round(total_estimated_cost / travellers))
    daily_average_expense = int(round(total_estimated_cost / duration))
    remaining_budget = budget - total_estimated_cost

    # Budget Status Classification
    if total_estimated_cost <= budget:
        budget_status = "Within Budget"
        status_code = "within"
        status_message = "Great news! Your estimated trip cost is within your total budget."
    elif total_estimated_cost <= (budget * 1.15):
        budget_status = "Slightly Over Budget"
        status_code = "slightly_over"
        over_by = total_estimated_cost - budget
        status_message = f"Notice: Estimated cost exceeds your budget slightly by {format_inr(over_by)}. You can easily trim local shopping or dining."
    else:
        budget_status = "Over Budget"
        status_code = "over"
        over_by = total_estimated_cost - budget
        status_message = f"Alert: Estimated expenses exceed your budget by {format_inr(over_by)}. Consider adjusting trip duration or group budget."

    return {
        "transportation": int(round(transport_total)),
        "accommodation": int(round(accommodation_total)),
        "food": int(round(food_total)),
        "local_transport": int(round(local_transport_total)),
        "sightseeing": int(round(sightseeing_total)),
        "miscellaneous": misc_total,
        "total_estimated_cost": total_estimated_cost,
        "per_person_cost": per_person_cost,
        "daily_average_expense": daily_average_expense,
        "remaining_budget": remaining_budget,
        "budget_status": budget_status,
        "status_code": status_code,
        "status_message": status_message,
        "rooms_needed": rooms_needed,
        "nights": nights
    }


# ==========================================
# 5. ITINERARY GENERATOR (STEP 4)
# ==========================================
def parse_attractions(attractions_str):
    """Parse pipe-separated attractions from destinations.csv"""
    results = []
    if not attractions_str or pd.isna(attractions_str):
        return results
    raw_list = str(attractions_str).split(";")
    for item in raw_list:
        parts = [p.strip() for p in item.split("|")]
        if len(parts) >= 5:
            results.append({
                "name": parts[0],
                "category": parts[1],
                "fee": parts[2],
                "hours": parts[3],
                "description": parts[4]
            })
        elif len(parts) >= 2:
            results.append({
                "name": parts[0],
                "category": parts[1] if len(parts) > 1 else "Sightseeing",
                "fee": "Free / Nominal",
                "hours": "Daytime",
                "description": parts[2] if len(parts) > 2 else "Iconic local attraction."
            })
    return results


def parse_hotels(hotels_str):
    """Parse pipe-separated hotels from destinations.csv"""
    results = []
    if not hotels_str or pd.isna(hotels_str):
        return results
    raw_list = str(hotels_str).split(";")
    for item in raw_list:
        parts = [p.strip() for p in item.split("|")]
        if len(parts) >= 5:
            results.append({
                "name": parts[0],
                "location": parts[1],
                "price": parts[2],
                "type": parts[3],
                "link": parts[4]
            })
    return results


def parse_travel_tips(tips_str):
    """Parse pipe-separated travel tips"""
    results = {}
    if not tips_str or pd.isna(tips_str):
        return results
    parts = str(tips_str).split("|")
    for p in parts:
        if ":" in p:
            k, v = p.split(":", 1)
            results[k.strip()] = v.strip()
    return results


def generate_daywise_itinerary(dest_dict, duration, daily_cost):
    """
    Automatically creates a realistic, day-wise schedule
    integrating verified attractions and practical pacing.
    """
    attractions = parse_attractions(dest_dict.get("attractions", ""))
    num_attractions = len(attractions)

    itinerary = []
    for day_num in range(1, duration + 1):
        if day_num == 1:
            title = "Day 1: Arrival, Check-in & Scenic Welcome"
            morning = f"Arrive in {dest_dict['destination']}, transfer to hotel, check-in, and relax after transit."
            if num_attractions > 0:
                first_attraction = attractions[0]
                afternoon = f"Savor authentic local lunch; leisurely walk around the town center or visit {first_attraction['name']}."
            else:
                afternoon = "Savor traditional lunch and take a gentle stroll around the local neighborhood."
            evening = "Enjoy the evening sunset, explore vibrant local handicrafts bazaars, and dine at a top-rated local restaurant."
            places = [attractions[0]["name"]] if num_attractions > 0 else ["Town Center", "Local Bazaars"]

        elif day_num == duration and duration > 1:
            title = f"Day {day_num}: Cultural Souvenirs, Farewell & Departure"
            morning = "Relish a relaxed breakfast, pack up, and visit a heritage viewpoint or pick up famous local delicacies."
            afternoon = "Enjoy a farewell lunch, check-out from your accommodation, and transfer to airport/railway station."
            evening = "Departure with cherished memories of your Indian journey."
            places = ["Local Artisan Market", "Scenic Farewell Point"]

        else:
            # Middle days: rotate through attractions
            att_idx = ((day_num - 2) * 2 + 1) % max(1, num_attractions)
            att_next = (att_idx + 1) % max(1, num_attractions)

            att1 = attractions[att_idx] if num_attractions > att_idx else None
            att2 = attractions[att_next] if num_attractions > att_next else None

            title = f"Day {day_num}: Adventure, Heritage & Local Wonders"
            if att1:
                morning = f"Morning excursion to **{att1['name']}** ({att1['category']}). {att1['description']}"
            else:
                morning = f"Explore scenic natural surroundings and picturesque mountain/coastal walking trails."

            if att2:
                afternoon = f"After a local meal, head to **{att2['name']}** ({att2['category']}). {att2['description']}"
            else:
                afternoon = "Visit historical architecture, regional craft centers, and tranquil scenic gardens."

            evening = "Unwind with regional street food, sunset photography, and cultural music or cafe time."
            places = [a["name"] for a in [att1, att2] if a]

        itinerary.append({
            "day": day_num,
            "title": title,
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening,
            "places": places,
            "est_daily_cost": daily_cost
        })

    return itinerary


# ==========================================
# 6. REPORTLAB PDF GENERATOR (STEP 7)
# ==========================================
class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages for dynamic 'Page X of Y' footers"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        # Running Header on page 2+
        if self._pageNumber > 1:
            self.drawString(40, 802, "WanderWise – Smart India Travel Planner")
            self.drawRightString(555, 802, "Personalized Travel Plan")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 794, 555, 794)
        # Running Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_text)
        self.drawString(40, 30, "Generated by WanderWise | Explore India. Your Budget. Your Journey.")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 42, 555, 42)
        self.restoreState()


def generate_pdf_report(dest_dict, user_prefs, costs, itinerary):
    """
    Builds a professional, clean multi-page travel report.
    STRICTLY NO CHARTS OR GRAPHS.
    Uses Indian Rupee format 'Rs. XX,XXX'.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=45,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0E7490"),
        spaceAfter=4
    )
    tagline_style = ParagraphStyle(
        'Tagline',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )
    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    story = []

    # 1. Header Banner & Title
    story.append(Paragraph("WanderWise – Smart India Travel Planner", title_style))
    story.append(Paragraph("Explore India. Your Budget. Your Journey. | Official Personalized Plan", tagline_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0E7490"), spaceAfter=10))

    # 2. Trip Overview & Preferences Table
    story.append(Paragraph("1. Traveler Profile & Preferences", section_heading))
    prefs_data = [
        [
            Paragraph("<b>Destination:</b>", body_style),
            Paragraph(f"{dest_dict['destination']}, {dest_dict['state']}", body_bold),
            Paragraph("<b>Total Budget:</b>", body_style),
            Paragraph(f"Rs. {user_prefs['budget']:,}", body_bold)
        ],
        [
            Paragraph("<b>Trip Duration:</b>", body_style),
            Paragraph(f"{user_prefs['duration']} Days ({costs['nights']} Nights)", body_style),
            Paragraph("<b>No. of Travelers:</b>", body_style),
            Paragraph(f"{user_prefs['travellers']} Person(s)", body_style)
        ],
        [
            Paragraph("<b>Travel Interests:</b>", body_style),
            Paragraph(", ".join(user_prefs['interests']), body_style),
            Paragraph("<b>Starting Location:</b>", body_style),
            Paragraph(user_prefs.get('starting_city', 'India'), body_style)
        ],
        [
            Paragraph("<b>Best Time to Visit:</b>", body_style),
            Paragraph(dest_dict.get('best_time', 'Pleasant season'), body_style),
            Paragraph("<b>Generated Date:</b>", body_style),
            Paragraph(datetime.now().strftime("%d %b %Y"), body_style)
        ]
    ]
    t_prefs = Table(prefs_data, colWidths=[110, 160, 110, 140])
    t_prefs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_prefs)
    story.append(Spacer(1, 10))

    # 3. Destination Overview
    story.append(Paragraph("2. Selected Destination Overview", section_heading))
    story.append(Paragraph(f"<b>About {dest_dict['destination']}:</b> {dest_dict['description']}", body_style))
    story.append(Spacer(1, 10))

    # 4. Cost Breakdown Table
    story.append(Paragraph("3. Detailed Trip Cost Estimation & Budget Analysis", section_heading))
    cost_data = [
        [
            Paragraph("Expense Category", table_cell_bold),
            Paragraph("Calculation Basis", table_cell_bold),
            Paragraph("Estimated Total (Rs.)", table_cell_bold),
            Paragraph("Per Person (Rs.)", table_cell_bold),
            Paragraph("Share (%)", table_cell_bold)
        ]
    ]

    tot = max(1, costs['total_estimated_cost'])
    breakdowns = [
        ("Transportation (Intercity)", f"{user_prefs['travellers']} Travelers roundtrip", costs['transportation']),
        ("Accommodation", f"{costs['nights']} nights, {costs['rooms_needed']} room(s)", costs['accommodation']),
        ("Food & Dining", f"3 meals/day for {user_prefs['duration']} days", costs['food']),
        ("Local Transportation", f"Cabs / autos for {user_prefs['duration']} days", costs['local_transport']),
        ("Sightseeing & Activities", f"Entry fees and monument access", costs['sightseeing']),
        ("Miscellaneous / Contingency", "Emergency buffer (~7%)", costs['miscellaneous'])
    ]

    for cat, basis, amt in breakdowns:
        pct = f"{(amt / tot) * 100:.1f}%"
        pp = f"Rs. {int(round(amt / user_prefs['travellers'])):,}"
        cost_data.append([
            Paragraph(cat, table_cell),
            Paragraph(basis, table_cell),
            Paragraph(f"Rs. {amt:,}", table_cell),
            Paragraph(pp, table_cell),
            Paragraph(pct, table_cell)
        ])

    # Totals row
    cost_data.append([
        Paragraph("<b>Total Estimated Trip Cost</b>", table_cell_bold),
        Paragraph(f"<b>Budget Status: {costs['budget_status']}</b>", table_cell_bold),
        Paragraph(f"<b>Rs. {costs['total_estimated_cost']:,}</b>", table_cell_bold),
        Paragraph(f"<b>Rs. {costs['per_person_cost']:,}</b>", table_cell_bold),
        Paragraph("<b>100%</b>", table_cell_bold)
    ])

    t_costs = Table(cost_data, colWidths=[150, 140, 95, 85, 50])
    t_costs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0E7490")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_costs)

    budget_diff = costs['remaining_budget']
    if budget_diff >= 0:
        budget_note = f"<b>Budget Analysis:</b> Within Budget. Estimated remaining balance: <b>Rs. {budget_diff:,}</b>."
    else:
        budget_note = f"<b>Budget Analysis:</b> Exceeds designated budget by <b>Rs. {abs(budget_diff):,}</b>."
    story.append(Spacer(1, 4))
    story.append(Paragraph(budget_note, body_style))
    story.append(Spacer(1, 10))

    # 5. Day-by-Day Personalized Itinerary
    story.append(Paragraph("4. Personalized Day-Wise Itinerary", section_heading))
    itin_data = [
        [
            Paragraph("Day", table_cell_bold),
            Paragraph("Morning Activities", table_cell_bold),
            Paragraph("Afternoon Activities", table_cell_bold),
            Paragraph("Evening Activities", table_cell_bold)
        ]
    ]
    for d in itinerary:
        itin_data.append([
            Paragraph(f"<b>Day {d['day']}</b>", table_cell_bold),
            Paragraph(d['morning'], table_cell),
            Paragraph(d['afternoon'], table_cell),
            Paragraph(d['evening'], table_cell)
        ])

    t_itin = Table(itin_data, colWidths=[45, 160, 160, 155])
    t_itin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0369A1")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_itin)
    story.append(Spacer(1, 10))

    # 6. Recommended Hotels
    hotels = parse_hotels(dest_dict.get("hotels", ""))
    if hotels:
        story.append(Paragraph("5. Recommended Accommodations", section_heading))
        h_data = [
            [
                Paragraph("Hotel / Resort Name", table_cell_bold),
                Paragraph("Category", table_cell_bold),
                Paragraph("Location", table_cell_bold),
                Paragraph("Approx. Price / Night", table_cell_bold)
            ]
        ]
        for h in hotels:
            h_data.append([
                Paragraph(h['name'], table_cell),
                Paragraph(h['type'], table_cell),
                Paragraph(h['location'], table_cell),
                Paragraph(f"Rs. {h['price']}", table_cell)
            ])
        t_hotels = Table(h_data, colWidths=[180, 110, 130, 100])
        t_hotels.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_hotels)
        story.append(Spacer(1, 10))

    # 7. Travel Tips & Smart Packing
    tips = parse_travel_tips(dest_dict.get("travel_tips", ""))
    if tips:
        story.append(Paragraph("6. Destination Travel Tips & Guidelines", section_heading))
        for key, val in tips.items():
            story.append(Paragraph(f"• <b>{key}:</b> {val}", body_style))
        story.append(Spacer(1, 8))

    # 8. Disclaimer
    story.append(Paragraph("7. Important Travel Disclaimers", section_heading))
    disclaimer_text = (
        "All cost estimates, hotel rates, and attraction fees are realistic approximations compiled "
        "from verified Indian travel data. Live market rates may vary based on peak seasons, "
        "holidays, and booking timeframes. Please verify monument opening hours locally before visiting."
    )
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disc', parent=body_style, fontName='Helvetica-Oblique', fontSize=8)))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


# ==========================================
# 7. MAIN APPLICATION CONTROLLER
# ==========================================
def main():
    # Load dataset
    df = load_destinations()
    if df.empty:
        st.stop()

    # Hero Banner
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🧭 WanderWise</div>
        <div class="hero-tagline">Explore India. Your Budget. Your Journey.</div>
        <div style="font-size: 0.95rem; opacity: 0.9; max-width: 800px;">
            Intelligent, India-only travel planner providing curated destination recommendations,
            realistic cost breakdowns, personalized day-wise itineraries, verified hotels, and downloadable PDF reports.
        </div>
        <div class="hero-badges">
            <span class="hero-pill">🇮🇳 100% Authentic India Destinations</span>
            <span class="hero-pill">💰 Realistic Cost Estimator</span>
            <span class="hero-pill">📅 Dynamic Day-Wise Itineraries</span>
            <span class="hero-pill">📄 Instant PDF Report Download</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Navigation & Quick Info
    with st.sidebar:
        st.header("🧭 WanderWise Nav")
        st.caption("Plan your journey in simple steps")

        step_names = [
            "1. Travel Preferences",
            "2. Destination Picks",
            "3. Cost & Budget",
            "4. Day-Wise Itinerary",
            "5. Hotels & Attractions",
            "6. Travel Dashboard",
            "7. PDF Report & Print"
        ]

        curr_step = st.session_state.step
        for idx, sname in enumerate(step_names, start=1):
            if idx == curr_step:
                st.markdown(f"**👉 <span style='color:#0e7490;'>{sname} (Current)</span>**", unsafe_allow_html=True)
            elif idx < curr_step:
                if st.button(f"✓ {sname}", key=f"nav_{idx}", use_container_width=True):
                    st.session_state.step = idx
                    st.rerun()
            else:
                st.caption(f"⚪ {sname}")

        st.divider()

        # Selected Destination Quick Glance in Sidebar
        if st.session_state.selected_destination:
            dest = st.session_state.selected_destination
            st.subheader("Selected Journey")
            st.write(f"📍 **{dest['destination']}**, {dest['state']}")
            st.write(f"⏱️ **{st.session_state.user_preferences['duration']} Days** | 👥 **{st.session_state.user_preferences['travellers']} Person(s)**")
            st.write(f"💰 **Budget:** {format_inr(st.session_state.user_preferences['budget'])}")

        st.divider()
        if st.button("🔄 Reset & Plan New Trip", use_container_width=True):
            st.session_state.step = 1
            st.session_state.selected_destination = None
            st.session_state.cost_breakdown = None
            st.rerun()

    # Step Progress Stepper Bar
    step_items_html = []
    step_labels = ["Preferences", "Recommendations", "Cost Estimation", "Itinerary", "Hotels & Tips", "Dashboard", "PDF Report"]
    for i, lbl in enumerate(step_labels, 1):
        if i == st.session_state.step:
            cls = "active"
        elif i < st.session_state.step:
            cls = "completed"
        else:
            cls = ""
        step_items_html.append(f'<div class="step-item {cls}"><span class="step-num">{i}</span><span>{lbl}</span></div>')

    st.markdown(f'<div class="step-indicator">{"".join(step_items_html)}</div>', unsafe_allow_html=True)


    # ==========================================
    # STEP 1: USER PREFERENCES
    # ==========================================
    if st.session_state.step == 1:
        st.subheader("Step 1: Your Travel Preferences")
        st.write("Tell us your budget and travel style. WanderWise will match you with the finest destinations in India.")

        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            budget = st.number_input(
                "Total Travel Budget for the Trip (₹ INR)",
                min_value=5000,
                max_value=500000,
                value=int(st.session_state.user_preferences.get("budget", 25000)),
                step=1000,
                help="Your total estimated travel budget for all travelers combined."
            )

            duration = st.slider(
                "Trip Duration (Number of Days)",
                min_value=1,
                max_value=20,
                value=int(st.session_state.user_preferences.get("duration", 4)),
                help="Recommended 2-7 days for weekend and holiday getaways."
            )

            travellers = st.number_input(
                "Number of Travellers",
                min_value=1,
                max_value=12,
                value=int(st.session_state.user_preferences.get("travellers", 2)),
                step=1
            )

        with col2:
            interest_options = [
                "Beaches",
                "Mountains",
                "Adventure",
                "Nature",
                "Historical Places",
                "Religious Places",
                "Food and Culture",
                "Hill Stations",
                "Wildlife",
                "Family Trips"
            ]

            selected_interests = st.multiselect(
                "Select Your Travel Interests (Choose 1 or more)",
                options=interest_options,
                default=st.session_state.user_preferences.get("interests", ["Mountains", "Nature"]),
                help="WanderWise will prioritize destinations matching your passions."
            )

            city_options = [
                "Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata",
                "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Kochi",
                "Chandigarh", "Lucknow", "Bhubaneswar", "Other City in India"
            ]
            default_city = st.session_state.user_preferences.get("starting_city", "Delhi")
            starting_city = st.selectbox(
                "Starting City (Optional - helps estimate intercity transit)",
                options=city_options,
                index=city_options.index(default_city) if default_city in city_options else 0
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Plan My Trip – Find Matching Destinations", type="primary", use_container_width=True):
            if not selected_interests:
                st.warning("Please choose at least one travel interest so we can personalize your destination!")
            else:
                st.session_state.user_preferences = {
                    "budget": budget,
                    "duration": duration,
                    "interests": selected_interests,
                    "starting_city": starting_city,
                    "travellers": travellers
                }
                st.session_state.step = 2
                st.rerun()


    # ==========================================
    # STEP 2: DESTINATION RECOMMENDATIONS
    # ==========================================
    elif st.session_state.step == 2:
        st.subheader("Step 2: Destination Recommendations")
        st.write("Based on your preferences, budget, and trip duration, here are the top 3 recommended Indian destinations:")

        top_recommendations = score_destinations(df, st.session_state.user_preferences)

        if not top_recommendations:
            st.info("No matching destinations found. Try broadening your travel interests or increasing your budget.")
        else:
            cols = st.columns(3, gap="medium")
            for idx, item in enumerate(top_recommendations):
                dest_data = item["data"]
                score = item["score"]
                est_cost = item["estimated_trip_total"]

                with cols[idx]:
                    st.markdown(f"""
                    <div class="dest-card">
                        <div class="dest-card-header">
                            <div>
                                <h3 style="margin:0; font-size:1.35rem; color:#0f172a;">{dest_data['destination']}</h3>
                                <span style="font-size:0.85rem; color:#64748b; font-weight:600;">📍 {dest_data['state']}</span>
                            </div>
                            <span class="match-badge">{score}% Match</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Destination Image with safe fallback
                    img_url = dest_data.get("image_url", "")
                    if pd.notna(img_url) and str(img_url).startswith("http"):
                        st.image(img_url, use_container_width=True)

                    st.write(dest_data.get("description", ""))
                    st.markdown(f"💡 **Why Recommended:** {item['why_recommended']}")

                    st.markdown(f"""
                    <div style="background:#f1f5f9; padding:0.75rem 1rem; border-radius:10px; margin:0.8rem 0; font-size:0.88rem;">
                        <div>⏱️ <b>Suggested Duration:</b> {dest_data.get('suggested_days', 4)} Days</div>
                        <div>🌤️ <b>Best Time:</b> {dest_data.get('best_time', 'Pleasant year round')}</div>
                        <div>💰 <b>Estimated Trip Cost:</b> {format_inr(est_cost)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"👉 Select {dest_data['destination']}", key=f"sel_dest_{idx}", type="primary", use_container_width=True):
                        st.session_state.selected_destination = dest_data
                        # Precalculate costs
                        st.session_state.cost_breakdown = calculate_trip_costs(dest_data, st.session_state.user_preferences)
                        st.session_state.step = 3
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Back to Preferences", use_container_width=True):
                st.session_state.step = 1
                st.rerun()


    # ==========================================
    # STEP 3: COST ESTIMATION & BUDGET ANALYSIS
    # ==========================================
    elif st.session_state.step == 3:
        dest = st.session_state.selected_destination
        prefs = st.session_state.user_preferences

        if not dest:
            st.warning("Please select a destination first.")
            st.session_state.step = 2
            st.rerun()

        costs = calculate_trip_costs(dest, prefs)
        st.session_state.cost_breakdown = costs

        st.subheader(f"Step 3: Cost Estimation for {dest['destination']}, {dest['state']}")
        st.write(f"Itemized expenditure estimate for **{prefs['travellers']} traveler(s)** over **{prefs['duration']} day(s)**.")

        # Budget Status Pill
        if costs['status_code'] == 'within':
            st.markdown(f'<div class="status-pill-within">✅ {costs["budget_status"]} – {costs["status_message"]}</div>', unsafe_allow_html=True)
        elif costs['status_code'] == 'slightly_over':
            st.markdown(f'<div class="status-pill-slightly-over">⚠️ {costs["budget_status"]} – {costs["status_message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-pill-over">🚨 {costs["budget_status"]} – {costs["status_message"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4 Summary Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Budget</div>
                <div class="metric-value">{format_inr(prefs['budget'])}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Estimated Trip Cost</div>
                <div class="metric-value" style="color:#0e7490;">{format_inr(costs['total_estimated_cost'])}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Cost Per Person</div>
                <div class="metric-value">{format_inr(costs['per_person_cost'])}</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            rem = costs['remaining_budget']
            rem_color = "#166534" if rem >= 0 else "#991b1b"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Remaining Balance</div>
                <div class="metric-value" style="color:{rem_color};">{format_inr(rem)}</div>
            </div>
            """, unsafe_allow_html=True)

        # Clean Table of Expense Breakdown
        st.markdown("#### Itemized Expense Breakdown")
        table_data = [
            {"Expense Category": "🚆 Intercity Transportation", "Description": f"{prefs['travellers']} person(s) transit from {prefs.get('starting_city', 'origin')}", "Amount (₹)": format_inr(costs['transportation']), "Per Person (₹)": format_inr(costs['transportation'] // prefs['travellers'])},
            {"Expense Category": "🏨 Accommodation", "Description": f"{costs['nights']} nights stay, {costs['rooms_needed']} room(s)", "Amount (₹)": format_inr(costs['accommodation']), "Per Person (₹)": format_inr(costs['accommodation'] // prefs['travellers'])},
            {"Expense Category": "🍽️ Food & Dining", "Description": f"Breakfast, lunch, and dinner for {prefs['duration']} days", "Amount (₹)": format_inr(costs['food']), "Per Person (₹)": format_inr(costs['food'] // prefs['travellers'])},
            {"Expense Category": "🚕 Local Transportation", "Description": f"Sightseeing cabs, autos, or rentals for {prefs['duration']} days", "Amount (₹)": format_inr(costs['local_transport']), "Per Person (₹)": format_inr(costs['local_transport'] // prefs['travellers'])},
            {"Expense Category": "🎟️ Sightseeing & Activities", "Description": "Monuments, adventure sports, parks, and temple entry fees", "Amount (₹)": format_inr(costs['sightseeing']), "Per Person (₹)": format_inr(costs['sightseeing'] // prefs['travellers'])},
            {"Expense Category": "💼 Miscellaneous / Buffer", "Description": "Emergency buffer and shopping allowance (~7%)", "Amount (₹)": format_inr(costs['miscellaneous']), "Per Person (₹)": format_inr(costs['miscellaneous'] // prefs['travellers'])}
        ]
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        st.caption("ℹ️ *All prices are realistic approximations based on current Indian destination averages. Actual prices may fluctuate based on season and booking time.*")

        st.markdown("<br>", unsafe_allow_html=True)
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ Change Destination", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        with col_next:
            if st.button("Generate Day-Wise Itinerary ➡️", type="primary", use_container_width=True):
                st.session_state.step = 4
                st.rerun()


    # ==========================================
    # STEP 4: AUTOMATIC ITINERARY GENERATION
    # ==========================================
    elif st.session_state.step == 4:
        dest = st.session_state.selected_destination
        prefs = st.session_state.user_preferences

        if not dest:
            st.session_state.step = 2
            st.rerun()

        daily_exp = st.session_state.cost_breakdown['daily_average_expense'] if st.session_state.cost_breakdown else 2000
        itinerary = generate_daywise_itinerary(dest, prefs['duration'], daily_exp)

        st.subheader(f"Step 4: Personalized {prefs['duration']}-Day Itinerary for {dest['destination']}")
        st.write("A practical, geographically structured day-wise travel schedule tailored to your duration.")

        for day in itinerary:
            st.markdown(f"""
            <div class="day-box">
                <div class="day-header">
                    <span>{day['title']}</span>
                    <span style="font-size:0.88rem; color:#64748b;">Est. Daily Spend: {format_inr(day['est_daily_cost'])}</span>
                </div>
                <div style="font-size:0.92rem; line-height:1.6; color:#334155;">
                    <div>🌅 <b>Morning:</b> {day['morning']}</div>
                    <div style="margin-top:0.4rem;">☀️ <b>Afternoon:</b> {day['afternoon']}</div>
                    <div style="margin-top:0.4rem;">🌆 <b>Evening:</b> {day['evening']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ Back to Cost Estimation", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
        with col_next:
            if st.button("Explore Hotels & Travel Tips ➡️", type="primary", use_container_width=True):
                st.session_state.step = 5
                st.rerun()


    # ==========================================
    # STEP 5: HOTELS, ATTRACTIONS & TRAVEL TIPS
    # ==========================================
    elif st.session_state.step == 5:
        dest = st.session_state.selected_destination
        if not dest:
            st.session_state.step = 2
            st.rerun()

        st.subheader(f"Step 5: Hotels, Attractions & Travel Tips – {dest['destination']}")

        tab_hotels, tab_attractions, tab_tips = st.tabs([
            "🏨 Recommended Hotels",
            "📍 Nearby Attractions",
            "💡 Destination Travel Tips"
        ])

        with tab_hotels:
            hotels = parse_hotels(dest.get("hotels", ""))
            if not hotels:
                st.info("Verified hotel data is being compiled for this location.")
            else:
                st.write("Handpicked accommodations across Budget, Standard, and Luxury categories:")
                h_cols = st.columns(len(hotels))
                for i, h in enumerate(hotels):
                    with h_cols[i]:
                        st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1.25rem; height:100%; box-shadow:0 2px 6px rgba(0,0,0,0.03);">
                            <div style="font-weight:700; font-size:1.1rem; color:#0f172a; margin-bottom:0.3rem;">{h['name']}</div>
                            <span style="background:#e0f2fe; color:#0369a1; padding:0.2rem 0.6rem; border-radius:6px; font-size:0.78rem; font-weight:700;">{h['type']}</span>
                            <div style="margin-top:0.8rem; font-size:0.88rem; color:#64748b;">📍 {h['location']}</div>
                            <div style="margin-top:0.4rem; font-size:1.15rem; font-weight:800; color:#0e7490;">₹{h['price']} <span style="font-size:0.8rem; font-weight:500; color:#64748b;">/ night</span></div>
                            <div style="margin-top:1rem;">
                                <a href="{h['link']}" target="_blank" style="text-decoration:none; background:#0e7490; color:white; padding:0.45rem 0.9rem; border-radius:6px; font-size:0.82rem; font-weight:600; display:inline-block;">View Booking / Map ↗</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.caption("ℹ️ *Hotel prices are verified estimates. Booking links open live search or official portals.*")

        with tab_attractions:
            attractions = parse_attractions(dest.get("attractions", ""))
            if not attractions:
                st.info("Attraction list is being updated.")
            else:
                st.write("Top verified sights and points of interest:")
                for att in attractions:
                    st.markdown(f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:1rem 1.25rem; margin-bottom:0.8rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-weight:700; font-size:1.05rem; color:#0f172a;">{att['name']}</div>
                            <span style="background:#f1f5f9; color:#475569; font-weight:600; font-size:0.78rem; padding:0.2rem 0.5rem; border-radius:4px;">{att['category']}</span>
                        </div>
                        <div style="font-size:0.88rem; color:#334155; margin:0.4rem 0;">{att['description']}</div>
                        <div style="font-size:0.82rem; color:#64748b; display:flex; gap:1.5rem;">
                            <span>🎟️ <b>Fee:</b> {att['fee']}</span>
                            <span>⏰ <b>Visiting Hours:</b> {att['hours']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_tips:
            tips = parse_travel_tips(dest.get("travel_tips", ""))
            if not tips:
                st.info("Tips for this destination are available in the summary report.")
            else:
                for k, v in tips.items():
                    st.markdown(f"""
                    <div style="margin-bottom:0.9rem;">
                        <span style="font-weight:700; color:#0e7490;">📌 {k}:</span>
                        <span style="color:#334155; font-size:0.92rem;"> {v}</span>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ Back to Itinerary", use_container_width=True):
                st.session_state.step = 4
                st.rerun()
        with col_next:
            if st.button("View Travel Dashboard ➡️", type="primary", use_container_width=True):
                st.session_state.step = 6
                st.rerun()


    # ==========================================
    # STEP 6: SIMPLE TRAVEL DASHBOARD
    # STRICTLY NO CHARTS OR GRAPHS
    # ==========================================
    elif st.session_state.step == 6:
        dest = st.session_state.selected_destination
        prefs = st.session_state.user_preferences
        costs = st.session_state.cost_breakdown

        if not dest or not costs:
            st.session_state.step = 2
            st.rerun()

        st.subheader("Step 6: Travel Plan Dashboard")
        st.write("A clean executive summary of your entire Indian journey. Everything in one unified view.")

        # Metric Cards Row 1
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Selected Destination", f"{dest['destination']}", f"State: {dest['state']}")
        m2.metric("Trip Budget", format_inr(prefs['budget']), f"{prefs['travellers']} Traveler(s)")
        m3.metric("Estimated Expenses", format_inr(costs['total_estimated_cost']), f"{costs['budget_status']}")
        rem = costs['remaining_budget']
        m4.metric("Remaining Budget", format_inr(rem), "Buffer Balance" if rem >= 0 else "Over Budget")

        st.markdown("<br>", unsafe_allow_html=True)

        # Expense Summary Table
        st.markdown("#### Comprehensive Cost Breakdown Summary")
        summary_rows = [
            {"Category": "Intercity Travel", "Cost (₹)": format_inr(costs['transportation']), "Share": f"{(costs['transportation']/costs['total_estimated_cost'])*100:.1f}%"},
            {"Category": "Accommodation", "Cost (₹)": format_inr(costs['accommodation']), "Share": f"{(costs['accommodation']/costs['total_estimated_cost'])*100:.1f}%"},
            {"Category": "Food & Dining", "Cost (₹)": format_inr(costs['food']), "Share": f"{(costs['food']/costs['total_estimated_cost'])*100:.1f}%"},
            {"Category": "Local Sightseeing & Transit", "Cost (₹)": format_inr(costs['local_transport'] + costs['sightseeing']), "Share": f"{((costs['local_transport'] + costs['sightseeing'])/costs['total_estimated_cost'])*100:.1f}%"},
            {"Category": "Contingency & Buffer", "Cost (₹)": format_inr(costs['miscellaneous']), "Share": f"{(costs['miscellaneous']/costs['total_estimated_cost'])*100:.1f}%"},
            {"Category": "TOTAL ESTIMATED EXPENSE", "Cost (₹)": format_inr(costs['total_estimated_cost']), "Share": "100.0%"}
        ]
        st.table(pd.DataFrame(summary_rows))

        # Dashboard Highlights in clean text cards
        col_l, col_r = st.columns([1, 1], gap="medium")
        with col_l:
            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:1.25rem; height:100%;">
                <h4 style="margin-top:0; color:#0e7490;">📅 Itinerary Highlights</h4>
                <p>• <b>Duration:</b> {prefs['duration']} Days & {costs['nights']} Nights</p>
                <p>• <b>Starting Location:</b> {prefs.get('starting_city', 'India')}</p>
                <p>• <b>Ideal Visiting Season:</b> {dest.get('best_time', 'September to May')}</p>
                <p>• <b>Daily Average Spend:</b> {format_inr(costs['daily_average_expense'])} per day</p>
            </div>
            """, unsafe_allow_html=True)

        with col_r:
            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:1.25rem; height:100%;">
                <h4 style="margin-top:0; color:#0e7490;">🎒 Travel Readiness</h4>
                <p>• <b>Budget Viability:</b> {costs['budget_status']}</p>
                <p>• <b>Accommodation Plan:</b> {costs['rooms_needed']} Room(s) reserved</p>
                <p>• <b>Interests Covered:</b> {', '.join(prefs['interests'])}</p>
                <p>• <b>Documentation:</b> Ready for instant PDF generation & printing</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ Back to Hotels & Tips", use_container_width=True):
                st.session_state.step = 5
                st.rerun()
        with col_next:
            if st.button("Download or Print PDF Report ➡️", type="primary", use_container_width=True):
                st.session_state.step = 7
                st.rerun()


    # ==========================================
    # STEP 7: PRINT OR DOWNLOAD PDF REPORT
    # ==========================================
    elif st.session_state.step == 7:
        dest = st.session_state.selected_destination
        prefs = st.session_state.user_preferences
        costs = st.session_state.cost_breakdown

        if not dest or not costs:
            st.session_state.step = 2
            st.rerun()

        daily_exp = costs['daily_average_expense']
        itinerary = generate_daywise_itinerary(dest, prefs['duration'], daily_exp)

        st.subheader("Step 7: Download or Print Your Complete Travel Plan")
        st.write("Your personalized travel dossier is ready. You can download the professionally formatted PDF or print it directly from your browser.")

        # Generate ReportLab PDF in memory
        with st.spinner("Compiling high-resolution PDF document..."):
            pdf_bytes = generate_pdf_report(dest, prefs, costs, itinerary)

        # Download & Print Buttons
        col_btn1, col_btn2 = st.columns(2, gap="medium")
        with col_btn1:
            st.download_button(
                label=f"📥 Download Travel Plan (PDF)",
                data=pdf_bytes,
                file_name=f"WanderWise_Trip_Plan_{dest['destination'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )

        with col_btn2:
            # Browser print trigger
            st.markdown("""
            <button onclick="window.print()" style="
                width: 100%;
                background-color: #0f172a;
                color: white;
                border: none;
                padding: 0.65rem 1.25rem;
                font-size: 1rem;
                font-weight: 600;
                border-radius: 8px;
                cursor: pointer;
            ">🖨️ Print Travel Plan (Browser)</button>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # PDF Document Preview Section
        with st.expander("📄 Click to Preview PDF Travel Plan Contents", expanded=True):
            st.markdown(f"### 🧭 WanderWise Travel Dossier – {dest['destination']}")
            st.markdown(f"**Traveler(s):** {prefs['travellers']} | **Duration:** {prefs['duration']} Days | **Budget Status:** {costs['budget_status']}")
            st.divider()

            st.write(f"**Selected Destination:** {dest['destination']}, {dest['state']}")
            st.write(f"**Overview:** {dest['description']}")
            st.write(f"**Total Estimated Trip Cost:** {format_inr(costs['total_estimated_cost'])} (Budget: {format_inr(prefs['budget'])})")

            st.markdown("#### Day-Wise Schedule")
            for day in itinerary:
                st.markdown(f"**Day {day['day']}:** {day['title']}")
                st.write(f"- 🌅 Morning: {day['morning']}")
                st.write(f"- ☀️ Afternoon: {day['afternoon']}")
                st.write(f"- 🌆 Evening: {day['evening']}")

        st.markdown("<br>", unsafe_allow_html=True)
        col_back, col_reset = st.columns(2)
        with col_back:
            if st.button("⬅️ Back to Dashboard", use_container_width=True):
                st.session_state.step = 6
                st.rerun()
        with col_reset:
            if st.button("🔄 Plan Another Trip", use_container_width=True):
                st.session_state.step = 1
                st.session_state.selected_destination = None
                st.session_state.cost_breakdown = None
                st.rerun()


if __name__ == "__main__":
    main()
