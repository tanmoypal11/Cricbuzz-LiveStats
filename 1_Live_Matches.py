import streamlit as st
from utils.api import fetch

st.title("📊 Live Matches")

data = fetch("/matches/v1/live")
match_options = {}

if "typeMatches" in data:
    for mtype in data["typeMatches"]:
        for series in mtype["seriesMatches"]:
            for match in series.get("seriesAdWrapper", {}).get("matches", []):
                if "matchInfo" in match:
                    info = match["matchInfo"]
                    match_id = info["matchId"]
                    title = f"{info['team1']['teamName']} vs {info['team2']['teamName']} ({info.get('matchDesc','')})"
                    match_options[title] = match_id

if match_options:
    selected = st.selectbox("Select a Live Match", list(match_options.keys()))
    match_id = match_options[selected]
    score_data = fetch(f"/mcenter/v1/{match_id}/hscard")

    if "scoreCard" in score_data:
        for inning in score_data["scoreCard"]:
            st.markdown(f"### 🏏 {inning['batTeamDetails']['batTeamName']} - {inning.get('runs',0)}/{inning.get('wickets',0)} in {inning.get('overs','0')} overs")

            st.write("**Batting:**")
            batsmen = [
                [b["batName"], b["runs"], b["balls"], b["fours"], b["sixes"], b["strikeRate"]]
                for b in inning["batTeamDetails"].get("batsmenData", {}).values()
            ]
            st.table(batsmen)

            st.write("**Bowling:**")
            bowlers = [
                [bo["bowlName"], bo["overs"], bo["maidens"], bo["runs"], bo["wickets"], bo["economy"]]
                for bo in inning.get("bowlTeamDetails", {}).get("bowlersData", {}).values()
            ]
            st.table(bowlers)
else:
    st.warning("⚠️ No live matches found at the moment.")
