import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="CR7 Goals Explorer",
    page_icon="⚽",
    layout="wide"
)

df = pd.read_csv('data/ronaldo_goals.csv')

# ---- Club Config ----
club_config = {
    "All Clubs": {
        "primary": "#00BFFF",
        "secondary": "#1a1a1a",
        "bg": "#0a0a0a",
        "text": "#FFFFFF",
        "subtitle": "816 goals · 5 clubs · 20 competitions · One legend",
        "gradient": "linear-gradient(135deg, #0a0a0a, #1a1a1a)",
        "bar_color": "#00BFFF"
    },
    "Sporting CP": {
        "primary": "#006600",
        "secondary": "#004400",
        "bg": "#001a00",
        "text": "#FFFFFF",
        "subtitle": "Where it all began · Liga Portugal · 2002-2003",
        "gradient": "linear-gradient(135deg, #001a00, #003300, #001a00)",
        "bar_color": "#00cc00"
    },
    "Manchester United": {
        "primary": "#CC0000",
        "secondary": "#800000",
        "bg": "#1a0000",
        "text": "#FFFFFF",
        "subtitle": "The Red Devil · Premier League · 2003-2009",
        "gradient": "linear-gradient(135deg, #1a0000, #2a0000, #1a0000)",
        "bar_color": "#ff3333"
    },
    "Real Madrid": {
        "primary": "#FFFFFF",
        "secondary": "#c8a800",
        "bg": "#1a1500",
        "text": "#FFFFFF",
        "subtitle": "Los Blancos · LaLiga · 2009-2018",
        "gradient": "linear-gradient(135deg, #1a1500, #2a2200, #1a1500)",
        "bar_color": "#FFFFFF"
    },
    "Juventus FC": {
        "primary": "#222222",
        "secondary": "#aaaaaa",
        "bg": "#0d0d0d",
        "text": "#FFFFFF",
        "subtitle": "La Vecchia Signora · Serie A · 2018-2021",
        "gradient": "linear-gradient(135deg, #0d0d0d, #1a1a1a, #0d0d0d)",
        "bar_color": "#888888"
    },
    "Al-Nassr FC": {
        "primary": "#F5C518",
        "secondary": "#003580",
        "bg": "#000f2a",
        "text": "#FFFFFF",
        "subtitle": "The Saudi Chapter · Saudi Pro League · 2023-Present",
        "gradient": "linear-gradient(135deg, #00051a, #000f2a, #001040)",
        "bar_color": "#F5C518"
    }
}

# ---- Session State ----
if 'selected_club' not in st.session_state:
    st.session_state['selected_club'] = 'All Clubs'
selected_club = st.session_state['selected_club']
cfg = club_config[selected_club]

# ---- Dynamic Theme CSS ----
st.markdown(f"""
<style>
.stApp {{
    background: {cfg['gradient']};
}}
hr {{
    border: 1px solid {cfg['primary']};
    opacity: 0.4;
}}
[data-testid="metric-container"] {{
    background: linear-gradient(135deg, {cfg['secondary']}33, {cfg['bg']});
    border: 1px solid {cfg['primary']};
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 4px 15px {cfg['primary']}22;
}}
[data-testid="metric-container"] label {{
    color: {cfg['primary']} !important;
    font-size: 0.85em !important;
}}
[data-testid="metric-container"] [data-testid="metric-value"] {{
    color: #FFFFFF !important;
    font-size: 1.8em !important;
    font-weight: bold !important;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {cfg['bg']}, {cfg['secondary']}44);
    border-right: 1px solid {cfg['primary']};
}}
[data-testid="stSidebar"] * {{
    color: {cfg['primary']} !important;
}}
h1, h2, h3 {{
    color: {cfg['primary']} !important;
}}
.stButton > button {{
    background: transparent;
    color: {cfg['primary']};
    border: 1px solid {cfg['primary']};
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s;
}}
.stButton > button:hover {{
    background: {cfg['primary']};
    color: #000000;
}}
</style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.markdown(f"""
<div style='text-align: center; padding: 10px 0;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg'
         style='width: 100%; border-radius: 12px; border: 2px solid {cfg['primary']};'/>
    <p style='color: {cfg['primary']}; font-weight: bold; margin-top: 8px;'>Cristiano Ronaldo</p>
    <p style='color: #aaaaaa; font-size: 0.8em;'>816 Career Goals</p>
</div>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown("""
<h2 style='text-align: center; color: #FFD700; margin-bottom: 20px;'>
    ⚽ CR7 Career Goals Explorer
</h2>
""", unsafe_allow_html=True)

# ---- Club Selector ----
club_names = list(club_config.keys())
cols = st.columns(6)

for i, club in enumerate(club_names):
    with cols[i]:
        c = club_config[club]
        is_selected = selected_club == club
        circle_size = "50px" if is_selected else "40px"
        glow = f"0 0 20px {c['primary']}cc" if is_selected else f"0 0 10px {c['primary']}66"
        border = "3px solid #ffffff" if is_selected else "2px solid #444"

        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 5px;'>
            <div style='
                width: {circle_size};
                height: {circle_size};
                background-color: {c["primary"]};
                border-radius: 50%;
                margin: 0 auto 6px auto;
                border: {border};
                box-shadow: {glow};
            '></div>
        </div>
        """, unsafe_allow_html=True)

        # selected button gets filled style via CSS
        if is_selected:
            st.markdown(f"""
            <style>
            div[data-testid="column"]:nth-child({i + 1}) .stButton > button {{
                background-color: {c["primary"]} !important;
                color: #000000 !important;
                border: 2px solid {c["primary"]} !important;
                font-weight: bold !important;
            }}
            </style>
            """, unsafe_allow_html=True)

        if st.button(club, key=f"btn_{club}", use_container_width=True):
            st.session_state['selected_club'] = club
            st.rerun()

st.markdown("---")

# ---- Filter Data ----
if selected_club == "All Clubs":
    filtered_df = df
else:
    filtered_df = df[df['team'] == selected_club]

# ---- Hero Banner ----
st.markdown(f"""
<div style='
    background: {cfg["gradient"]};
    padding: 50px 40px;
    border-radius: 16px;
    border: 2px solid {cfg["primary"]};
    margin-bottom: 30px;
    text-align: center;
    box-shadow: 0 8px 32px {cfg["primary"]}33;
'>
    <h1 style='color: {cfg["primary"]}; font-size: 3em; margin: 10px 0;'>
        {selected_club}
    </h1>
    <p style='color: #cccccc; font-size: 1.1em;'>{cfg["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ---- Metrics ----
total_goals = len(filtered_df)
competitions = filtered_df['competition'].nunique()
seasons = filtered_df['season'].nunique()
top_method = filtered_df['goal_method'].mode()[0] if len(filtered_df) > 0 else "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("⚽ Goals", total_goals)
col2.metric("🏆 Competitions", competitions)
col3.metric("📅 Seasons", seasons)
col4.metric("🎯 Top Method", top_method)

st.markdown("---")

# ---- Charts ----
if selected_club == "All Clubs":
    st.markdown(f"<h3 style='color: {cfg['primary']}'>🏟️ Goals by Club</h3>", unsafe_allow_html=True)
    club_goals = filtered_df['team'].value_counts().reset_index()
    club_goals.columns = ['club', 'goals']
    fig1 = px.bar(club_goals, x='club', y='goals', text='goals',
                  color_discrete_sequence=[cfg['bar_color']])
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        xaxis_title='', yaxis_title='Goals'
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.markdown(f"<h3 style='color: {cfg['primary']}'>📅 Goals per Season at {selected_club}</h3>", unsafe_allow_html=True)
    season_goals = filtered_df['season'].value_counts().reset_index()
    season_goals.columns = ['season', 'goals']
    season_goals = season_goals.sort_values('season')
    fig1 = px.bar(season_goals, x='season', y='goals', text='goals',
                  color_discrete_sequence=[cfg['bar_color']])
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        xaxis_title='Season', yaxis_title='Goals'
    )
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<h3 style='color: {cfg['primary']}'>🎯 Goal Methods</h3>", unsafe_allow_html=True)
    method_goals = filtered_df['goal_method'].value_counts().reset_index()
    method_goals.columns = ['method', 'goals']
    fig2 = px.pie(method_goals, names='method', values='goals', hole=0.4,
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown(f"<h3 style='color: {cfg['primary']}'>🏠 Home vs Away</h3>", unsafe_allow_html=True)
    home_away = filtered_df['home_away'].value_counts().reset_index()
    home_away.columns = ['type', 'goals']
    fig3 = px.pie(home_away, names='type', values='goals', hole=0.4,
                  color_discrete_map={'Home': cfg['primary'], 'Away': '#555555'})
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

st.markdown(f"<h3 style='color: {cfg['primary']}'>😤 Top Opponents</h3>", unsafe_allow_html=True)
top_opponents = filtered_df['opponent'].value_counts().head(10).reset_index()
top_opponents.columns = ['opponent', 'goals']
fig4 = px.bar(top_opponents, x='goals', y='opponent', orientation='h',
              text='goals', color_discrete_sequence=[cfg['bar_color']])
fig4.update_traces(textposition='outside')
fig4.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#ffffff',
    yaxis_title='', xaxis_title='Goals', height=400
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #555; font-size: 0.8em;'>
    CR7 Goals Explorer · Built with Python & Streamlit
</p>
""", unsafe_allow_html=True)