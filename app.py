import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scraper import (
  get_player_stats,
  get_team_stats,
  get_all_players,
  get_all_teams
)

st.set_page_config(layout="wide")
st.title("⚽ Player/Team Comparison Tool")

option = st.radio("Compare", ["Players", "Teams"])

if option == "Players":
    players = get_all_players()
    if not players:
        st.warning("No player data available.")
    else:
        player1_name = st.selectbox("Select Player 1", options=list(players.keys()), key="p1")
        player2_name = st.selectbox("Select Player 2", options=list(players.keys()), key="p2")

        if player1_name and player2_name:
            df1 = get_player_stats(players[player1_name])
            df2 = get_player_stats(players[player2_name])

            st.subheader(f"Stats for {player1_name}")
            st.dataframe(df1)
            st.subheader(f"Stats for {player2_name}")
            st.dataframe(df2)

            def extract_selected_stats(df):
                df.columns = df.columns.map(str)
                try:
                    row = df[df["90s"].astype(str).str.contains(r"^\d")].head(1)
                    stats = {
                        "G90": float(row["Gls"].values[0]),
                        "xG90": float(row["xG"].values[0]),
                        "Sh90": float(row["Sh"].values[0]),
                        "A90": float(row["Ast"].values[0]),
                        "xA90": float(row["xA"].values[0]),
                        "KP90": float(row["KP"].values[0])
                    }
                    return stats
                except Exception as e:
                    st.warning(f"Could not extract radar stats: {e}")
                    return {}

            stats1 = extract_selected_stats(df1)
            stats2 = extract_selected_stats(df2)

            if stats1 and stats2:
                categories = list(stats1.keys())
                vals1 = list(stats1.values())
                vals2 = list(stats2.values())

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=vals1, theta=categories, fill='toself', name=player1_name))
                fig.add_trace(go.Scatterpolar(r=vals2, theta=categories, fill='toself', name=player2_name))

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(vals1 + vals2) * 1.2])),
                    showlegend=True,
                    title="🔵 Player Comparison Radar"
                )

                st.plotly_chart(fig, use_container_width=True)

elif option == "Teams":
    teams = get_all_teams()
    if not teams:
        st.warning("No team data available.")
    else:
        team1_name = st.selectbox("Select Team 1", options=list(teams.keys()), key="t1")
        team2_name = st.selectbox("Select Team 2", options=list(teams.keys()), key="t2")

        if team1_name and team2_name:
            df1 = get_team_stats(teams[team1_name])
            df2 = get_team_stats(teams[team2_name])

            st.subheader(f"Stats for {team1_name}")
            st.dataframe(df1)
            st.subheader(f"Stats for {team2_name}")
            st.dataframe(df2)
