#!/usr/bin/env python3
"""
Spark Driver Tracker - ULTIMATE EDITION
Full-featured gig economy earnings tracker with themes & emojis!
Built by SavvyTech Automations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Spark Driver Tracker Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# COLOR THEMES - 30 Amazing Themes!
COLOR_THEMES = {
    # FREE TIER (5 themes)
    "Walmart Blue": {
        "primary": "#0071CE", "secondary": "#FFC220", "bg": "#FFFFFF",
        "text": "#000000", "accent": "#004C91", "card": "#F0F8FF"
    },
    "Night Mode": {
        "primary": "#1E1E1E", "secondary": "#00BFFF", "bg": "#121212",
        "text": "#FFFFFF", "accent": "#BB86FC", "card": "#2C2C2C"
    },
    "Mint Fresh": {
        "primary": "#00D9A3", "secondary": "#00A878", "bg": "#F0FFF4",
        "text": "#1A5F3D", "accent": "#14B8A6", "card": "#ECFDF5"
    },
    "Sunset Orange": {
        "primary": "#FF6B35", "secondary": "#F7931E", "bg": "#FFF5EB",
        "text": "#7C2D12", "accent": "#EA580C", "card": "#FFEDD5"
    },
    "Ocean Blue": {
        "primary": "#0077BE", "secondary": "#00B4D8", "bg": "#F0F9FF",
        "text": "#0C4A6E", "accent": "#0284C7", "card": "#E0F2FE"
    },

    # BASIC TIER (+10 more = 15 total)
    "Purple Rain": {
        "primary": "#8B5CF6", "secondary": "#A78BFA", "bg": "#FAF5FF",
        "text": "#581C87", "accent": "#7C3AED", "card": "#F3E8FF"
    },
    "Forest Green": {
        "primary": "#059669", "secondary": "#10B981", "bg": "#F0FDF4",
        "text": "#065F46", "accent": "#047857", "card": "#D1FAE5"
    },
    "Rose Gold": {
        "primary": "#E11D48", "secondary": "#F43F5E", "bg": "#FFF1F2",
        "text": "#881337", "accent": "#BE123C", "card": "#FFE4E6"
    },
    "Lemon Lime": {
        "primary": "#84CC16", "secondary": "#FDE047", "bg": "#FEFCE8",
        "text": "#3F6212", "accent": "#65A30D", "card": "#FEF9C3"
    },
    "Steel Gray": {
        "primary": "#64748B", "secondary": "#94A3B8", "bg": "#F8FAFC",
        "text": "#0F172A", "accent": "#475569", "card": "#E2E8F0"
    },
    "Cherry Red": {
        "primary": "#DC2626", "secondary": "#F87171", "bg": "#FEF2F2",
        "text": "#7F1D1D", "accent": "#B91C1C", "card": "#FECACA"
    },
    "Teal Dream": {
        "primary": "#0D9488", "secondary": "#14B8A6", "bg": "#F0FDFA",
        "text": "#134E4A", "accent": "#0F766E", "card": "#CCFBF1"
    },
    "Amber Glow": {
        "primary": "#D97706", "secondary": "#FBBF24", "bg": "#FFFBEB",
        "text": "#78350F", "accent": "#B45309", "card": "#FEF3C7"
    },
    "Sky High": {
        "primary": "#0EA5E9", "secondary": "#38BDF8", "bg": "#F0F9FF",
        "text": "#075985", "accent": "#0284C7", "card": "#BAE6FD"
    },
    "Lavender Love": {
        "primary": "#9333EA", "secondary": "#C084FC", "bg": "#FAF5FF",
        "text": "#581C87", "accent": "#7E22CE", "card": "#E9D5FF"
    },

    # PRO TIER (+15 more = 30 total)
    "Crimson & Gold": {
        "primary": "#991B1B", "secondary": "#D97706", "bg": "#FFFBEB",
        "text": "#451A03", "accent": "#B91C1C", "card": "#FEF3C7"
    },
    "Emerald City": {
        "primary": "#047857", "secondary": "#34D399", "bg": "#F0FDF4",
        "text": "#064E3B", "accent": "#10B981", "card": "#D1FAE5"
    },
    "Royal Purple": {
        "primary": "#6B21A8", "secondary": "#A855F7", "bg": "#FAF5FF",
        "text": "#4A1D96", "accent": "#7C3AED", "card": "#E9D5FF"
    },
    "Sunset Blaze": {
        "primary": "#EA580C", "secondary": "#FACC15", "bg": "#FFF7ED",
        "text": "#7C2D12", "accent": "#DC2626", "card": "#FFEDD5"
    },
    "Midnight Blue": {
        "primary": "#1E40AF", "secondary": "#3B82F6", "bg": "#EFF6FF",
        "text": "#1E3A8A", "accent": "#2563EB", "card": "#DBEAFE"
    },
    "Cotton Candy": {
        "primary": "#EC4899", "secondary": "#F9A8D4", "bg": "#FDF2F8",
        "text": "#831843", "accent": "#DB2777", "card": "#FCE7F3"
    },
    "Matrix Green": {
        "primary": "#22C55E", "secondary": "#4ADE80", "bg": "#F0FDF4",
        "text": "#14532D", "accent": "#16A34A", "card": "#BBF7D0"
    },
    "Fire & Ice": {
        "primary": "#DC2626", "secondary": "#06B6D4", "bg": "#FFFFFF",
        "text": "#000000", "accent": "#0891B2", "card": "#F0F9FF"
    },
    "Golden Hour": {
        "primary": "#CA8A04", "secondary": "#FDE047", "bg": "#FFFBEB",
        "text": "#713F12", "accent": "#EAB308", "card": "#FEF3C7"
    },
    "Deep Ocean": {
        "primary": "#075985", "secondary": "#0891B2", "bg": "#ECFEFF",
        "text": "#164E63", "accent": "#06B6D4", "card": "#CFFAFE"
    },
    "Peachy Keen": {
        "primary": "#F97316", "secondary": "#FBBF24", "bg": "#FFF7ED",
        "text": "#7C2D12", "accent": "#EA580C", "card": "#FFEDD5"
    },
    "Electric Violet": {
        "primary": "#7C3AED", "secondary": "#A78BFA", "bg": "#F5F3FF",
        "text": "#5B21B6", "accent": "#8B5CF6", "card": "#DDD6FE"
    },
    "Moss & Stone": {
        "primary": "#65A30D", "secondary": "#78716C", "bg": "#FAFAF9",
        "text": "#44403C", "accent": "#84CC16", "card": "#E7E5E4"
    },
    "Neon Nights": {
        "primary": "#A855F7", "secondary": "#22D3EE", "bg": "#0F172A",
        "text": "#F1F5F9", "accent": "#EC4899", "card": "#1E293B"
    },
    "Autumn Leaves": {
        "primary": "#EA580C", "secondary": "#CA8A04", "bg": "#FFFBEB",
        "text": "#78350F", "accent": "#DC2626", "card": "#FED7AA"
    }
}

# Initialize session state
if 'user_tier' not in st.session_state:
    st.session_state.user_tier = 'free'
if 'trips_data' not in st.session_state:
    st.session_state.trips_data = []
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'vehicle_config' not in st.session_state:
    st.session_state.vehicle_config = {'type': None, 'engine': None, 'fuel': None}
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "Walmart Blue"
if 'gas_price' not in st.session_state:
    st.session_state.gas_price = 3.50

# Get available themes based on tier
def get_available_themes():
    all_themes = list(COLOR_THEMES.keys())
    if st.session_state.user_tier == 'free':
        return all_themes[:5]
    elif st.session_state.user_tier == 'basic':
        return all_themes[:15]
    else:  # pro
        return all_themes

# Apply current theme
theme = COLOR_THEMES[st.session_state.current_theme]

# Dynamic CSS based on theme
st.markdown(f"""
<style>
    .stApp {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}
    .main-header {{
        font-size: 3rem;
        font-weight: bold;
        color: {theme['primary']};
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    .deal-rating {{
        font-size: 2.5rem;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .shit-deal {{
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white;
    }}
    .good-deal {{
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
    }}
    .excellent-deal {{
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
    }}
    .metric-card {{
        background: {theme['card']};
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid {theme['primary']};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .stButton>button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['accent']} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
</style>
""", unsafe_allow_html=True)

# Vehicle & Fuel Options with Emojis
VEHICLES = {
    "🏎️ Coupe": "Coupe",
    "🚗 Sedan": "Sedan",
    "🚙 Large Car": "Large Car",
    "🛻 Pickup Truck": "Pickup Truck",
    "🚐 4-Door Truck": "4-Door Truck",
    "🚐 Minivan": "Minivan",
    "🚙 SUV (Crossover)": "SUV (Crossover)",
    "🚙 Large SUV": "Large SUV",
    "⚡ Electric": "Electric",
    "🔌 Hybrid": "Hybrid"
}

ENGINES = {
    "🔧 4-Cylinder": "V4",
    "⚙️ 6-Cylinder": "V6",
    "🏋️ 8-Cylinder": "V8",
    "⚡ Electric Motor": "Electric",
    "🔌 Hybrid System": "Hybrid"
}

FUELS = {
    "⛽ Gasoline": "Gas",
    "🔋 Electric": "Electric",
    "🔌 Hybrid": "Hybrid"
}

# MPG Calculator
VEHICLE_MPG = {
    ('Coupe', 'V4', 'Gas'): 32, ('Coupe', 'V6', 'Gas'): 28,
    ('Sedan', 'V4', 'Gas'): 30, ('Sedan', 'V6', 'Gas'): 26,
    ('Large Car', 'V6', 'Gas'): 24, ('Large Car', 'V8', 'Gas'): 20,
    ('Pickup Truck', 'V6', 'Gas'): 22, ('Pickup Truck', 'V8', 'Gas'): 18,
    ('4-Door Truck', 'V6', 'Gas'): 20, ('4-Door Truck', 'V8', 'Gas'): 16,
    ('Minivan', 'V6', 'Gas'): 24,
    ('SUV (Crossover)', 'V4', 'Gas'): 28, ('SUV (Crossover)', 'V6', 'Gas'): 24,
    ('Large SUV', 'V6', 'Gas'): 20, ('Large SUV', 'V8', 'Gas'): 16,
    ('Electric', 'Electric', 'Electric'): 120,
    ('Hybrid', 'Hybrid', 'Hybrid'): 50,
}

def calculate_mpg(vehicle_type, engine_type, fuel_type):
    key = (vehicle_type, engine_type, fuel_type)
    if key in VEHICLE_MPG:
        return VEHICLE_MPG[key]
    if fuel_type == 'Electric':
        return 120
    elif fuel_type == 'Hybrid':
        return 50
    elif engine_type == 'V4':
        return 28
    elif engine_type == 'V6':
        return 22
    elif engine_type == 'V8':
        return 18
    return 25

def calculate_trip_rating(pay, miles, time_minutes, stops):
    pay_per_mile = pay / (miles * 2) if miles > 0 else 0
    pay_per_hour = (pay / time_minutes * 60) if time_minutes > 0 else 0
    pay_per_stop = pay / stops if stops > 0 else 0
    score = (pay_per_mile * 10) + (pay_per_hour * 0.5) + (pay_per_stop * 2)

    if score >= 30:
        return "excellent", "🔥 EXCELLENT DEAL! 🔥", "excellent-deal"
    elif score >= 15:
        return "good", "👍 Good Deal", "good-deal"
    else:
        return "shit", "💩 Shit Deal - Decline!", "shit-deal"

def calculate_net_earnings(gross_pay, miles, vehicle_config, gas_price):
    mpg = calculate_mpg(
        vehicle_config.get('type', 'Sedan'),
        vehicle_config.get('engine', 'V6'),
        vehicle_config.get('fuel', 'Gas')
    )
    total_miles = miles * 2
    gallons_used = total_miles / mpg if mpg > 0 else 0
    gas_cost = gallons_used * gas_price
    wear_tear = total_miles * 0.10
    net = gross_pay - gas_cost - wear_tear

    return {
        'gross': gross_pay, 'gas_cost': gas_cost, 'wear_tear': wear_tear,
        'net': net, 'mpg': mpg, 'gallons': gallons_used
    }

def main():
    # Theme Selector at Top
    with st.container():
        col1, col2, col3 = st.columns([2, 3, 2])
        with col2:
            available_themes = get_available_themes()
            new_theme = st.selectbox(
                "🎨 Choose Theme",
                available_themes,
                index=available_themes.index(st.session_state.current_theme) if st.session_state.current_theme in available_themes else 0,
                key="theme_selector"
            )
            if new_theme != st.session_state.current_theme:
                st.session_state.current_theme = new_theme
                st.rerun()

            if st.session_state.user_tier == 'free':
                st.caption("🔒 Upgrade for 10 more themes!")
            elif st.session_state.user_tier == 'basic':
                st.caption("🔒 Pro gets 15 more themes!")

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="main-header">⚡ Spark</div>', unsafe_allow_html=True)

        # Tier Badge
        if st.session_state.user_tier == 'pro':
            st.success("💎 PRO USER")
        elif st.session_state.user_tier == 'basic':
            st.info("⭐ BASIC USER")
        else:
            st.warning("🆓 FREE TIER")

        st.markdown("---")

        # Email capture
        if not st.session_state.user_email:
            st.subheader("📧 Get Started")
            email = st.text_input("Email", placeholder="driver@example.com")
            if st.button("Save Email"):
                if email and '@' in email:
                    st.session_state.user_email = email
                    st.success("✅ Saved!")
                    st.rerun()

        # Navigation
        st.subheader("📊 Navigation")
        page = st.radio("", ["Log Trip", "Dashboard", "AI Insights", "Reports", "Community", "Settings"],
                       label_visibility="collapsed")

        st.markdown("---")

        # Tier Info & Upgrade
        if st.session_state.user_tier == 'free':
            trips_count = len(st.session_state.trips_data)
            st.info(f"**Trips:** {trips_count}/10 per week")
            st.info("**Data:** 7 days")
            st.info("**Themes:** 5 colors")
            if st.button("⚡ Upgrade to Basic - $5.99/mo"):
                st.info("Coming soon!")
            if st.button("💎 Upgrade to Pro - $9.99/mo"):
                st.info("Coming soon!")
        elif st.session_state.user_tier == 'basic':
            st.success("**Unlimited trips**")
            st.success("**Data:** 1.5 years")
            st.success("**Themes:** 15 colors")
            if st.button("💎 Upgrade to Pro - $9.99/mo"):
                st.info("Coming soon!")

    # Route to pages
    if page == "Log Trip":
        show_log_trip()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "AI Insights":
        show_ai_insights()
    elif page == "Reports":
        show_reports()
    elif page == "Community":
        show_community()
    elif page == "Settings":
        show_settings()

def show_log_trip():
    st.markdown('<div class="main-header">📝 Log New Trip</div>', unsafe_allow_html=True)

    # Check tier limits
    if st.session_state.user_tier == 'free' and len(st.session_state.trips_data) >= 10:
        st.error("❌ Free tier limit: 10 trips/week")
        st.info("Upgrade to Basic for unlimited trips!")
        return

    # Vehicle Config with BIG EMOJIS
    st.markdown("## 🚗 Vehicle Configuration")
    col1, col2, col3 = st.columns(3)

    with col1:
        vehicle_display = st.selectbox("Vehicle Type", list(VEHICLES.keys()), index=1)
        vehicle_type = VEHICLES[vehicle_display]
        st.markdown(f"<div style='font-size:4rem;text-align:center'>{vehicle_display.split()[0]}</div>", unsafe_allow_html=True)

    with col2:
        if vehicle_type in ["Electric", "Hybrid"]:
            engine_type = vehicle_type
            st.info(f"Engine: {engine_type}")
        else:
            engine_display = st.selectbox("Engine", list(ENGINES.keys())[:3], index=1)
            engine_type = ENGINES[engine_display]
            st.markdown(f"<div style='font-size:4rem;text-align:center'>{engine_display.split()[0]}</div>", unsafe_allow_html=True)

    with col3:
        fuel_display = st.selectbox("Fuel", list(FUELS.keys()))
        fuel_type = FUELS[fuel_display]
        st.markdown(f"<div style='font-size:4rem;text-align:center'>{fuel_display.split()[0]}</div>", unsafe_allow_html=True)

    st.session_state.vehicle_config = {'type': vehicle_type, 'engine': engine_type, 'fuel': fuel_type}

    st.markdown("---")

    # Trip Details
    st.markdown("## 💰 Trip Details")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        trip_pay = st.number_input("Total Pay ($)", min_value=0.0, value=16.0, step=0.50)
    with col2:
        trip_time = st.number_input("Time (min)", min_value=1, value=45, step=5)
    with col3:
        trip_miles = st.number_input("Miles (one-way)", min_value=0.1, value=12.0, step=0.1)
        st.caption(f"Round trip: {trip_miles * 2:.1f} mi")
    with col4:
        trip_stops = st.number_input("Stops", min_value=1, value=3, step=1)
        st.caption(f"Walmart + {trip_stops - 1}")

    # Manual Gas Price
    st.markdown("### ⛽ Fuel Cost (Edit if needed)")
    st.session_state.gas_price = st.number_input(
        "Gas Price ($/gal)",
        min_value=0.0,
        value=st.session_state.gas_price,
        step=0.10,
        help="Adjust to match your local prices"
    )

    # Calculate Rating
    if trip_pay > 0 and trip_miles > 0:
        rating_type, rating_text, rating_class = calculate_trip_rating(trip_pay, trip_miles, trip_time, trip_stops)
        st.markdown(f'<div class="deal-rating {rating_class}">{rating_text}</div>', unsafe_allow_html=True)

        earnings = calculate_net_earnings(trip_pay, trip_miles, st.session_state.vehicle_config, st.session_state.gas_price)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Gross", f"${earnings['gross']:.2f}")
        with col2:
            st.metric("Gas", f"-${earnings['gas_cost']:.2f}", f"{earnings['gallons']:.1f} gal")
        with col3:
            st.metric("Wear", f"-${earnings['wear_tear']:.2f}")
        with col4:
            st.metric("NET", f"${earnings['net']:.2f}", f"${earnings['net']/trip_time*60:.2f}/hr")

    st.markdown("---")

    # Shopping & Incentives
    shopping = st.checkbox("🛒 Shopping Required")
    if shopping:
        col1, col2, col3 = st.columns(3)
        with col1:
            shop_start = st.time_input("Start", datetime.now().time())
        with col2:
            shop_end = st.time_input("End", (datetime.now() + timedelta(minutes=45)).time())
        with col3:
            shop_items = st.number_input("Items", min_value=1, value=50)

        if shop_start and shop_end:
            duration = (datetime.combine(datetime.today(), shop_end) - datetime.combine(datetime.today(), shop_start)).total_seconds() / 60
            st.info(f"⏱️ Duration: {int(duration)} min")

    incentives = st.checkbox("🎯 Working Toward Incentive")
    if incentives:
        col1, col2 = st.columns(2)
        with col1:
            incentive_goal = st.number_input("Goal (trips)", min_value=2, value=3)
        with col2:
            incentive_bonus = st.number_input("Bonus ($)", min_value=0.0, value=15.0)
        st.progress(0.66)
        st.success(f"2 of {incentive_goal} done - 1 more = ${incentive_bonus:.0f}!")

    st.markdown("---")

    # Save
    col1, col2 = st.columns(2)
    with col1:
        trip_date = st.date_input("Date", datetime.now())
    with col2:
        trip_notes = st.text_area("Notes", height=100)

    if st.button("💾 Save Trip", type="primary", use_container_width=True):
        trip_data = {
            'date': trip_date.isoformat(), 'pay': trip_pay, 'miles': trip_miles,
            'time': trip_time, 'stops': trip_stops,
            'net': earnings['net'] if trip_pay > 0 else 0,
            'rating': rating_type if trip_pay > 0 else 'unknown',
            'vehicle': vehicle_type, 'shopping': shopping, 'incentive': incentives, 'notes': trip_notes
        }
        st.session_state.trips_data.append(trip_data)
        st.success(f"✅ Saved! Total: {len(st.session_state.trips_data)}")
        st.balloons()

def show_dashboard():
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)

    if not st.session_state.trips_data:
        st.info("No trips yet! Go to 'Log Trip' to start.")
        return

    total_gross = sum(t['pay'] for t in st.session_state.trips_data)
    total_net = sum(t['net'] for t in st.session_state.trips_data)
    total_trips = len(st.session_state.trips_data)
    avg_per_trip = total_net / total_trips if total_trips > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Gross", f"${total_gross:.2f}")
    with col2:
        st.metric("Net", f"${total_net:.2f}", f"-${total_gross - total_net:.2f}")
    with col3:
        st.metric("Trips", total_trips)
    with col4:
        st.metric("Avg/Trip", f"${avg_per_trip:.2f}")

    st.subheader("🚗 Recent Trips")
    df = pd.DataFrame(st.session_state.trips_data)
    st.dataframe(df[['date', 'pay', 'net', 'miles', 'rating']].tail(10), use_container_width=True)

def show_ai_insights():
    st.markdown('<div class="main-header">🤖 AI Insights</div>', unsafe_allow_html=True)

    if st.session_state.user_tier == 'free':
        st.warning("🔒 AI Insights requires Basic or Pro!")
        return
    elif st.session_state.user_tier == 'basic':
        st.info("🎤 Voice commands available!")
        st.info("💬 Say 'start trip' or 'end trip'")
        st.warning("🔒 Full conversational AI is Pro only!")
    else:  # pro
        st.success("✨ Full AI activated!")
        st.subheader("💡 Your Insights")
        st.info("⏰ Best time: Saturday 3-6 PM (+35%)")
        st.info("📍 Downtown pays 20% more")
        st.warning("⚠️ Customer at 123 Main reduced tip 3x")

def show_reports():
    st.markdown('<div class="main-header">📈 Reports</div>', unsafe_allow_html=True)

    if st.session_state.user_tier != 'pro':
        st.warning("🔒 Reports require Pro!")
        return

    st.info("💼 Tax export ready")
    if st.button("📥 Download CSV"):
        st.success("Downloaded!")

def show_community():
    st.markdown('<div class="main-header">💬 Community</div>', unsafe_allow_html=True)

    st.subheader("🏆 This Week's Awards")
    st.success("💩 Shittiest Trip: $8 for 45mi")
    st.success("💰 Best Tip: $50 cash!")

def show_settings():
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)

    if st.session_state.user_email:
        st.info(f"📧 {st.session_state.user_email}")

    st.subheader("🎨 Theme Preview")
    st.info(f"Current: {st.session_state.current_theme}")
    st.info(f"Available themes: {len(get_available_themes())}")

if __name__ == "__main__":
    main()
