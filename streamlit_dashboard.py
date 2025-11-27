import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="National Athlete Performance Platform", layout="wide", page_icon="🏃")

@st.cache_data
def load_data():
    df = pd.read_csv('Athlete_Training_Recovery_Tracker_Dataset.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Talent_Score'] = (
        df['Performance_Score'] * 0.4 +
        (100 - df['Fatigue_Level'] * 10) * 0.2 +
        df['Recovery_Index'] * 0.2 +
        df['Nutrition_Score'] * 0.1 +
        (df['Sleep_Hours'] / 9 * 100) * 0.1
    )
    return df

@st.cache_data
def load_training_data():
    training_df = pd.read_csv('sports_training_dataset.csv')
    training_df['Date'] = pd.to_datetime(training_df['Date'])
    
    # Add calculated fields
    def categorize_heart_rate(hr):
        if hr < 120: return 'Low Intensity'
        elif hr < 140: return 'Moderate Intensity'
        elif hr < 160: return 'High Intensity'
        else: return 'Maximum Intensity'
    
    training_df['HR_Zone'] = training_df['Heart_Rate_Avg'].apply(categorize_heart_rate)
    training_df['Training_Efficiency'] = (
        (training_df['Endurance_Score'] * 0.4) +
        (training_df['Technique_Score'] * 0.4) +
        ((training_df['Distance_Covered'] / training_df['Session_Duration']) * 10 * 0.2)
    )
    training_df['Training_Load'] = (
        training_df['Session_Duration'] * 
        (training_df['Heart_Rate_Avg'] / 100) * 
        (training_df['Speed_Avg'] / 10)
    )
    training_df['Age_Group'] = pd.cut(training_df['Age'], bins=[0, 20, 23, 30], labels=['18-20', '21-23', '24+'])
    
    return training_df

def generate_training_recommendations(session_data):
    """Generate training recommendations based on session data"""
    recommendations = []
    
    if session_data['Heart_Rate_Avg'] < 120:
        recommendations.append("💓 INTENSITY: Increase training intensity")
    elif session_data['Heart_Rate_Avg'] > 170:
        recommendations.append("💓 INTENSITY: Reduce intensity - risk of overexertion")
    
    if session_data['Endurance_Score'] < 60:
        recommendations.append("🏃 ENDURANCE: Focus on aerobic capacity")
    elif session_data['Endurance_Score'] > 90:
        recommendations.append("🏃 ENDURANCE: Excellent - maintain program")
    
    if session_data['Technique_Score'] < 60:
        recommendations.append("🎯 TECHNIQUE: Prioritize skill development")
    elif session_data['Technique_Score'] > 85:
        recommendations.append("🎯 TECHNIQUE: Advanced level achieved")
    
    if session_data['Session_Duration'] < 30:
        recommendations.append("⏱️ DURATION: Extend session length")
    elif session_data['Session_Duration'] > 90:
        recommendations.append("⏱️ DURATION: Consider shorter, intense sessions")
    
    if session_data['Performance_Level'] == 'Needs Improvement':
        recommendations.append("📈 PERFORMANCE: Implement progression plan")
    
    return recommendations

def generate_recommendations(athlete_data):
    recommendations = []
    if athlete_data['Fatigue_Level'] >= 8:
        recommendations.append("🔴 HIGH FATIGUE: Reduce training intensity by 30%")
    elif athlete_data['Fatigue_Level'] >= 6:
        recommendations.append("🟡 MODERATE FATIGUE: Add recovery sessions")
    else:
        recommendations.append("🟢 LOW FATIGUE: Can increase intensity by 10-15%")
    
    if athlete_data['Sleep_Hours'] < 7:
        recommendations.append("😴 SLEEP: Increase to 8-9 hours")
    if athlete_data['Nutrition_Score'] < 70:
        recommendations.append("🍎 NUTRITION: Consult sports nutritionist")
    if athlete_data['Recovery_Index'] < 60:
        recommendations.append("🔄 RECOVERY: Add recovery sessions")
    if athlete_data['Injury_Risk'] == 'High':
        recommendations.append("⚠️ INJURY RISK: Medical assessment required")
    
    return recommendations

# Load data
df = load_data()
training_df = load_training_data()

# Header
st.title("🏃 National Athlete Performance Data Platform")
st.markdown("*Centralized digital platform for athlete development, monitoring, and talent identification*")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Injury Prevention", "Talent Identification", "Athlete Profiles", "Training Analysis"])

if page == "Dashboard":
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Athletes", f"{df['Athlete_ID'].nunique():,}")
    with col2:
        st.metric("Sports Disciplines", df['Sport_Type'].nunique())
    with col3:
        st.metric("Avg Performance", f"{df['Performance_Score'].mean():.1f}/100")
    with col4:
        high_risk = df[df['Injury_Risk'] == 'High']['Athlete_ID'].nunique()
        st.metric("High-Risk Athletes", f"{high_risk} ({high_risk/df['Athlete_ID'].nunique()*100:.1f}%)")
    
    # Performance trends
    st.subheader("📈 Performance Trends")
    monthly_perf = df.groupby([df['Date'].dt.to_period('M'), 'Sport_Type'])['Performance_Score'].mean().reset_index()
    monthly_perf['Month'] = monthly_perf['Date'].astype(str)
    
    fig = px.line(monthly_perf, x='Month', y='Performance_Score', color='Sport_Type',
                  title="Average Performance by Sport Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Sport distribution
    col1, col2 = st.columns(2)
    with col1:
        sport_counts = df['Sport_Type'].value_counts()
        fig = px.pie(values=sport_counts.values, names=sport_counts.index, title="Athletes by Sport")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        avg_by_sport = df.groupby('Sport_Type')['Performance_Score'].mean().sort_values(ascending=True)
        fig = px.bar(x=avg_by_sport.values, y=avg_by_sport.index, orientation='h',
                     title="Average Performance by Sport")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Injury Prevention":
    st.header("🏥 Injury Risk Assessment & Prevention")
    
    # Risk distribution
    col1, col2 = st.columns(2)
    
    with col1:
        risk_counts = df['Injury_Risk'].value_counts()
        colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
        fig = px.pie(values=risk_counts.values, names=risk_counts.index, 
                     title="Overall Injury Risk Distribution",
                     color=risk_counts.index, color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        risk_by_sport = df.groupby(['Sport_Type', 'Injury_Risk']).size().reset_index(name='Count')
        fig = px.bar(risk_by_sport, x='Sport_Type', y='Count', color='Injury_Risk',
                     title="Injury Risk by Sport", color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk factors analysis
    st.subheader("Risk Factors Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(df, x='Fatigue_Level', y='Performance_Score', color='Injury_Risk',
                        title="Fatigue vs Performance", color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(df, x='Injury_Risk', y='Sleep_Hours', 
                     title="Sleep Hours by Risk Level", color='Injury_Risk',
                     color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    # High-risk athletes
    st.subheader("⚠️ High-Risk Athletes Requiring Attention")
    high_risk_athletes = df[df['Injury_Risk'] == 'High'][['Athlete_ID', 'Sport_Type', 'Fatigue_Level', 'Sleep_Hours', 'Recovery_Index']].head(10)
    st.dataframe(high_risk_athletes, use_container_width=True)

elif page == "Talent Identification":
    st.header("🌟 Talent Identification System")
    
    # Top talents
    st.subheader("Top Talents by Sport")
    selected_sport = st.selectbox("Select Sport", df['Sport_Type'].unique())
    
    sport_data = df[df['Sport_Type'] == selected_sport]
    top_talents = sport_data.nlargest(5, 'Talent_Score')[['Athlete_ID', 'Talent_Score', 'Performance_Score', 'Injury_Risk']]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(top_talents, use_container_width=True)
    
    with col2:
        fig = px.scatter(sport_data, x='Performance_Score', y='Talent_Score', 
                        color='Injury_Risk', size='Recovery_Index',
                        title=f"Talent vs Performance - {selected_sport}",
                        color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Talent distribution
    st.subheader("Talent Score Distribution")
    fig = px.box(df, x='Sport_Type', y='Talent_Score', title="Talent Score by Sport")
    fig.update_xaxis(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Elite athletes (top 10%)
    elite_threshold = df['Talent_Score'].quantile(0.9)
    elite_athletes = df[df['Talent_Score'] >= elite_threshold]
    
    st.subheader(f"🏆 Elite Athletes (Top 10% - Score ≥ {elite_threshold:.1f})")
    elite_summary = elite_athletes.groupby('Sport_Type').size().reset_index(name='Elite_Count')
    
    fig = px.bar(elite_summary, x='Sport_Type', y='Elite_Count', 
                 title="Elite Athletes by Sport")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Athlete Profiles":
    st.header("👤 Individual Athlete Profiles")
    
    # Athlete selection
    selected_athlete = st.selectbox("Select Athlete", df['Athlete_ID'].unique())
    athlete_data = df[df['Athlete_ID'] == selected_athlete].iloc[-1]
    
    # Profile overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Sport", athlete_data['Sport_Type'])
        st.metric("Performance Score", f"{athlete_data['Performance_Score']}/100")
        st.metric("Talent Score", f"{athlete_data['Talent_Score']:.1f}/100")
    
    with col2:
        st.metric("Injury Risk", athlete_data['Injury_Risk'])
        st.metric("Fatigue Level", f"{athlete_data['Fatigue_Level']}/10")
        st.metric("Recovery Index", f"{athlete_data['Recovery_Index']}/100")
    
    with col3:
        st.metric("Training Hours", f"{athlete_data['Training_Hours']:.1f}h")
        st.metric("Sleep Hours", f"{athlete_data['Sleep_Hours']:.1f}h")
        st.metric("Nutrition Score", f"{athlete_data['Nutrition_Score']}/100")
    
    # Performance radar chart
    st.subheader("Performance Profile")
    categories = ['Performance', 'Recovery', 'Nutrition', 'Sleep Quality', 'Training Load']
    values = [
        athlete_data['Performance_Score'],
        athlete_data['Recovery_Index'],
        athlete_data['Nutrition_Score'],
        (athlete_data['Sleep_Hours'] / 9) * 100,
        (athlete_data['Training_Hours'] / 6) * 100
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=selected_athlete
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Athlete Performance Radar"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("🎯 Personalized Recommendations")
    recommendations = generate_recommendations(athlete_data)
    for rec in recommendations:
        st.write(f"• {rec}")
    
    # Historical performance
    athlete_history = df[df['Athlete_ID'] == selected_athlete].sort_values('Date')
    if len(athlete_history) > 1:
        st.subheader("📊 Performance History")
        fig = px.line(athlete_history, x='Date', y='Performance_Score', 
                     title=f"Performance Trend - {selected_athlete}")
        st.plotly_chart(fig, use_container_width=True)
    
    # Ranking
    sport_athletes = df[df['Sport_Type'] == athlete_data['Sport_Type']]
    performance_rank = (sport_athletes['Performance_Score'] < athlete_data['Performance_Score']).sum() + 1
    total_in_sport = len(sport_athletes['Athlete_ID'].unique())
    percentile = ((total_in_sport - performance_rank) / total_in_sport * 100)
    
    st.subheader("🏆 Rankings")
    st.write(f"**Performance Rank in {athlete_data['Sport_Type']}:** {performance_rank}/{total_in_sport}")
    st.write(f"**Percentile:** {percentile:.1f}%")

elif page == "Training Analysis":
    st.header("🏋️ Advanced Training Session Analysis")
    
    # Training KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sessions", f"{len(training_df):,}")
    with col2:
        st.metric("Athletes in Training", training_df['Athlete_ID'].nunique())
    with col3:
        st.metric("Avg Session Duration", f"{training_df['Session_Duration'].mean():.0f} min")
    with col4:
        st.metric("Avg Heart Rate", f"{training_df['Heart_Rate_Avg'].mean():.0f} bpm")
    
    # Interactive filters
    st.subheader("📊 Interactive Training Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_sport_training = st.selectbox("Select Sport (Training)", ['All'] + list(training_df['Sport_Type'].unique()))
    with col2:
        selected_performance = st.selectbox("Performance Level", ['All'] + list(training_df['Performance_Level'].unique()))
    with col3:
        selected_gender = st.selectbox("Gender", ['All'] + list(training_df['Gender'].unique()))
    
    # Filter data
    filtered_training = training_df.copy()
    if selected_sport_training != 'All':
        filtered_training = filtered_training[filtered_training['Sport_Type'] == selected_sport_training]
    if selected_performance != 'All':
        filtered_training = filtered_training[filtered_training['Performance_Level'] == selected_performance]
    if selected_gender != 'All':
        filtered_training = filtered_training[filtered_training['Gender'] == selected_gender]
    
    # Training intensity analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Heart rate zones
        hr_zone_counts = filtered_training['HR_Zone'].value_counts()
        fig = px.pie(values=hr_zone_counts.values, names=hr_zone_counts.index, 
                     title="Training Intensity Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Performance level distribution
        perf_counts = filtered_training['Performance_Level'].value_counts()
        colors = {'Excellent': 'green', 'Average': 'orange', 'Needs Improvement': 'red'}
        fig = px.bar(x=perf_counts.index, y=perf_counts.values, 
                     title="Performance Level Distribution",
                     color=perf_counts.index, color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    # Training efficiency analysis
    st.subheader("⚡ Training Efficiency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(filtered_training, x='Endurance_Score', y='Technique_Score', 
                        color='Performance_Level', size='Training_Efficiency',
                        title="Endurance vs Technique (Size = Efficiency)",
                        color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(filtered_training, x='Sport_Type', y='Training_Efficiency', 
                     title="Training Efficiency by Sport")
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top performers
    st.subheader("🏆 Top Training Performances")
    top_sessions = filtered_training.nlargest(10, 'Training_Efficiency')
    st.dataframe(top_sessions[['Athlete_ID', 'Sport_Type', 'Training_Efficiency', 'Endurance_Score', 'Technique_Score', 'Performance_Level']], use_container_width=True)
    
    # Training load management
    st.subheader("📈 Training Load Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(filtered_training, x='Training_Load', nbins=20, 
                          title="Training Load Distribution")
        high_load_threshold = filtered_training['Training_Load'].quantile(0.9)
        fig.add_vline(x=high_load_threshold, line_dash="dash", line_color="red", 
                     annotation_text=f"High Load Threshold ({high_load_threshold:.1f})")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        sport_load = filtered_training.groupby('Sport_Type')['Training_Load'].mean().sort_values(ascending=True)
        fig = px.bar(x=sport_load.values, y=sport_load.index, orientation='h',
                     title="Average Training Load by Sport")
        st.plotly_chart(fig, use_container_width=True)
    
    # Individual session analysis
    st.subheader("🔍 Individual Session Analysis")
    
    selected_athlete_training = st.selectbox("Select Athlete for Session Analysis", 
                                           filtered_training['Athlete_ID'].unique())
    
    athlete_sessions = filtered_training[filtered_training['Athlete_ID'] == selected_athlete_training]
    
    if len(athlete_sessions) > 0:
        latest_session = athlete_sessions.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Latest Performance", latest_session['Performance_Level'])
            st.metric("Heart Rate", f"{latest_session['Heart_Rate_Avg']:.0f} bpm")
            st.metric("Session Duration", f"{latest_session['Session_Duration']:.0f} min")
        
        with col2:
            st.metric("Endurance Score", f"{latest_session['Endurance_Score']:.1f}/100")
            st.metric("Technique Score", f"{latest_session['Technique_Score']:.1f}/100")
            st.metric("Training Efficiency", f"{latest_session['Training_Efficiency']:.1f}")
        
        with col3:
            st.metric("Average Speed", f"{latest_session['Speed_Avg']:.1f} m/s")
            st.metric("Distance Covered", f"{latest_session['Distance_Covered']:.0f} m")
            st.metric("Training Load", f"{latest_session['Training_Load']:.1f}")
        
        # Session recommendations
        st.subheader("💡 Training Recommendations")
        recommendations = generate_training_recommendations(latest_session)
        for rec in recommendations:
            st.write(f"• {rec}")
        
        # Athlete's session history
        if len(athlete_sessions) > 1:
            st.subheader("📊 Session History")
            fig = px.line(athlete_sessions, x='Date', y=['Endurance_Score', 'Technique_Score'], 
                         title=f"Performance Trends - Athlete {selected_athlete_training}")
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**National Athlete Performance Data Platform** - Empowering sports excellence through data-driven insights")