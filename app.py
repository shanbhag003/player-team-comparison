import streamlit as st
import pandas as pd
from scraper import (
    get_player_stats,
    get_team_stats,
    get_all_players,
    get_all_teams
)

st.set_page_config(layout="wide")
st.title("⚽ Player/Team Comparison Tool")

comparison_type = st.radio("Compare:", ["Players", "Teams"])

if comparison_type == "Players":
    player_dict = get_all_players()
    player_names = sorted(player_dict.keys())

    player1 = st.selectbox("Select Player 1", player_names, key="p1")
    player2 = st.selectbox("Select Player 2", player_names, key="p2")

    if st.button("Compare Players"):
        url1 = player_dict[player1]
        url2 = player_dict[player2]

        try:
            df1 = get_player_stats(url1)
            df2 = get_player_stats(url2)

            st.subheader(f"{player1} Stats")
            st.dataframe(df1)

            st.subheader(f"{player2} Stats")
            st.dataframe(df2)

        except Exception as e:
            st.error(f"Error fetching player data: {e}")

elif comparison_type == "Teams":
    team_dict = get_all_teams()
    team_names = sorted(team_dict.keys())

    team1 = st.selectbox("Select Team 1", team_names, key="t1")
    team2 = st.selectbox("Select Team 2", team_names, key="t2")

    if st.button("Compare Teams"):
        url1 = team_dict[team1]
        url2 = team_dict[team2]

        try:
            df1 = get_team_stats(url1)
            df2 = get_team_stats(url2)

            st.subheader(f"{team1} Stats")
            st.dataframe(df1)

            st.subheader(f"{team2} Stats")
            st.dataframe(df2)

        except Exception as e:
            st.error(f"Error fetching team data: {e}")
