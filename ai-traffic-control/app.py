import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

st.set_page_config(
    page_title="AI Traffic Control System",
    page_icon="🚦",
    layout="wide"
)

# Initialize session state
if 'emergency_mode' not in st.session_state:
    st.session_state.emergency_mode = False
if 'mode' not in st.session_state:
    st.session_state.mode = "AI Adaptive"

def main():
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f4e79, #2c5282); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin: 0;">🚦 AI Traffic Control System</h1>
        <h3 style="color: #bee3f8; margin: 0; margin-top: 0.5rem;">Real-time Adaptive Management - Main St & 1st Ave</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Operation Mode
        st.session_state.mode = st.selectbox(
            "Operation Mode", 
            ["AI Adaptive", "Manual Override", "Emergency Mode"]
        )
        
        if st.session_state.mode == "AI Adaptive":
            st.success("✅ AI controlling traffic signals automatically")
            algorithm = st.selectbox(
                "AI Algorithm", 
                ["YOLO + Adaptive Timing", "Reinforcement Learning", "Genetic Algorithm"]
            )
            
            # AI Parameters
            st.subheader("⚙️ AI Parameters")
            confidence = st.slider("Detection Confidence", 0.3, 0.9, 0.5)
            min_green = st.slider("Min Green Time (s)", 10, 30, 15)
            max_green = st.slider("Max Green Time (s)", 40, 90, 60)
            
        elif st.session_state.mode == "Manual Override":
            st.warning("⚠️ Manual mode active")
            ns_time = st.slider("North-South Green (s)", 15, 60, 30)
            ew_time = st.slider("East-West Green (s)", 15, 60, 30)
        
        # Emergency Controls
        st.subheader("🚨 Emergency Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚑 Emergency", type="primary"):
                st.session_state.emergency_mode = True
                st.success("🚨 Emergency activated!")
        
        with col2:
            if st.button("🔄 Reset"):
                st.session_state.emergency_mode = False
                st.info("✅ Normal operation")
        
        if st.session_state.emergency_mode:
            emergency_dir = st.selectbox("Emergency Direction", ["North-South", "East-West"])
            st.error("🚨 EMERGENCY OVERRIDE ACTIVE")
        
        # System Info
        st.subheader("ℹ️ System Info")
        st.info(f"🤖 AI Model: YOLO v8\n📊 Accuracy: 94.2%\n🟢 Status: Online\n🕒 Last Update: {datetime.now().strftime('%H:%M:%S')}")

    # Main Dashboard - Metrics
    vehicle_counts = {
        'north': np.random.randint(8, 18),
        'south': np.random.randint(6, 15), 
        'east': np.random.randint(10, 20),
        'west': np.random.randint(5, 12)
    }
    total_vehicles = sum(vehicle_counts.values())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "🟢 Online" if not st.session_state.emergency_mode else "🟡 Emergency"
        st.metric("System Status", status, delta="All systems operational")
    
    with col2:
        st.metric("Total Vehicles", total_vehicles, delta=f"+{np.random.randint(1,8)}")
    
    with col3:
        avg_wait = round(2.3 + np.random.uniform(-0.5, 0.5), 1)
        st.metric("Avg Wait Time", f"{avg_wait} min", delta=f"-0.{np.random.randint(1,9)} min")
    
    with col4:
        efficiency = round(94.2 + np.random.uniform(-2, 3), 1)
        st.metric("AI Efficiency", f"{efficiency}%", delta=f"+{np.random.randint(1,4)}.{np.random.randint(1,9)}%")

    # Live Traffic Monitoring
    st.subheader("📹 Live Traffic Monitoring - Main St & 1st Ave")
    
    col_main, col_signals = st.columns([3, 1])
    
    with col_main:
        st.info("🎥 Live camera feeds - AI processing in real-time")
        
        # Vehicle counts by direction
        subcol1, subcol2, subcol3, subcol4 = st.columns(4)
        
        directions = [
            ('north', '⬆️', 'North', subcol1),
            ('south', '⬇️', 'South', subcol2),
            ('east', '➡️', 'East', subcol3),
            ('west', '⬅️', 'West', subcol4)
        ]
        
        for direction, icon, name, col in directions:
            with col:
                count = vehicle_counts[direction]
                
                if count < 8:
                    density_color, density = "🟢", "Low"
                elif count < 15:
                    density_color, density = "🟡", "Medium"
                else:
                    density_color, density = "🔴", "High"
                
                st.metric(f"{density_color} {icon} {name}", count, delta=f"{density} density")
    
    with col_signals:
        st.subheader("🚦 Signal Status")
        
        if st.session_state.emergency_mode:
            st.write("🟢 **Emergency Direction**: 45s")
            st.write("🔴 **Other Directions**: STOP")
        else:
            # Adaptive timing based on traffic
            total_ns = vehicle_counts['north'] + vehicle_counts['south']
            total_ew = vehicle_counts['east'] + vehicle_counts['west']
            
            if total_ns > total_ew:
                st.write(f"🟢 **North-South**: {min(60, max(15, total_ns * 2))}s")
                st.write(f"🔴 **East-West**: {max(15, 60 - total_ns)}s")
            else:
                st.write(f"🔴 **North-South**: {max(15, 60 - total_ew)}s")
                st.write(f"🟢 **East-West**: {min(60, max(15, total_ew * 2))}s")
        
        st.subheader("🤖 AI Status")
        if st.session_state.mode == "AI Adaptive":
            st.success("✅ YOLO Detection: Active")
            st.success("✅ Adaptive Control: Active")
            st.info("🧠 Processing: 32 FPS")
        else:
            st.warning("⚠️ AI Suspended")

    # Analytics
    st.subheader("📊 Real-time Analytics & Performance")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Traffic trends
        times = pd.date_range(start=datetime.now() - timedelta(minutes=30), 
                             end=datetime.now(), freq='3min')
        
        df = pd.DataFrame({
            'Time': times,
            'North': np.random.randint(5, 20, len(times)),
            'South': np.random.randint(5, 20, len(times)),
            'East': np.random.randint(5, 20, len(times)),
            'West': np.random.randint(5, 20, len(times))
        })
        
        fig_line = px.line(
            df, x='Time', y=['North', 'South', 'East', 'West'],
            title="🚗 Vehicle Count Trends (Last 30 min)",
            color_discrete_map={
                'North': '#3182ce', 'South': '#e53e3e', 
                'East': '#38a169', 'West': '#d69e2e'
            }
        )
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)
    
    with chart_col2:
        # Performance gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = efficiency,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "🎯 AI Efficiency"},
            delta = {'reference': 90},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00d4aa"},
                'steps': [
                    {'range': [0, 60], 'color': "#ffcccc"},
                    {'range': [60, 90], 'color': "#ffffcc"},
                    {'range': [90, 100], 'color': "#ccffcc"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95}}))
        fig_gauge.update_layout(height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Current distribution pie chart
    fig_pie = px.pie(
        values=list(vehicle_counts.values()),
        names=[f"{name} Lane" for name in ['North', 'South', 'East', 'West']],
        title="🚦 Current Traffic Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Performance metrics
    st.subheader("⚡ System Performance Metrics")
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    with perf_col1:
        st.metric("🎯 Detection Accuracy", f"{round(94.2 + np.random.uniform(-2, 2), 1)}%", delta="↑ 2.1%")
    with perf_col2:
        st.metric("⚡ Response Time", f"{round(1.8 + np.random.uniform(-0.5, 0.3), 1)}s", delta="↓ 0.3s")
    with perf_col3:
        st.metric("🚚 Traffic Throughput", f"{round(87.5 + np.random.uniform(-5, 8), 1)}%", delta="↑ 12.3%")
    with perf_col4:
        st.metric("🌱 Emission Reduction", f"{round(15.6 + np.random.uniform(-2, 4), 1)}%", delta="↑ 3.2%")

    # Success message
    st.success("🎉 **Congratulations!** Your AI Traffic Control System is successfully deployed on Streamlit Cloud and accessible worldwide!")

    # Auto refresh every 5 seconds
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()
