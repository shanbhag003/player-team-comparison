import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

@st.cache_data(show_spinner=False)
def get_all_players():
    res = requests.get("https://fbref.com/en/players/")
    soup = BeautifulSoup(res.text, "lxml")
    links = soup.select("div#content a[href^='/en/players/']")

    player_dict = {}
    for a in links:
        href = a.get("href", "")
        name = a.text.strip()
        if href.count("/") == 4:  # /en/players/{id}/{name}
            full_url = "https://fbref.com" + href
            player_dict[name] = full_url
    return player_dict

@st.cache_data(show_spinner=False)
def get_all_teams():
    res = requests.get("https://fbref.com/en/squads/")
    soup = BeautifulSoup(res.text, "lxml")
    links = soup.select("div#content a[href^='/en/squads/']")

    team_dict = {}
    for a in links:
        href = a.get("href", "")
        name = a.text.strip()
        if href.count("/") == 4:  # /en/squads/{id}/{name}
            full_url = "https://fbref.com" + href
            team_dict[name] = full_url
    return team_dict

@st.cache_data(show_spinner=False)
def get_player_stats(url):
    tables = pd.read_html(url)
    return tables[0]  # update if needed

@st.cache_data(show_spinner=False)
def get_team_stats(url):
    tables = pd.read_html(url)
    return tables[0]  # update if needed
