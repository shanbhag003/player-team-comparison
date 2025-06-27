import streamlit as st
import pandas as pd
import requests
import json
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
            if re.match(r"^/en/players/[a-zA-Z0-9]{8}/[a-zA-Z0-9\-']+$", href) and len(name) > 3:
                full_url = "https://fbref.com" + href
                player_dict[name] = full_url

        if player_dict:
            return player_dict
        else:
            raise Exception("Empty player dict")

    except Exception as e:
        print(f"Live player fetch failed: {e}")
        with open("players.json", "r") as f:
            return json.load(f)

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

        if team_dict:
            return team_dict
        else:
            raise Exception("Empty team dict")

    except Exception as e:
        print(f"Live team fetch failed: {e}")
        with open("teams.json", "r") as f:
            return json.load(f)

@st.cache_data(show_spinner=False)
def get_player_stats(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        tables = pd.read_html(res.text)
        return tables[0] if tables else pd.DataFrame()
    except Exception as e:
        print(f"Error fetching player stats from {url}:", e)
        return pd.DataFrame({"Error": ["Unable to fetch stats. Try a different player."]})

@st.cache_data(show_spinner=False)
def get_team_stats(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        tables = pd.read_html(res.text)
        return tables[0] if tables else pd.DataFrame()
    except Exception as e:
        print(f"Error fetching team stats from {url}:", e)
        return pd.DataFrame({"Error": ["Unable to fetch stats. Try a different team."]})
