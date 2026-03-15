import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Career Overview", page_icon="📊", layout="wide")
st.title("📊 Career Overview")
st.markdown("---")

df = pd.read_csv('data/ronaldo_goals.csv')

# clean goal_minute
df['goal_minute'] = df['goal_minute'].astype(str).str.replace("'", "").str.replace("+", ".").str.strip()
df['goal_minute'] = pd.to_numeric(df['goal_minute'], errors='coerce')

# ---- Goals by Club ----
st.subheader("🏟️ Goals by Club")
club_goals = df['team'].value_counts().reset_index()
club_goals.columns = ['club', 'goals']
club_order = ['Sporting CP', 'Manchester United', 'Real Madrid', 'Juventus FC', 'Al-Nassr FC']
club_goals['club'] = pd.Categorical(club_goals['club'], categories=club_order, ordered=True)
club_goals = club_goals.sort_values('club')

fig1 = px.bar(
    club_goals,
    x='club',
    y='goals',
    color='club',
    text='goals',
    color_discrete_sequence=['#006600', '#CC0000', '#FFD700', '#000033', '#FFD700'],
)
fig1.update_traces(textposition='outside')
fig1.update_layout(showlegend=False, xaxis_title='', yaxis_title='Goals')
st.plotly_chart(fig1, width='stretch')

st.markdown("---")

# ---- Goals per Season ----
st.subheader("📅 Goals per Season")
season_goals = df['season'].value_counts().reset_index()
season_goals.columns = ['season', 'goals']
season_goals = season_goals.sort_values('season')

fig2 = px.line(
    season_goals,
    x='season',
    y='goals',
    markers=True,
    color_discrete_sequence=['#FFD700']
)
fig2.update_layout(xaxis_tickangle=-45, xaxis_title='Season', yaxis_title='Goals')
st.plotly_chart(fig2, width='stretch')

st.markdown("---")

col1, col2 = st.columns(2)

# ---- Home vs Away ----
with col1:
    st.subheader("🏠 Home vs Away")
    home_away = df['home_away'].value_counts().reset_index()
    home_away.columns = ['type', 'goals']
    fig3 = px.pie(
        home_away,
        names='type',
        values='goals',
        color_discrete_sequence=['#1DB954', '#FF4444'],
        hole=0.4
    )
    st.plotly_chart(fig3, width='stretch')

# ---- Goals by Position ----
with col2:
    st.subheader("🧍 Goals by Position")
    pos_goals = df['player_position'].value_counts().reset_index()
    pos_goals.columns = ['position', 'goals']
    fig4 = px.bar(
        pos_goals,
        x='goals',
        y='position',
        orientation='h',
        color='goals',
        color_continuous_scale='Reds',
        text='goals'
    )
    fig4.update_traces(textposition='outside')
    fig4.update_layout(coloraxis_showscale=False, yaxis_title='', xaxis_title='Goals')
    st.plotly_chart(fig4, width='stretch')
