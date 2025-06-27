import streamlit as st
import pandas as pd
from scraper import get_player_stats, get_team_stats

st.set_page_config(layout="wide")
st.title("⚽ Player/Team Comparison Tool")

comparison_type = st.radio("Compare:", ["Players", "Teams"])

if comparison_type == "Players":
    url1 = st.text_input("Enter FBref URL for Player 1")
    url2 = st.text_input("Enter FBref URL for Player 2")
    
    if st.button("Compare Players"):
        try:
            df1 = get_player_stats(url1)
            df2 = get_player_stats(url2)
            st.subheader("Player 1 Stats")
            st.dataframe(df1)
            st.subheader("Player 2 Stats")
            st.dataframe(df2)
        except Exception as e:
            st.error(f"Error fetching data: {e}")

elif comparison_type == "Teams":
    url1 = st.text_input("Enter FBref URL for Team 1")
    url2 = st.text_input("Enter FBref URL for Team 2")
    
    if st.button("Compare Teams"):
        try:
            df1 = get_team_stats(url1)
            df2 = get_team_stats(url2)
            st.subheader("Team 1 Stats")
            st.dataframe(df1)
            st.subheader("Team 2 Stats")
            st.dataframe(df2)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
