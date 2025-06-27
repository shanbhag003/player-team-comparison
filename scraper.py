import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

@st.cache_data(show_spinner=False)
def get_all_players():
    url = "https://fbref.com/en/players/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    links = soup.select("div#content a[href^='/en/players/']")

    player_dict = {}
    for a in links:
        name = a.text.strip()
        href = a.get("href", "")
        # Valid player profile: /en/players/{id}/{name}
        if re.match(r"^/en/players/[a-zA-Z0-9]{8}/.+", href) and len(name) > 3:
            full_url = "https://fbref.com" + href
            player_dict[name] = full_url
    return player_dict

@st.cache_data(show_spinner=False)
def get_all_teams():
    url = "https://fbref.com/en/squads/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    links = soup.select("div#content a[href^='/en/squads/']")

    team_dict = {}
    for a in links:
        name = a.text.strip()
        href = a.get("href", "")
        # Valid team profile: /en/squads/{id}/{team-name}
        if re.match(r"^/en/squads/[a-zA-Z0-9]{8}/[a-zA-Z0-9\-]+$", href):
            full_url = "https://fbref.com" + href
            team_dict[name] = full_url
    return team_dict

@st.cache_data(show_spinner=False)
def get_player_stats(url):
    tables = pd.read_html(url)
    return tables[0] if tables else pd.DataFrame()

@st.cache_data(show_spinner=False)
def get_team_stats(url):
    tables = pd.read_html(url)
    return tables[0] if tables else pd.DataFrame()
