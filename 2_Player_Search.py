import streamlit as st
import requests
import pandas as pd

# API Config
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": "ddbcfd40b9msh911004891824267p1640f9jsn038fe760a8e0",  # ✅ your key
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

# Page setup
st.set_page_config(page_title="Cricbuzz Player Search", page_icon="🏏", layout="wide")
st.title("🏏 Cricbuzz Player Search")

# Search bar
player_name = st.text_input("🔍 Search Player", placeholder="Type player name...")

if player_name.strip():
    url = f"{BASE_URL}/stats/v1/player/search"
    params = {"plrN": player_name.lower()}  # case-insensitive search

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if "player" in data and data["player"]:
            st.subheader(f"Results for **{player_name.title()}**")

            for p in data["player"]:
                if player_name.lower() in p.get("name", "").lower():
                    st.markdown(f"### {p.get('name', 'Unknown')} ({p.get('teamName', 'N/A')})")
                    st.write(f"**Player ID:** {p.get('id', 'N/A')}")

                    # Button to fetch full profile
                    if st.button(f"📄 View Profile: {p.get('name')}"):
                        player_id = p.get("id")

                        # ----- Player Info -----
                        info_url = f"{BASE_URL}/stats/v1/player/{player_id}"
                        info_res = requests.get(info_url, headers=HEADERS).json()
                        clean_info = {k: v for k, v in info_res.items() if k not in ["image", "bio", "faceImageId"]}

                        st.subheader(clean_info.get("name", "Unknown"))
                        st.write(f"**Nickname:** {clean_info.get('nickName', 'N/A')}")
                        st.write(f"**Role:** {clean_info.get('role', 'N/A')}")
                        st.write(f"**Batting Style:** {clean_info.get('bat', 'N/A')}")
                        st.write(f"**Bowling Style:** {clean_info.get('bowl', 'N/A')}")
                        st.write(f"**Team:** {clean_info.get('intlTeam', 'N/A')}")
                        st.write(f"**Other Teams:** {clean_info.get('teams', 'N/A')}")
                        st.write(f"**DOB:** {clean_info.get('DoB', 'N/A')}")
                        st.write(f"**Height:** {clean_info.get('height', 'N/A')}")
                        st.write(f"**Birth Place:** {clean_info.get('birthPlace', 'N/A')}")

                        if "appIndex" in clean_info:
                            st.markdown(f"[🌐 Full Profile]({clean_info['appIndex'].get('webURL', '#')})")

                        # ----- Batting Stats -----
                        bat_url = f"{BASE_URL}/stats/v1/player/{player_id}/batting"
                        bat_res = requests.get(bat_url, headers=HEADERS).json()

                        if "values" in bat_res:
                            st.markdown("### 🏏 Batting Stats")
                            bat_headers = bat_res["headers"][1:]  # Skip ROWHEADER
                            bat_data = {row["values"][0]: row["values"][1:] for row in bat_res["values"]}
                            df_bat = pd.DataFrame(bat_data, index=bat_headers).T
                            st.dataframe(df_bat)

                        # ----- Bowling Stats -----
                        bowl_url = f"{BASE_URL}/stats/v1/player/{player_id}/bowling"
                        bowl_res = requests.get(bowl_url, headers=HEADERS).json()

                        if "values" in bowl_res:
                            st.markdown("### 🎯 Bowling Stats")
                            bowl_headers = bowl_res["headers"][1:]  # Skip ROWHEADER
                            bowl_data = {row["values"][0]: row["values"][1:] for row in bowl_res["values"]}
                            df_bowl = pd.DataFrame(bowl_data, index=bowl_headers).T
                            st.dataframe(df_bowl)

                    st.divider()
        else:
            st.warning("⚠️ No players found!")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
