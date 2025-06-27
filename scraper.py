import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

@st.cache_data(show_spinner=False)
def get_all_players():
    url = "https://fbref.com/en/players/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        links = soup.select("div#content a[href^='/en/players/']")

        player_dict = {}
        for a in links:
            name = a.text.strip()
            href = a.get("href", "")
            if re.match(r"^/en/players/[a-zA-Z0-9]{8}/[a-zA-Z0-9\-\']+$", href) and len(name) > 3:
                full_url = "https://fbref.com" + href
                player_dict[name] = full_url
        if not player_dict:
            raise ValueError("No players found")
        return player_dict
    except Exception as e:
        print(f"FBref error: {e}")
        # fallback example players
        return {
            "Lionel Messi": "https://fbref.com/en/players/d70ce98e/Lionel-Messi",
            "Cristiano Ronaldo": "https://fbref.com/en/players/dea698d9/Cristiano-Ronaldo"
        }

@st.cache_data(show_spinner=False)
def get_all_teams():
    url = "https://fbref.com/en/squads/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        links = soup.select("div#content a[href^='/en/squads/']")

        team_dict = {}
        for a in links:
            name = a.text.strip()
            href = a.get("href", "")
            if re.match(r"^/en/squads/[a-zA-Z0-9]{8}/[a-zA-Z0-9\-]+$", href):
                full_url = "https://fbref.com" + href
                team_dict[name] = full_url
        if not team_dict:
            raise ValueError("No teams found")
        return team_dict
    except Exception
