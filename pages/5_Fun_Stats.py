import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fun Stats", page_icon="🔮", layout="wide")
st.title("🔮 Fun Stats")
st.markdown("---")

df = pd.read_csv('data/ronaldo_goals.csv')
df['goal_minute'] = df['goal_minute'].astype(str).str.replace("'", "").str.replace("+", ".").str.strip()
df['goal_minute'] = pd.to_numeric(df['goal_minute'], errors='coerce')

# ---- Top Assist Players ----
st.subheader("🤝 Who Assists Ronaldo the Most?")
assists = df[df['assist_player'] != 'Not Applicable']['assist_player'].value_counts().head(10).reset_index()
assists.columns = ['player', 'assists']

fig1 = px.bar(
    assists,
    x='assists',
    y='player',
    orientation='h',
    color='assists',
    color_continuous_scale='Greens',
    text='assists'
)
fig1.update_traces(textposition='outside')
fig1.update_layout(coloraxis_showscale=False, yaxis_title='', xaxis_title='Assists')
st.plotly_chart(fig1, width='stretch')

st.markdown("---")

# ---- Clutch Goals (80th min+) ----
st.subheader("💪 Clutch Goals — Scored in 80th Minute or Later")
clutch = df[df['goal_minute'] >= 80]
col1, col2, col3 = st.columns(3)
col1.metric("Total Clutch Goals", len(clutch))
col2.metric("% of Career Goals", f"{round(len(clutch)/len(df)*100, 1)}%")
col3.metric("Latest Goal Minute", f"{int(df['goal_minute'].dropna().max())}'")

clutch_by_club = clutch['team'].value_counts().reset_index()
clutch_by_club.columns = ['club', 'clutch_goals']
fig2 = px.bar(
    clutch_by_club,
    x='club',
    y='clutch_goals',
    color='club',
    text='clutch_goals',
    color_discrete_sequence=['#006600', '#CC0000', '#FFD700', '#000033', '#00A86B']
)
fig2.update_traces(textposition='outside')
fig2.update_layout(showlegend=False, xaxis_title='', yaxis_title='Clutch Goals')
st.plotly_chart(fig2, width='stretch')

st.markdown("---")

# ---- Solo Run Goals ----
st.subheader("🏃 Solo Run Goals by Club")
solo = df[df['goal_method'] == 'Solo run']
solo_club = solo['team'].value_counts().reset_index()
solo_club.columns = ['club', 'goals']
fig3 = px.pie(solo_club, names='club', values='goals', hole=0.4,
              color_discrete_sequence=px.colors.qualitative.Bold)
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Solo Run Goals", len(solo))
    st.plotly_chart(fig3, width='stretch')

st.markdown("---")

# ---- Free Kick Goals ----
st.subheader("🎯 Free Kick Goals by Club")
fk = df[df['goal_method'] == 'Direct free kick']
fk_club = fk['team'].value_counts().reset_index()
fk_club.columns = ['club', 'goals']

fig4 = px.bar(
    fk_club,
    x='club',
    y='goals',
    color='club',
    text='goals',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig4.update_traces(textposition='outside')
fig4.update_layout(showlegend=False, xaxis_title='', yaxis_title='Free Kick Goals')
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Free Kick Goals", len(fk))
    st.plotly_chart(fig4, width='stretch')

st.markdown("---")

# ---- Penalty Goals ----
st.subheader("⚽ Penalty Goals by Club")
pen = df[df['goal_method'] == 'Penalty']
pen_club = pen['team'].value_counts().reset_index()
pen_club.columns = ['club', 'goals']

fig5 = px.bar(
    pen_club,
    x='club',
    y='goals',
    color='club',
    text='goals',
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig5.update_traces(textposition='outside')
fig5.update_layout(showlegend=False, xaxis_title='', yaxis_title='Penalty Goals')
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Penalty Goals", len(pen))
    st.plotly_chart(fig5, width='stretch')
