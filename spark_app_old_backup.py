#!/usr/bin/env python3
"""
Spark Driver Tracker - Revenue Engine
Streamlit app with free/pro tier paywall
Built by Chlo - SavvyTech Automations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from stripe_integration import SparkPaymentProcessor

# Page config
st.set_page_config(
    page_title="Spark Driver Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_tier' not in st.session_state:
    st.session_state.user_tier = 'free'  # Default to free tier
if 'trips_logged' not in st.session_state:
    st.session_state.trips_logged = 0
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Initialize payment processor
payment_processor = SparkPaymentProcessor()

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
    .subheader {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .pro-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .free-badge {
        background: #28A745;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .paywall {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #004C91;
    }
</style>
""", unsafe_allow_html=True)

def check_tier_access(feature: str) -> bool:
    """Check if user has access to a feature based on tier"""
    pro_features = [
        'zone_analytics',
        'goal_tracking',
        'tax_export',
        'unlimited_trips',
        'advanced_charts'
    ]

    if feature in pro_features and st.session_state.user_tier == 'free':
        return False
    return True

def show_upgrade_prompt(feature_name: str):
    """Show upgrade prompt for Pro feature"""
    st.markdown(f"""
    <div class="paywall">
        <h2>🔒 {feature_name} is a Pro Feature</h2>
        <p>Upgrade to Spark Pro for just $12/month to unlock:</p>
        <ul style="text-align: left; display: inline-block;">
            <li>Unlimited trip tracking</li>
            <li>Zone heat maps & analytics</li>
            <li>Goal setting & tracking</li>
            <li>Tax-ready exports</li>
            <li>Priority support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.user_email:
        if st.button("⚡ Upgrade to Pro - $12/month", use_container_width=True):
            result = payment_processor.create_checkout_session(
                customer_email=st.session_state.user_email,
                tier="pro"
            )
            if result['success']:
                st.markdown(f"[Click here to complete payment]({result['checkout_url']})")
            else:
                st.error(f"Error: {result['error']}")
    else:
        st.warning("Enter your email in the sidebar to upgrade")

def main():
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="main-header">⚡ Spark</div>', unsafe_allow_html=True)

        # User tier badge
        if st.session_state.user_tier == 'pro':
            st.markdown('<span class="pro-badge">PRO USER</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="free-badge">FREE TIER</span>', unsafe_allow_html=True)

        st.markdown("---")

        # Email capture (for free users)
        if not st.session_state.user_email:
            st.subheader("📧 Get Started")
            email = st.text_input("Email Address", placeholder="driver@example.com")
            if st.button("Save", use_container_width=True):
                if email and '@' in email:
                    st.session_state.user_email = email
                    st.success("✅ Email saved!")
                    st.rerun()
                else:
                    st.error("Please enter a valid email")

        # Navigation
        st.subheader("📊 Navigation")
        page = st.radio(
            "Go to:",
            ["Dashboard", "Log Trip", "Analytics", "Goals", "Settings"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Upgrade CTA (for free users)
        if st.session_state.user_tier == 'free':
            st.info(f"**Free Tier:** {st.session_state.trips_logged}/50 trips logged")
            if st.session_state.user_email:
                if st.button("⚡ Upgrade to Pro", use_container_width=True, type="primary"):
                    result = payment_processor.create_checkout_session(
                        customer_email=st.session_state.user_email,
                        tier="pro"
                    )
                    if result['success']:
                        st.markdown(f"[Complete payment here]({result['checkout_url']})")

    # Main content area
    if page == "Dashboard":
        show_dashboard()
    elif page == "Log Trip":
        show_log_trip()
    elif page == "Analytics":
        show_analytics()
    elif page == "Goals":
        show_goals()
    elif page == "Settings":
        show_settings()

def show_dashboard():
    """Main dashboard view"""
    st.markdown('<div class="main-header">Track Every Trip. Maximize Every Dollar.</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Your delivery earnings, simplified.</div>', unsafe_allow_html=True)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Earnings", "$1,247.50", "+$142 this week")
    with col2:
        st.metric("Trips Logged", "127", "+23 this week")
    with col3:
        st.metric("Avg Per Trip", "$9.82", "+$0.45")
    with col4:
        st.metric("This Month", "$847.20", "68% of goal")

    # Earnings chart
    st.subheader("📈 Earnings Over Time")

    # Sample data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    earnings = [15 + i * 2 + (i % 7) * 10 for i in range(30)]

    df = pd.DataFrame({'Date': dates, 'Earnings': earnings})

    fig = px.line(df, x='Date', y='Earnings', title='Daily Earnings')
    fig.update_traces(line_color='#004C91', line_width=3)
    fig.update_layout(hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    # Recent trips
    st.subheader("🚗 Recent Trips")
    recent_trips = pd.DataFrame({
        'Time': ['2:45 PM', '1:20 PM', '11:30 AM'],
        'Distance': ['3.2 mi', '5.1 mi', '2.8 mi'],
        'Earnings': ['$12.50', '$18.75', '$9.25'],
        'Zone': ['Downtown', 'Suburbs', 'Airport']
    })
    st.dataframe(recent_trips, use_container_width=True, hide_index=True)

def show_log_trip():
    """Trip logging interface"""
    st.header("📝 Log New Trip")

    # Free tier limit
    if st.session_state.user_tier == 'free' and st.session_state.trips_logged >= 50:
        st.error("❌ Free tier limit reached (50 trips)")
        show_upgrade_prompt("Unlimited Trip Logging")
        return

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date", datetime.now())
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")

    with col2:
        distance = st.number_input("Distance (miles)", min_value=0.0, step=0.1)
        earnings = st.number_input("Earnings ($)", min_value=0.0, step=0.5)
        zone = st.selectbox("Zone", ["Downtown", "Suburbs", "Airport", "University", "Other"])

    notes = st.text_area("Notes (optional)")

    if st.button("💾 Save Trip", type="primary", use_container_width=True):
        st.session_state.trips_logged += 1
        st.success(f"✅ Trip logged! Total: {st.session_state.trips_logged}")
        st.balloons()

def show_analytics():
    """Analytics and insights (Pro feature)"""
    st.header("📊 Advanced Analytics")

    if not check_tier_access('zone_analytics'):
        show_upgrade_prompt("Zone Analytics & Heat Maps")
        return

    # Zone performance
    st.subheader("🗺️ Zone Performance")

    zone_data = pd.DataFrame({
        'Zone': ['Downtown', 'Suburbs', 'Airport', 'University'],
        'Trips': [45, 32, 18, 27],
        'Avg Earnings': [12.50, 9.80, 15.20, 8.90],
        'Best Time': ['Lunch', 'Dinner', 'Morning', 'Afternoon']
    })

    fig = px.bar(zone_data, x='Zone', y='Avg Earnings', title='Average Earnings by Zone', color='Avg Earnings')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(zone_data, use_container_width=True, hide_index=True)

def show_goals():
    """Goal tracking (Pro feature)"""
    st.header("🎯 Goals & Targets")

    if not check_tier_access('goal_tracking'):
        show_upgrade_prompt("Goal Setting & Tracking")
        return

    st.subheader("📈 Monthly Goal Progress")

    goal = 1200
    current = 847.20
    progress = (current / goal) * 100

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        delta={'reference': goal},
        title={'text': "Monthly Earnings Goal"},
        gauge={
            'axis': {'range': [None, goal]},
            'bar': {'color': "#004C91"},
            'steps': [
                {'range': [0, goal*0.5], 'color': "lightgray"},
                {'range': [goal*0.5, goal*0.8], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': goal
            }
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.success(f"You're at {progress:.1f}% of your monthly goal!")

def show_settings():
    """Settings and account management"""
    st.header("⚙️ Settings")

    st.subheader("Account Information")
    if st.session_state.user_email:
        st.info(f"📧 Email: {st.session_state.user_email}")
    else:
        st.warning("No email on file")

    st.subheader("Subscription")
    if st.session_state.user_tier == 'pro':
        st.success("✅ Pro Subscriber")
        # TODO: Add customer portal link
    else:
        st.info("Free Tier User")
        if st.session_state.user_email:
            if st.button("Upgrade to Pro"):
                result = payment_processor.create_checkout_session(
                    customer_email=st.session_state.user_email,
                    tier="pro"
                )
                if result['success']:
                    st.markdown(f"[Complete payment]({result['checkout_url']})")

    st.markdown("---")

    st.subheader("Export Data")
    if check_tier_access('tax_export'):
        if st.button("📥 Export for Taxes (CSV)", use_container_width=True):
            # TODO: Generate CSV export
            st.success("Export ready! (feature coming soon)")
    else:
        show_upgrade_prompt("Tax Export")

if __name__ == "__main__":
    main()
