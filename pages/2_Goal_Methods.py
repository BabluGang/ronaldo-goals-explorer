import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Goal Methods", page_icon="⚽", layout="wide")
st.title("⚽ Goal Methods")
st.markdown("---")

df = pd.read_csv('data/ronaldo_goals.csv')
df['goal_minute'] = df['goal_minute'].astype(str).str.replace("'", "").str.replace("+", ".").str.strip()
df['goal_minute'] = pd.to_numeric(df['goal_minute'], errors='coerce')

# ---- Goal Method Breakdown ----
st.subheader("🎯 How Does He Score?")
method_goals = df['goal_method'].value_counts().reset_index()
method_goals.columns = ['method', 'goals']

fig1 = px.bar(
    method_goals,
    x='goals',
    y='method',
    orientation='h',
    color='goals',
    color_continuous_scale='Reds',
    text='goals'
)
fig1.update_traces(textposition='outside')
fig1.update_layout(coloraxis_showscale=False, yaxis_title='', xaxis_title='Goals')
st.plotly_chart(fig1, width='stretch')

st.markdown("---")

# ---- Goal Method by Club ----
st.subheader("🏟️ Goal Method by Club")
club_method = df.groupby(['team', 'goal_method']).size().reset_index(name='goals')
fig2 = px.bar(
    club_method,
    x='team',
    y='goals',
    color='goal_method',
    barmode='stack',
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig2.update_layout(xaxis_title='', yaxis_title='Goals', legend_title='Method')
st.plotly_chart(fig2, width='stretch')

st.markdown("---")

# ---- Goal Minute Distribution ----
st.subheader("⏱️ When Does He Score? (Goal Minute Distribution)")
fig3 = px.histogram(
    df.dropna(subset=['goal_minute']),
    x='goal_minute',
    nbins=18,
    color_discrete_sequence=['#FFD700'],
    labels={'goal_minute': 'Minute', 'count': 'Goals'}
)
fig3.update_layout(bargap=0.1)
st.plotly_chart(fig3, width='stretch')

st.markdown("---")

# ---- Goal Minute Bucket ----
st.subheader("⏱️ Goals by Time Period")
bucket_goals = df['goal_minute_bucket'].value_counts().reset_index()
bucket_goals.columns = ['period', 'goals']
bucket_order = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '90+']
bucket_goals['period'] = pd.Categorical(bucket_goals['period'], categories=bucket_order, ordered=True)
bucket_goals = bucket_goals.sort_values('period')

fig4 = px.bar(
    bucket_goals,
    x='period',
    y='goals',
    color='goals',
    color_continuous_scale='Oranges',
    text='goals'
)
fig4.update_traces(textposition='outside')
fig4.update_layout(coloraxis_showscale=False, xaxis_title='Time Period', yaxis_title='Goals')
st.plotly_chart(fig4, width='stretch')
