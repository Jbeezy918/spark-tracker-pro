#!/usr/bin/env python3
"""
Spark Driver Tracker - Pro Version
Full-featured gig economy earnings tracker
Built by SavvyTech Automations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="Spark Driver Tracker Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_tier' not in st.session_state:
    st.session_state.user_tier = 'free'
if 'trips_data' not in st.session_state:
    st.session_state.trips_data = []
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'vehicle_config' not in st.session_state:
    st.session_state.vehicle_config = {
        'type': None,
        'engine': None,
        'fuel': None
    }

# Vehicle data for MPG calculations
VEHICLE_MPG = {
    ('Coupe', 'V4', 'Gas'): 32,
    ('Coupe', 'V6', 'Gas'): 28,
    ('Sedan', 'V4', 'Gas'): 30,
    ('Sedan', 'V6', 'Gas'): 26,
    ('Large Car', 'V6', 'Gas'): 24,
    ('Large Car', 'V8', 'Gas'): 20,
    ('Pickup Truck', 'V6', 'Gas'): 22,
    ('Pickup Truck', 'V8', 'Gas'): 18,
    ('4-Door Truck', 'V6', 'Gas'): 20,
    ('4-Door Truck', 'V8', 'Gas'): 16,
    ('Minivan', 'V6', 'Gas'): 24,
    ('SUV (Crossover)', 'V4', 'Gas'): 28,
    ('SUV (Crossover)', 'V6', 'Gas'): 24,
    ('Large SUV', 'V6', 'Gas'): 20,
    ('Large SUV', 'V8', 'Gas'): 16,
    ('Electric', 'Electric', 'Electric'): 120,  # MPGe
    ('Hybrid', 'Hybrid', 'Hybrid'): 50,
}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #004C91;
        text-align: center;
        margin-bottom: 1rem;
    }
    .deal-rating {
        font-size: 2.5rem;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-weight: bold;
    }
    .shit-deal {
        background: #ff4444;
        color: white;
    }
    .good-deal {
        background: #44ff44;
        color: #333;
    }
    .excellent-deal {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
    }
    .pro-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    .free-badge {
        background: #28A745;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def calculate_mpg(vehicle_type, engine_type, fuel_type):
    """Calculate MPG based on vehicle configuration"""
    key = (vehicle_type, engine_type, fuel_type)
    # Try exact match
    if key in VEHICLE_MPG:
        return VEHICLE_MPG[key]

    # Fallback estimates
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
    return 25  # Default

def calculate_trip_rating(pay, miles, time_minutes, stops):
    """Calculate if trip is shit, good, or excellent"""
    # Normalize metrics
    pay_per_mile = pay / (miles * 2) if miles > 0 else 0  # Round trip
    pay_per_hour = (pay / time_minutes * 60) if time_minutes > 0 else 0
    pay_per_stop = pay / stops if stops > 0 else 0

    # Scoring (higher is better)
    score = (pay_per_mile * 10) + (pay_per_hour * 0.5) + (pay_per_stop * 2)

    if score >= 30:
        return "excellent", "🔥 EXCELLENT DEAL! 🔥", "excellent-deal"
    elif score >= 15:
        return "good", "👍 Good Deal", "good-deal"
    else:
        return "shit", "💩 Shit Deal - Decline!", "shit-deal"

def calculate_net_earnings(gross_pay, miles, vehicle_config, gas_price=3.50):
    """Calculate net earnings after expenses"""
    # Get MPG
    mpg = calculate_mpg(
        vehicle_config.get('type', 'Sedan'),
        vehicle_config.get('engine', 'V6'),
        vehicle_config.get('fuel', 'Gas')
    )

    # Calculate costs
    total_miles = miles * 2  # Round trip
    gallons_used = total_miles / mpg if mpg > 0 else 0
    gas_cost = gallons_used * gas_price
    wear_tear = total_miles * 0.10  # $0.10/mile depreciation

    net = gross_pay - gas_cost - wear_tear

    return {
        'gross': gross_pay,
        'gas_cost': gas_cost,
        'wear_tear': wear_tear,
        'net': net,
        'mpg': mpg,
        'gallons': gallons_used
    }

def main():
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="main-header">⚡ Spark</div>', unsafe_allow_html=True)

        # Tier badge
        if st.session_state.user_tier == 'pro':
            st.markdown('<span class="pro-badge">PRO USER</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="free-badge">FREE TIER</span>', unsafe_allow_html=True)

        st.markdown("---")

        # Email capture
        if not st.session_state.user_email:
            st.subheader("📧 Get Started")
            email = st.text_input("Email Address", placeholder="driver@example.com")
            if st.button("Save", use_container_width=True):
                if email and '@' in email:
                    st.session_state.user_email = email
                    st.success("✅ Email saved!")
                    st.rerun()

        # Navigation
        st.subheader("📊 Navigation")
        page = st.radio(
            "Go to:",
            ["Log Trip", "Dashboard", "AI Insights", "Reports", "Community", "Settings"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Upgrade CTA
        if st.session_state.user_tier == 'free':
            trips_count = len(st.session_state.trips_data)
            st.info(f"**Free Tier:** {trips_count}/50 trips")
            st.info("**Data:** 7 days only")
            if st.button("⚡ Upgrade to Pro - $12/mo", use_container_width=True, type="primary"):
                st.switch_page("pages/upgrade.py")  # Would redirect to Stripe

    # Main content
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
    """Enhanced trip logging with all features"""
    st.markdown('<div class="main-header">📝 Log New Trip</div>', unsafe_allow_html=True)

    # Check free tier limit
    if st.session_state.user_tier == 'free' and len(st.session_state.trips_data) >= 50:
        st.error("❌ Free tier limit reached (50 trips)")
        st.info("Upgrade to Pro for unlimited trip tracking!")
        return

    # Vehicle Configuration (Required)
    st.subheader("🚗 Vehicle Configuration")
    col1, col2, col3 = st.columns(3)

    with col1:
        vehicle_type = st.selectbox(
            "Vehicle Type",
            [
                "Coupe", "Sedan", "Large Car",
                "Pickup Truck", "4-Door Truck",
                "Minivan", "SUV (Crossover)", "Large SUV",
                "Electric", "Hybrid"
            ],
            index=1  # Default to Sedan
        )

    with col2:
        if vehicle_type in ["Electric", "Hybrid"]:
            engine_type = vehicle_type
            st.info(f"Engine: {engine_type}")
        else:
            engine_type = st.selectbox("Engine Type", ["V4", "V6", "V8"])

    with col3:
        if vehicle_type == "Electric":
            fuel_type = "Electric"
            st.info("Fuel: Electric")
        elif vehicle_type == "Hybrid":
            fuel_type = "Hybrid"
            st.info("Fuel: Hybrid")
        else:
            fuel_type = "Gas"
            st.info("Fuel: Gasoline")

    # Store vehicle config
    st.session_state.vehicle_config = {
        'type': vehicle_type,
        'engine': engine_type,
        'fuel': fuel_type
    }

    st.markdown("---")

    # Trip Details
    st.subheader("💰 Trip Details")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        trip_pay = st.number_input("Total Pay ($)", min_value=0.0, value=16.0, step=0.50)

    with col2:
        trip_time = st.number_input("Est. Time (minutes)", min_value=1, value=45, step=5)

    with col3:
        trip_miles = st.number_input("Miles (one-way)", min_value=0.1, value=12.0, step=0.1)
        st.caption(f"Round trip: {trip_miles * 2:.1f} miles")

    with col4:
        trip_stops = st.number_input("Total Stops", min_value=1, value=3, step=1)
        st.caption(f"Walmart + {trip_stops - 1} deliveries")

    # Calculate and show trip rating
    if trip_pay > 0 and trip_miles > 0 and trip_time > 0:
        rating_type, rating_text, rating_class = calculate_trip_rating(
            trip_pay, trip_miles, trip_time, trip_stops
        )

        st.markdown(f'<div class="deal-rating {rating_class}">{rating_text}</div>',
                   unsafe_allow_html=True)

        # Show detailed breakdown
        earnings = calculate_net_earnings(
            trip_pay, trip_miles, st.session_state.vehicle_config
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Gross Pay", f"${earnings['gross']:.2f}")
        with col2:
            st.metric("Gas Cost", f"-${earnings['gas_cost']:.2f}",
                     delta=f"{earnings['gallons']:.1f} gal")
        with col3:
            st.metric("Wear & Tear", f"-${earnings['wear_tear']:.2f}")
        with col4:
            st.metric("NET Earnings", f"${earnings['net']:.2f}",
                     delta=f"${earnings['net']/trip_time*60:.2f}/hr")

    st.markdown("---")

    # Shopping Checkbox (Expandable)
    shopping = st.checkbox("🛒 Shopping Required")
    if shopping:
        col1, col2, col3 = st.columns(3)
        with col1:
            shop_start = st.time_input("Start Time", datetime.now().time())
        with col2:
            shop_end = st.time_input("End Time", (datetime.now() + timedelta(minutes=45)).time())
        with col3:
            shop_items = st.number_input("Items Count", min_value=1, value=50, step=1)

        # Calculate shopping duration
        if shop_start and shop_end:
            start_dt = datetime.combine(datetime.today(), shop_start)
            end_dt = datetime.combine(datetime.today(), shop_end)
            duration = (end_dt - start_dt).total_seconds() / 60
            st.info(f"⏱️ Shopping Duration: {int(duration)} minutes")

    # Incentives Checkbox (Expandable)
    incentives = st.checkbox("🎯 Working Toward Incentive")
    if incentives:
        col1, col2 = st.columns(2)
        with col1:
            incentive_goal = st.number_input("Goal (# of trips)", min_value=2, value=3, step=1)
        with col2:
            incentive_bonus = st.number_input("Bonus Amount ($)", min_value=0.0, value=15.0, step=5.0)

        # Progress tracker (simplified for now)
        st.progress(0.66)
        st.success(f"2 of {incentive_goal} complete - 1 more for ${incentive_bonus:.0f} bonus!")

    st.markdown("---")

    # Additional Info
    col1, col2 = st.columns(2)
    with col1:
        trip_date = st.date_input("Date", datetime.now())
    with col2:
        trip_notes = st.text_area("Notes (optional)", height=100)

    # Save Button
    if st.button("💾 Save Trip", type="primary", use_container_width=True):
        trip_data = {
            'date': trip_date.isoformat(),
            'pay': trip_pay,
            'miles': trip_miles,
            'time': trip_time,
            'stops': trip_stops,
            'net': earnings['net'] if trip_pay > 0 else 0,
            'rating': rating_type if trip_pay > 0 else 'unknown',
            'vehicle': vehicle_type,
            'shopping': shopping,
            'incentive': incentives,
            'notes': trip_notes
        }
        st.session_state.trips_data.append(trip_data)
        st.success(f"✅ Trip saved! Total trips: {len(st.session_state.trips_data)}")
        st.balloons()

def show_dashboard():
    """Dashboard with earnings overview"""
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)

    if not st.session_state.trips_data:
        st.info("No trips logged yet! Go to 'Log Trip' to get started.")
        return

    # Calculate totals
    total_gross = sum(t['pay'] for t in st.session_state.trips_data)
    total_net = sum(t['net'] for t in st.session_state.trips_data)
    total_trips = len(st.session_state.trips_data)
    avg_per_trip = total_net / total_trips if total_trips > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Gross", f"${total_gross:.2f}")
    with col2:
        st.metric("Total Net", f"${total_net:.2f}",
                 delta=f"-${total_gross - total_net:.2f} expenses")
    with col3:
        st.metric("Trips Logged", total_trips)
    with col4:
        st.metric("Avg Per Trip", f"${avg_per_trip:.2f}")

    # Recent trips table
    st.subheader("🚗 Recent Trips")
    df = pd.DataFrame(st.session_state.trips_data)
    df_display = df[['date', 'pay', 'net', 'miles', 'rating']].tail(10)
    st.dataframe(df_display, use_container_width=True)

def show_ai_insights():
    """AI-powered insights (Pro feature)"""
    st.markdown('<div class="main-header">🤖 AI Insights</div>', unsafe_allow_html=True)

    if st.session_state.user_tier != 'pro':
        st.warning("🔒 AI Insights is a Pro feature!")
        st.info("Upgrade to Pro for AI-powered recommendations")
        return

    st.success("✨ AI analyzing your trips...")

    # Sample insights
    st.subheader("💡 Your Insights")
    st.info("⏰ Your best earning window: **Saturday 3-6 PM** (+35% earnings)")
    st.info("📍 Downtown zone pays 20% more than Suburbs")
    st.warning("⚠️ Customer at 123 Main St reduced tip 3 times - consider declining")
    st.success("🎯 You're on track for $500 this week!")

def show_reports():
    """Reports and exports (Pro feature)"""
    st.markdown('<div class="main-header">📈 Reports</div>', unsafe_allow_html=True)

    if st.session_state.user_tier != 'pro':
        st.warning("🔒 Advanced Reports is a Pro feature!")
        return

    st.subheader("💼 Tax Reports")
    st.info("Export your earnings for tax season")
    if st.button("📥 Download CSV"):
        st.success("Report downloaded! (Feature in development)")

def show_community():
    """Community forum"""
    st.markdown('<div class="main-header">💬 Community</div>', unsafe_allow_html=True)

    st.subheader("🏆 This Week's Awards")
    st.success("💩 Shittiest Trip: $8 for 45 miles - shared by @driver123")
    st.success("💰 Best Tip: $50 cash tip! - shared by @sparkpro99")

    st.subheader("💬 Discussion")
    st.info("Community forum coming soon!")

def show_settings():
    """Settings page"""
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)

    st.subheader("Account")
    if st.session_state.user_email:
        st.info(f"📧 {st.session_state.user_email}")

    st.subheader("Subscription")
    if st.session_state.user_tier == 'pro':
        st.success("✅ Pro Subscriber")
    else:
        st.info("Free Tier")
        if st.button("Upgrade to Pro"):
            st.info("Redirecting to checkout...")

if __name__ == "__main__":
    main()
