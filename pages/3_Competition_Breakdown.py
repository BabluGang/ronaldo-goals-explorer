import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Competition Breakdown", page_icon="🏆", layout="wide")
st.title("🏆 Competition Breakdown")
st.markdown("---")

df = pd.read_csv('data/ronaldo_goals.csv')
df['competition'] = df['competition'].str.strip()

# ---- Goals by Competition ----
st.subheader("🌍 Goals by Competition")
comp_goals = df['competition'].value_counts().reset_index()
comp_goals.columns = ['competition', 'goals']

fig1 = px.bar(
    comp_goals,
    x='goals',
    y='competition',
    orientation='h',
    color='goals',
    color_continuous_scale='Blues',
    text='goals'
)
fig1.update_traces(textposition='outside')
fig1.update_layout(coloraxis_showscale=False, yaxis_title='', xaxis_title='Goals', height=600)
st.plotly_chart(fig1, width='stretch')

st.markdown("---")

# ---- Top Opponents ----
st.subheader("😤 Top Opponents — Who Has He Scored Most Against?")
top_opponents = df['opponent'].value_counts().head(15).reset_index()
top_opponents.columns = ['opponent', 'goals']

fig2 = px.bar(
    top_opponents,
    x='goals',
    y='opponent',
    orientation='h',
    color='goals',
    color_continuous_scale='Reds',
    text='goals'
)
fig2.update_traces(textposition='outside')
fig2.update_layout(coloraxis_showscale=False, yaxis_title='', xaxis_title='Goals', height=500)
st.plotly_chart(fig2, width='stretch')

st.markdown("---")

# ---- Filter by Competition ----
st.subheader("🔍 Explore by Competition")
selected_comp = st.selectbox("Select Competition", sorted(df['competition'].unique()))
filtered = df[df['competition'] == selected_comp]

col1, col2, col3 = st.columns(3)
col1.metric("Total Goals", len(filtered))
col2.metric("Most Common Method", filtered['goal_method'].mode()[0])
col3.metric("Home Goals", len(filtered[filtered['home_away'] == 'Home']))

method_comp = filtered['goal_method'].value_counts().reset_index()
method_comp.columns = ['method', 'goals']
fig3 = px.pie(method_comp, names='method', values='goals', hole=0.4,
              color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig3, width='stretch')
