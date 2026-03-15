import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Season by Season", page_icon="📅", layout="wide")
st.title("📅 Season by Season")
st.markdown("---")

df = pd.read_csv('data/ronaldo_goals.csv')

# ---- Goals per Season with Club ----
st.subheader("📈 Goals per Season by Club")
season_club = df.groupby(['season', 'team']).size().reset_index(name='goals')

fig1 = px.bar(
    season_club,
    x='season',
    y='goals',
    color='team',
    barmode='stack',
    color_discrete_map={
        'Sporting CP': '#006600',
        'Manchester United': '#CC0000',
        'Real Madrid': '#FFD700',
        'Juventus FC': '#000033',
        'Al-Nassr FC': '#00A86B'
    }
)
fig1.update_layout(xaxis_tickangle=-45, xaxis_title='Season', yaxis_title='Goals', legend_title='Club')
st.plotly_chart(fig1, width='stretch')

st.markdown("---")

# ---- Best and Worst Seasons ----
season_totals = df['season'].value_counts().reset_index()
season_totals.columns = ['season', 'goals']
best = season_totals.loc[season_totals['goals'].idxmax()]
worst = season_totals.loc[season_totals['goals'].idxmin()]

col1, col2 = st.columns(2)
col1.success(f"🏆 Best Season: **{best['season']}** — {best['goals']} goals")
col2.warning(f"📉 Worst Season: **{worst['season']}** — {worst['goals']} goals")

st.markdown("---")

# ---- Decade Comparison ----
st.subheader("🕐 Goals by Decade")
decade_goals = df['goal_decade'].value_counts().reset_index()
decade_goals.columns = ['decade', 'goals']
decade_goals = decade_goals.sort_values('decade')

fig2 = px.bar(
    decade_goals,
    x='decade',
    y='goals',
    color='decade',
    text='goals',
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig2.update_traces(textposition='outside')
fig2.update_layout(showlegend=False, xaxis_title='Decade', yaxis_title='Goals')
st.plotly_chart(fig2, width='stretch')

st.markdown("---")

# ---- Season Explorer ----
st.subheader("🔍 Explore a Season")
selected_season = st.selectbox("Select Season", sorted(df['season'].unique()))
filtered = df[df['season'] == selected_season]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Goals", len(filtered))
col2.metric("Club", filtered['team'].mode()[0])
col3.metric("Top Method", filtered['goal_method'].mode()[0])
col4.metric("Home Goals", len(filtered[filtered['home_away'] == 'Home']))

comp_season = filtered['competition'].value_counts().reset_index()
comp_season.columns = ['competition', 'goals']
fig3 = px.pie(comp_season, names='competition', values='goals', hole=0.4,
              color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig3, width='stretch')
