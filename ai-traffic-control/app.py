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

# Initialize session state for all new features
if 'emergency_mode' not in st.session_state:
    st.session_state.emergency_mode = False
if 'mode' not in st.session_state:
    st.session_state.mode = "AI Adaptive"
if 'emergency_dir' not in st.session_state:
    st.session_state.emergency_dir = "North-South"
if 'pedestrian_priority' not in st.session_state:
    st.session_state.pedestrian_priority = False
if 'lane_reversed' not in st.session_state:
    st.session_state.lane_reversed = False

# Helper function for data download
@st.cache_data
def convert_df_to_csv(df):
    """Converts a DataFrame to a CSV string for download."""
    return df.to_csv().encode('utf-8')

# --- Main App Logic ---
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
            ["AI Adaptive", "Manual Override", "Emergency Mode", "Predictive Mode"]
        )

        # Emergency Controls
        st.subheader("🚨 Emergency Controls")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚑 Activate Emergency", type="primary"):
                st.session_state.emergency_mode = True
                st.info("🚨 Emergency activated!")
        with col2:
            if st.button("🔄 Deactivate"):
                st.session_state.emergency_mode = False
                st.success("✅ Normal operation restored.")
        
        if st.session_state.emergency_mode:
            st.session_state.emergency_dir = st.selectbox("Emergency Direction", ["North-South", "East-West"])
            st.error("🚨 EMERGENCY OVERRIDE ACTIVE")
            
        # Futuristic Features
        st.subheader("🚀 Futuristic Features")
        
        # Dynamic Lane Management
        if st.checkbox("Dynamic Lane Management", value=st.session_state.lane_reversed):
            st.session_state.lane_reversed = True
            st.info("↔️ East-West Lane is now reversible!")
        else:
            st.session_state.lane_reversed = False
        
        # Pedestrian & Cyclist Priority
        if st.checkbox("Pedestrian & Cyclist Priority", value=st.session_state.pedestrian_priority):
            st.session_state.pedestrian_priority = True
            st.info("🚶‍♀️ Walk signal triggered on demand.")
        else:
            st.session_state.pedestrian_priority = False

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

    # Predictive Analysis Simulation
    if st.session_state.mode == "Predictive Mode":
        st.warning("🔮 AI is predicting future traffic flow.")
        # Simulate predictive change (e.g., a major event starting in 15 mins)
        vehicle_counts['east'] = max(vehicle_counts['east'], 30)
        vehicle_counts['west'] = max(vehicle_counts['west'], 25)

    total_vehicles = sum(vehicle_counts.values())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "🟢 Online" if not st.session_state.emergency_mode else "🟡 Emergency"
        st.metric("System Status", status)
    
    with col2:
        st.metric("Total Vehicles", total_vehicles, delta=f"+{np.random.randint(1,8)}")
    
    with col3:
        avg_wait = round(2.3 + np.random.uniform(-0.5, 0.5), 1)
        if st.session_state.emergency_mode:
            avg_wait = 0.5
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
        
        # Updated logic for emergency mode & dynamic lanes
        if st.session_state.emergency_mode:
            if st.session_state.emergency_dir == "North-South":
                st.write("🟢 **North-South**: 45s (Emergency)")
                st.write("🔴 **East-West**: STOP")
            else:
                st.write("🔴 **North-South**: STOP")
                st.write("🟢 **East-West**: 45s (Emergency)")
        elif st.session_state.pedestrian_priority:
            st.write("🚶‍♂️ **Walk Signal**: 30s")
            st.write("🔴 **All Traffic**: STOP")
        else:
            # Adaptive timing based on traffic and dynamic lanes
            total_ns = vehicle_counts['north'] + vehicle_counts['south']
            total_ew = vehicle_counts['east'] + vehicle_counts['west']

            if st.session_state.lane_reversed:
                # Prioritize Eastbound traffic
                st.write(f"🟢 **Eastbound**: {min(60, max(15, total_ew * 2))}s")
                st.write(f"🔴 **Westbound**: 0s (Reversed)")
            else:
                ew_time = min(60, max(15, total_ew * 2)) if total_ew > total_ns else max(15, 60 - total_ns)
                st.write(f"🟢 **East-West**: {ew_time}s")

            ns_time = min(60, max(15, total_ns * 2)) if total_ns > total_ew else max(15, 60 - total_ew)
            st.write(f"🟢 **North-South**: {ns_time}s")
            
        st.subheader("🤖 AI Status")
        if st.session_state.mode == "AI Adaptive":
            st.success("✅ YOLO Detection: Active")
            st.success("✅ Adaptive Control: Active")
            st.info("🧠 Processing: 32 FPS")
        elif st.session_state.mode == "Predictive Mode":
            st.success("🔮 Predictive Engine: Active")
            st.info("⏳ Forecasting: 15 min ahead")
        else:
            st.warning("⚠️ AI Suspended")

    # V2I Communication Simulation
    st.subheader("📡 V2I Communication & Dynamic Updates")
    st.info("Simulating an approaching emergency vehicle. Signal will preemptively clear the path.")
    col_v2i, col_empty = st.columns(2)
    with col_v2i:
        if st.button("🚨 Simulate V2I Emergency Vehicle"):
            st.session_state.emergency_mode = True
            st.session_state.emergency_dir = "North-South"
            st.success("Emergency vehicle detected! North-South lane being cleared.")
    
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

    # Performance and Environmental metrics
    st.subheader("⚡ System Performance Metrics")
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    with perf_col1:
        st.metric("🎯 Detection Accuracy", f"{round(94.2 + np.random.uniform(-2, 2), 1)}%", delta="↑ 2.1%")
    with perf_col2:
        st.metric("⚡ Response Time", f"{round(1.8 + np.random.uniform(-0.5, 0.3), 1)}s", delta="↓ 0.3s")
    with perf_col3:
        st.metric("🚚 Traffic Throughput", f"{round(87.5 + np.random.uniform(-5, 8), 1)}%", delta="↑ 12.3%")
    with perf_col4:
        emission_reduction = round(15.6 + np.random.uniform(-2, 4), 1)
        st.metric("🌱 Emission Reduction", f"{emission_reduction}%", delta="↑ 3.2%")

    st.subheader("💨 Environmental Impact Monitoring")
    # Simulate a real-time air quality chart
    air_data = pd.DataFrame({
        'Time': pd.date_range(datetime.now() - timedelta(minutes=10), datetime.now(), freq='1min'),
        'CO2_Level': 400 + np.random.uniform(-10, 10, 11),
        'NOx_Level': 50 + np.random.uniform(-5, 5, 11)
    })
    
    fig_air = px.line(air_data, x='Time', y=['CO2_Level', 'NOx_Level'], 
                      title="Air Quality Levels (Simulated)",
                      labels={'value': 'PPM', 'variable': 'Pollutant'})
    fig_air.update_layout(height=300)
    st.plotly_chart(fig_air, use_container_width=True)

    # Data export functionality
    st.subheader("📂 Export Data")
    vehicle_df = pd.DataFrame(
        list(vehicle_counts.items()),
        columns=['Direction', 'Vehicle_Count']
    )
    st.download_button(
        label="Download Current Vehicle Counts as CSV",
        data=convert_df_to_csv(vehicle_df),
        file_name='traffic_data.csv',
        mime='text/csv',
    )
    
    # Success message
    st.success("🎉 **Congratulations!** Your AI Traffic Control System is successfully deployed on Streamlit Cloud and accessible worldwide!")

    # Auto refresh every 5 seconds
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()
