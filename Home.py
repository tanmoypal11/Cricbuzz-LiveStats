import streamlit as st

# Page config
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)


# Main Header
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

# Intro
st.info(
    "Welcome to Cricbuzz LiveStats! 🚀\n\n"
    "This platform integrates live data from the Cricbuzz API with SQL databases "
    "to deliver real-time match updates, player statistics, and analytics."
)

# Technologies
st.header("🛠️ Technologies Used")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("- Streamlit\n- Plotly\n- Pandas")
with col2:
    st.markdown("- Python\n- REST API\n- JSON")
with col3:
    st.markdown("- MySQL\n- SQLite\n- PyMySQL")

# Features
st.header("⭐ Key Features")
features = {
    "📺 Live Match Updates": "Real-time scorecards and match details",
    "📊 Player Statistics": "Batting and bowling stats with history",
    "📈 SQL Analytics": "25+ queries for deeper insights",
    "🛠️ CRUD Operations": "Manage players & match data",
    "🎯 Fantasy Support": "Player form & performance tracking",
    "📱 Responsive": "Works on desktop, tablet, and mobile"
}
for title, desc in features.items():
    st.markdown(f"**{title}** — {desc}")

# Getting Started
st.header("🚀 Getting Started")
st.markdown("""
1. Use the sidebar for navigation  
2. Check **Live Matches** for ongoing games  
3. Explore **Player Stats**  
4. Run **SQL Analytics**  
5. Manage data with **CRUD Operations**
""")

# Project Structure
st.header("📁 Project Structure")
st.code("""
Cricbuzz-LiveStats/
├── main.py
├── utils/
│   ├── db_connection.py
│   ├── api_handler.py
│   └── data_processor.py
├── pages/
│   ├── live_matches.py
│   ├── player_stats.py
│   ├── sql_analytics.py
│   └── crud_operations.py
├── data/sample_data.db
├── requirements.txt
└── README.md
""")

# Business Use Cases
st.header("💼 Business Use Cases")
st.markdown("""
- Sports Media: Real-time updates for commentary  
- Fantasy Platforms: Player form analysis  
- Analytics Firms: Player evaluation  
- Education: Database teaching with real data  
- Betting & Prediction: Odds based on performance  
""")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Python & MySQL | © 2024 Cricbuzz LiveStats Project")
