import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------
# Database connection (single instance, reused)
# -----------------------------
try:
    conn = pymysql.connect(
        host="127.0.0.1",
        user="cricapp",
        password="Strong!Pass#123",
        database="Cricbuzz_project",
        port=3306
    )
except Exception as e:
    st.error(f"Database connection error: {e}")
    conn = None

# -----------------------------
# Streamlit app settings
# -----------------------------
st.set_page_config(page_title="Cricket Statistics Dashboard", layout="wide")
st.title("🏏 Cricket Statistics Dashboard")
st.markdown("---")

if conn:

    # -----------------------------
    # Question 1: Indian Players
    # -----------------------------
    st.header("1. Indian Cricket Players")
    try:
        query = """
        SELECT name as full_name, category as playing_role, 
               battingStyle as batting_style, bowlingStyle as bowling_style
        FROM indian_players
        ORDER BY name
        """
        df1 = pd.read_sql(query, conn)
        st.dataframe(df1, use_container_width=True)
    except Exception as e:
        st.warning(f"No data found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 2: Recent Matches (last 30 days)
    # -----------------------------
    st.header("2. Recent Matches (Last 30 Days)")
    try:
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        query = """
        SELECT matchDesc as match_description, team1Name as team1, 
               team2Name as team2, venueGround as venue, startDate as match_date
        FROM match_results
        WHERE startDate >= %s
        ORDER BY startDate DESC
        """
        df2 = pd.read_sql(query, conn, params=[thirty_days_ago])
        st.dataframe(df2, use_container_width=True)
    except Exception as e:
        st.warning(f"No recent matches found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 3: Top 10 ODI run scorers
    # -----------------------------
    st.header("3. Top 10 ODI Run Scorers")
    try:
        query = """
        SELECT Player as player_name, Runs as total_runs, 
               Average as batting_average
        FROM top_odi_runs
        ORDER BY Runs DESC
        LIMIT 10
        """
        df3 = pd.read_sql(query, conn)
        st.dataframe(df3, use_container_width=True)
    except Exception as e:
        st.warning(f"No ODI scorers found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 4: Large capacity venues
    # -----------------------------
    st.header("4. Large Capacity Venues")
    try:
        query = """
        SELECT ground as venue_name, city, country, capacity
        FROM venues
        WHERE capacity > 50000
        ORDER BY capacity DESC
        """
        df4 = pd.read_sql(query, conn)
        st.dataframe(df4, use_container_width=True)
    except Exception as e:
        st.warning(f"No large venues found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 5: Team wins
    # -----------------------------
    st.header("5. Matches Won by Each Team")
    try:
        query = """
        SELECT 
            t.team_id,
            t.team_name,
            COUNT(*) AS total_wins
        FROM test_teams t
        JOIN matches m ON t.team_id = m.match_winner_id
        WHERE m.match_winner_id IS NOT NULL 
          AND m.match_winner_id != 'draw'
        GROUP BY t.team_id, t.team_name
        ORDER BY total_wins DESC;
        """
        df5 = pd.read_sql(query, conn)
        st.dataframe(df5, use_container_width=True)
    except Exception as e:
        st.warning(f"No data found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 6: Players by role
    # -----------------------------
    st.header("6. Players by Playing Role")
    try:
        query = """
        SELECT role, COUNT(*) as player_count
        FROM teams_players
        WHERE role IS NOT NULL AND role != ''
        GROUP BY role
        ORDER BY player_count DESC
        """
        df6 = pd.read_sql(query, conn)
        st.dataframe(df6, use_container_width=True)
    except Exception as e:
        st.warning(f"No role data. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 7: Highest scores by format
    # -----------------------------
    st.header("7. Highest Individual Scores by Format")
    try:
        query = """
        SELECT Format as format, MAX(Highest_Score) as highest_score
        FROM highest_scores
        GROUP BY Format
        ORDER BY highest_score DESC
        """
        df7 = pd.read_sql(query, conn)
        st.dataframe(df7, use_container_width=True)
    except Exception as e:
        st.warning(f"No highest score data. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 8: 2024 cricket series
    # -----------------------------
    st.header("8. 2024 Cricket Series")
    try:
        query = """
        SELECT series_name, host_country, match_type, 
               start_date, total_matches
        FROM cricket_series_2024
        WHERE YEAR(start_date) = 2024
        ORDER BY start_date DESC
        """
        df8 = pd.read_sql(query, conn)
        st.dataframe(df8, use_container_width=True)
    except Exception as e:
        st.warning(f"No 2024 series data. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 9: All-rounders
    # -----------------------------
    st.header("9. All-Rounder Players (1000+ Runs & 50+ Wickets)")
    try:
        query = """
        SELECT 
            playerName,
            (COALESCE(Runs_Test_bat,0) + COALESCE(Runs_ODI_bat,0) + COALESCE(Runs_T20_bat,0)) AS TotalRuns,
            (COALESCE(Wickets_Test_bowl,0) + COALESCE(Wickets_ODI_bowl,0) + COALESCE(Wickets_T20_bowl,0)) AS TotalWickets
        FROM players_with_stats
        WHERE (COALESCE(Runs_Test_bat,0) + COALESCE(Runs_ODI_bat,0) + COALESCE(Runs_T20_bat,0)) > 1000
        AND (COALESCE(Wickets_Test_bowl,0) + COALESCE(Wickets_ODI_bowl,0) + COALESCE(Wickets_T20_bowl,0)) > 50
        ORDER BY TotalRuns DESC, TotalWickets DESC
        """
        df9 = pd.read_sql(query, conn)
        st.dataframe(df9, use_container_width=True)
    except Exception as e:
        st.warning(f"No all-rounder data found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 10: Last 20 completed matches
    # -----------------------------
    st.header("10. Last 20 Completed Matches")
    try:
        query = """
        select * from recent_matches
        limit 20
        """
        df10 = pd.read_sql(query, conn)
        st.dataframe(df10, use_container_width=True)
    except Exception as e:
        st.warning(f"No completed matches found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 11: Compare players across formats
    # -----------------------------
    st.header("11. Player Performance Across Formats")
    try:
        query = """
        SELECT 
            playerName,
            Runs_Test_bat AS test_runs,
            Runs_ODI_bat AS odi_runs,
            Runs_T20_bat AS t20_runs,

            ROUND(
                (
                    (Runs_Test_bat + Runs_ODI_bat + Runs_T20_bat) * 1.0
                ) / NULLIF(
                    ((Innings_Test_bat - `Not Out_Test_bat`) +
                     (Innings_ODI_bat - `Not Out_ODI_bat`) +
                     (Innings_T20_bat - `Not Out_T20_bat`)), 0
                ), 2
            ) AS overall_batting_average

        FROM players_with_stats
        WHERE 
            (
              (CASE WHEN Runs_Test_bat > 0 THEN 1 ELSE 0 END) +
              (CASE WHEN Runs_ODI_bat > 0 THEN 1 ELSE 0 END) +
              (CASE WHEN Runs_T20_bat > 0 THEN 1 ELSE 0 END)
            ) >= 2
        ORDER BY overall_batting_average DESC, playerName
        """
        df11 = pd.read_sql(query, conn)
        st.dataframe(df11, use_container_width=True)
    except Exception as e:
        st.warning(f"No comparative data found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 12: Home vs Away Performance
    # -----------------------------
    st.header("12. Home vs Away Performance")
    try:
        query = """
        WITH team_countries AS (
            SELECT
                team_id,
                team_name,
                CASE
                    WHEN UPPER(team_name) LIKE '%ENGLAND%' THEN 'England'
                    WHEN UPPER(team_name) LIKE '%INDIA%' THEN 'India'
                    WHEN UPPER(team_name) LIKE '%AUSTRALIA%' THEN 'Australia'
                    WHEN UPPER(team_name) LIKE '%NEW ZEALAND%' THEN 'New Zealand'
                    WHEN UPPER(team_name) LIKE '%SOUTH AFRICA%' THEN 'South Africa'
                    WHEN UPPER(team_name) LIKE '%PAKISTAN%' THEN 'Pakistan'
                    WHEN UPPER(team_name) LIKE '%SRI LANKA%' THEN 'Sri Lanka'
                    WHEN UPPER(team_name) LIKE '%WEST INDIES%' THEN 'West Indies'
                    WHEN UPPER(team_name) LIKE '%BANGLADESH%' THEN 'Bangladesh'
                    WHEN UPPER(team_name) LIKE '%ZIMBABWE%' THEN 'Zimbabwe'
                    WHEN UPPER(team_name) LIKE '%AFGHANISTAN%' THEN 'Afghanistan'
                    WHEN UPPER(team_name) LIKE '%IRELAND%' THEN 'Ireland'
                    ELSE 'Other'
                END AS country
            FROM test_teams
        ),
        venue_countries AS (
            SELECT DISTINCT
                venue_city,
                CASE
                    WHEN UPPER(venue_city) LIKE '%LONDON%' OR UPPER(venue_city) LIKE '%NOTTINGHAM%' OR UPPER(venue_city) LIKE '%LEEDS%' THEN 'England'
                    WHEN UPPER(venue_city) LIKE '%SYDNEY%' OR UPPER(venue_city) LIKE '%MELBOURNE%' OR UPPER(venue_city) LIKE '%BRISBANE%' THEN 'Australia'
                    WHEN UPPER(venue_city) LIKE '%MUMBAI%' OR UPPER(venue_city) LIKE '%DELHI%' OR UPPER(venue_city) LIKE '%BANGALORE%' THEN 'India'
                    WHEN UPPER(venue_city) LIKE '%WELLINGTON%' OR UPPER(venue_city) LIKE '%AUCKLAND%' THEN 'New Zealand'
                    WHEN UPPER(venue_city) LIKE '%JOHANNESBURG%' OR UPPER(venue_city) LIKE '%CAPE TOWN%' THEN 'South Africa'
                    WHEN UPPER(venue_city) LIKE '%LAHORE%' OR UPPER(venue_city) LIKE '%KARACHI%' THEN 'Pakistan'
                    WHEN UPPER(venue_city) LIKE '%COLOMBO%' OR UPPER(venue_city) LIKE '%KANDY%' THEN 'Sri Lanka'
                    WHEN UPPER(venue_city) LIKE '%BRIDGETOWN%' OR UPPER(venue_city) LIKE '%KINGSTON%' THEN 'West Indies'
                    WHEN UPPER(venue_city) LIKE '%DHAKA%' OR UPPER(venue_city) LIKE '%CHITTAGONG%' THEN 'Bangladesh'
                    WHEN UPPER(venue_city) LIKE '%HARARE%' THEN 'Zimbabwe'
                    ELSE 'Neutral'
                END AS country
            FROM matches
            WHERE venue_city IS NOT NULL
        ),
        match_venues AS (
            SELECT
                m.match_id,
                m.team1_id,
                m.team2_id,
                m.match_winner_id,
                vc.country AS venue_country,
                tc1.country AS team1_country,
                tc2.country AS team2_country
            FROM matches m
            JOIN venue_countries vc ON m.venue_city = vc.venue_city
            JOIN team_countries tc1 ON m.team1_id = tc1.team_id
            JOIN team_countries tc2 ON m.team2_id = tc2.team_id
            WHERE m.match_winner_id IS NOT NULL AND m.match_winner_id != 'draw'
        ),
        team_performance AS (
            SELECT
                t.team_id,
                t.team_name,
                COUNT(CASE WHEN mv.venue_country = tc.country THEN 1 END) AS home_matches,
                COUNT(CASE WHEN mv.venue_country = tc.country AND mv.match_winner_id = t.team_id THEN 1 END) AS home_wins,
                COUNT(CASE WHEN mv.venue_country != tc.country AND mv.venue_country != 'Neutral' THEN 1 END) AS away_matches,
                COUNT(CASE WHEN mv.venue_country != tc.country AND mv.venue_country != 'Neutral' AND mv.match_winner_id = t.team_id THEN 1 END) AS away_wins,
                COUNT(CASE WHEN mv.venue_country = 'Neutral' THEN 1 END) AS neutral_matches,
                COUNT(CASE WHEN mv.venue_country = 'Neutral' AND mv.match_winner_id = t.team_id THEN 1 END) AS neutral_wins
            FROM test_teams t
            JOIN team_countries tc ON t.team_id = tc.team_id
            JOIN match_venues mv ON t.team_id IN (mv.team1_id, mv.team2_id)
            GROUP BY t.team_id, t.team_name
        )
        SELECT
            team_name,
            home_matches,
            home_wins,
            ROUND(home_wins * 100.0 / NULLIF(home_matches, 0), 2) AS home_win_percentage,
            away_matches,
            away_wins,
            ROUND(away_wins * 100.0 / NULLIF(away_matches, 0), 2) AS away_win_percentage,
            neutral_matches,
            neutral_wins,
            ROUND(neutral_wins * 100.0 / NULLIF(neutral_matches, 0), 2) AS neutral_win_percentage,
            (home_matches + away_matches + neutral_matches) AS total_matches
        FROM team_performance
        WHERE home_matches + away_matches >= 5
        ORDER BY home_win_percentage DESC;
        """
        df12 = pd.read_sql(query, conn)
        st.dataframe(df12, use_container_width=True)
    except Exception as e:
        st.warning(f"No data found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 17: Toss Advantage Analysis
    # -----------------------------
    st.header("17. Toss Advantage Analysis")
    try:
        query = """
        WITH toss_analysis AS (
            SELECT
                m.match_format,
                COUNT(*) AS total_matches,
                COUNT(CASE WHEN m.match_winner_id = m.toss_winner_id THEN 1 END) AS toss_winner_wins,
                COUNT(CASE WHEN m.toss_winner_id = m.team1_id THEN 1 END) AS toss_bat_first,
                COUNT(CASE WHEN m.toss_winner_id = m.team1_id AND m.match_winner_id = m.toss_winner_id THEN 1 END) AS toss_bat_win,
                COUNT(CASE WHEN m.toss_winner_id = m.team2_id THEN 1 END) AS toss_field_first,
                COUNT(CASE WHEN m.toss_winner_id = m.team2_id AND m.match_winner_id = m.toss_winner_id THEN 1 END) AS toss_field_win
            FROM matches m
            WHERE m.match_winner_id IS NOT NULL AND m.match_winner_id != 'draw'
            GROUP BY m.match_format
        )
        SELECT
            match_format,
            total_matches,
            toss_winner_wins,
            ROUND(toss_winner_wins * 100.0 / total_matches, 2) AS toss_win_percentage,
            toss_bat_first,
            toss_bat_win,
            ROUND(toss_bat_win * 100.0 / NULLIF(toss_bat_first, 0), 2) AS bat_first_win_percentage,
            toss_field_first,
            toss_field_win,
            ROUND(toss_field_win * 100.0 / NULLIF(toss_field_first, 0), 2) AS field_first_win_percentage
        FROM toss_analysis
        ORDER BY match_format;
        """
        df17 = pd.read_sql(query, conn)
        st.dataframe(df17, use_container_width=True)
    except Exception as e:
        st.warning(f"No data found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 18: Most Economical Bowlers (ODI & T20)
    # -----------------------------
    st.header("18. Most Economical Bowlers (ODI & T20)")
    try:
        query = """
        SELECT 
            playerName,
           (COALESCE(Wickets_ODI_bowl,0) + COALESCE(Wickets_T20_bowl,0)) AS total_wickets,
            ROUND(
                (COALESCE(Runs_ODI_bowl,0) + COALESCE(Runs_T20_bowl,0)) * 6.0  
            / NULLIF((COALESCE(Balls_ODI_bowl,0) + COALESCE(Balls_T20_bowl,0)), 0), 2
            ) AS overall_economy
            FROM players_with_stats
        WHERE 
            -- Played at least 10 matches in LO formats
            (COALESCE(Matches_ODI_bowl,0) + COALESCE(Matches_T20_bowl,0)) >= 10
            -- Bowled at least 2 overs per match on average
        AND ( (COALESCE(Balls_ODI_bowl,0) + COALESCE(Balls_T20_bowl,0))  
              / NULLIF((COALESCE(Matches_ODI_bowl,0) + COALESCE(Matches_T20_bowl,0)), 0)  
            ) >= 12
        ORDER BY overall_economy ASC, total_wickets DESC, playerName
        """
        df18 = pd.read_sql(query, conn)
        st.dataframe(df18, use_container_width=True)
        
    except Exception as e:
        st.warning(f"No economical bowlers found. Error: {e}")
    st.markdown("---")

    # -----------------------------
    # Question 20: Player Matches & Batting Averages Across Formats
    # -----------------------------
    st.header("20. Player Matches & Batting Averages Across Formats")
    try:
        query = """
        SELECT
            playerName,
            Matches_Test_bat AS Test_Matches,
            Average_Test_bat AS Test_Batting_Avg,
            Matches_ODI_bat AS ODI_Matches,
            Average_ODI_bat AS ODI_Batting_Avg,
            Matches_T20_bat AS T20_Matches,
            Average_T20_bat AS T20_Batting_Avg,
            (COALESCE(Matches_Test_bat,0) + COALESCE(Matches_ODI_bat,0) + COALESCE(Matches_T20_bat,0)) AS Total_Matches
        FROM
            players_with_stats
        WHERE
            (COALESCE(Matches_Test_bat,0) + COALESCE(Matches_ODI_bat,0) + COALESCE(Matches_T20_bat,0)) >= 20
        ORDER BY
            Total_Matches DESC, playerName
        """
        df20 = pd.read_sql(query, conn)
        st.dataframe(df20, use_container_width=True)
    
    except Exception as e:
        st.warning(f"No players found with at least 20 matches. Error: {e}")
    st.markdown("---")


    # -----------------------------
    # Question 21: Comprehensive Player Performance Ranking
    # -----------------------------
    st.header("21. Comprehensive Player Performance Ranking without fielding")
    try:
        
        query = """
        WITH test_rank AS (
            SELECT 
                playerName AS test_player,
                ROUND((
                    (COALESCE(Runs_Test_bat,0) * 0.01) +
                    (COALESCE(Average_Test_bat,0) * 0.5) +
                    (COALESCE(SR_Test_bat,0) * 0.3) +
                    (COALESCE(Wickets_Test_bowl,0) * 2) +
                    ((50 - COALESCE(Avg_Test_bowl,50)) * 0.5) +
                    ((6 - COALESCE(Eco_Test_bowl,6)) * 2)
                ),2) AS test_score,
                RANK() OVER (ORDER BY 
                    ((COALESCE(Runs_Test_bat,0) * 0.01) +
                     (COALESCE(Average_Test_bat,0) * 0.5) +
                     (COALESCE(SR_Test_bat,0) * 0.3) +
                     (COALESCE(Wickets_Test_bowl,0) * 2) +
                     ((50 - COALESCE(Avg_Test_bowl,50)) * 0.5) +
                     ((6 - COALESCE(Eco_Test_bowl,6)) * 2)) DESC
                ) AS rnk
            FROM players_with_stats
        ),
        odi_rank AS (
            SELECT 
                playerName AS odi_player,
                ROUND((
                    (COALESCE(Runs_ODI_bat,0) * 0.01) +
                    (COALESCE(Average_ODI_bat,0) * 0.5) +
                    (COALESCE(SR_ODI_bat,0) * 0.3) +
                    (COALESCE(Wickets_ODI_bowl,0) * 2) +
                    ((50 - COALESCE(Avg_ODI_bowl,50)) * 0.5) +
                    ((6 - COALESCE(Eco_ODI_bowl,6)) * 2)
                ),2) AS odi_score,
                RANK() OVER (ORDER BY 
                    ((COALESCE(Runs_ODI_bat,0) * 0.01) +
                     (COALESCE(Average_ODI_bat,0) * 0.5) +
                     (COALESCE(SR_ODI_bat,0) * 0.3) +
                     (COALESCE(Wickets_ODI_bowl,0) * 2) +
                     ((50 - COALESCE(Avg_ODI_bowl,50)) * 0.5) +
                     ((6 - COALESCE(Eco_ODI_bowl,6)) * 2)) DESC
                ) AS rnk
            FROM players_with_stats
        ),
        t20_rank AS (
            SELECT 
                playerName AS t20_player,
                ROUND((
                    (COALESCE(Runs_T20_bat,0) * 0.01) +
                    (COALESCE(Average_T20_bat,0) * 0.5) +
                    (COALESCE(SR_T20_bat,0) * 0.3) +
                    (COALESCE(Wickets_T20_bowl,0) * 2) +
                    ((50 - COALESCE(Avg_T20_bowl,50)) * 0.5) +
                    ((6 - COALESCE(Eco_T20_bowl,6)) * 2)
                ),2) AS t20_score,
                RANK() OVER (ORDER BY 
                    ((COALESCE(Runs_T20_bat,0) * 0.01) +
                     (COALESCE(Average_T20_bat,0) * 0.5) +
                     (COALESCE(SR_T20_bat,0) * 0.3) +
                     (COALESCE(Wickets_T20_bowl,0) * 2) +
                     ((50 - COALESCE(Avg_T20_bowl,50)) * 0.5) +
                     ((6 - COALESCE(Eco_T20_bowl,6)) * 2)) DESC
                ) AS rnk
            FROM players_with_stats
        )
        SELECT 
            t.test_score, t.test_player,
            o.odi_score,  o.odi_player,
            tt.t20_score, tt.t20_player
        FROM test_rank t
        JOIN odi_rank o ON t.rnk = o.rnk
        JOIN t20_rank tt ON t.rnk = tt.rnk
        ORDER BY t.rnk
        LIMIT 20;
        """
        df21 = pd.read_sql(query, conn)
        st.dataframe(df21, use_container_width=True)
    except Exception as e:
        st.warning(f"No performance ranking found. Error: {e}")
    st.markdown("---")

    st.markdown("*Cricket Statistics Dashboard - Created with Streamlit*")

    # -----------------------------
    # Question 22: Head-to-Head Analysis
    # -----------------------------
    st.header("22. Head-to-Head Analysis")
    try:
        query = """
        WITH team_pairs AS (
            SELECT
                LEAST(m.team1_id, m.team2_id) AS team_a_id,
                GREATEST(m.team1_id, m.team2_id) AS team_b_id,
                t1.team_name AS team_a_name,
                t2.team_name AS team_b_name,
                COUNT(*) AS total_matches,
                COUNT(CASE WHEN m.match_winner_id = LEAST(m.team1_id, m.team2_id) THEN 1 END) AS team_a_wins,
                COUNT(CASE WHEN m.match_winner_id = GREATEST(m.team1_id, m.team2_id) THEN 1 END) AS team_b_wins,
                COUNT(CASE WHEN m.match_winner_id = 'draw' THEN 1 END) AS draws,
                AVG(CASE WHEN m.match_winner_id = LEAST(m.team1_id, m.team2_id) THEN m.margin_runs END) AS avg_win_margin_runs_a,
                AVG(CASE WHEN m.match_winner_id = LEAST(m.team1_id, m.team2_id) THEN m.margin_wickets END) AS avg_win_margin_wickets_a,
                AVG(CASE WHEN m.match_winner_id = GREATEST(m.team1_id, m.team2_id) THEN m.margin_runs END) AS avg_win_margin_runs_b,
                AVG(CASE WHEN m.match_winner_id = GREATEST(m.team1_id, m.team2_id) THEN m.margin_wickets END) AS avg_win_margin_wickets_b
            FROM matches m
            JOIN test_teams t1 ON LEAST(m.team1_id, m.team2_id) = t1.team_id
            JOIN test_teams t2 ON GREATEST(m.team1_id, m.team2_id) = t2.team_id
            WHERE m.match_winner_id IS NOT NULL
            GROUP BY LEAST(m.team1_id, m.team2_id), GREATEST(m.team1_id, m.team2_id), t1.team_name, t2.team_name
            HAVING COUNT(*) >= 5
        )
        SELECT
            team_a_name,
            team_b_name,
            total_matches,
            team_a_wins,
            team_b_wins,
            draws,
            ROUND(team_a_wins * 100.0 / total_matches, 2) AS team_a_win_percentage,
            ROUND(team_b_wins * 100.0 / total_matches, 2) AS team_b_win_percentage,
            ROUND(COALESCE(avg_win_margin_runs_a, 0), 1) AS avg_win_margin_runs_a,
            ROUND(COALESCE(avg_win_margin_wickets_a, 0), 1) AS avg_win_margin_wickets_a,
            ROUND(COALESCE(avg_win_margin_runs_b, 0), 1) AS avg_win_margin_runs_b,
            ROUND(COALESCE(avg_win_margin_wickets_b, 0), 1) AS avg_win_margin_wickets_b
        FROM team_pairs
        ORDER BY total_matches DESC;
        """
        df22 = pd.read_sql(query, conn)
        st.dataframe(df22, use_container_width=True)


    except Exception as e:
        st.warning(f"No data found. Error: {e}")
    st.markdown("---")


else:
    st.stop()
