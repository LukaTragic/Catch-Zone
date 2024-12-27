import sys, os, importlib
from typing import Dict
import sqlite3

sys.path.append(os.path.abspath('..'))

import src
importlib.reload(src)
from src import *

def fetch_store_team_data(team_code: str, webscrape_id: int, db_name: str, type: str):
    """
    Fetch and store team data as well as return for future use

    Args:
    team_code (str): Three letter team code
    webscrape_id (int): Helper variable for past data
    db_name (str): Database to store table in
    type (str): Identifier if hits or pitches
    Returns:
    roster (Dict): team roster
    output (pd.DataBase): hits or pitches of supplied team
    hr_output (pd.Database): hits or pitches of supplied team that resulted in a home run
    """


    con = sqlite3.connect(db_name)
    roster = get_roster(team_code, webscrape_id)

    if type == 'hits':
        hits = get_team_hits(roster)
        store(hits, db_name, f"{team_code.lower()}_hits")
        hr_hits = pd.read_sql_query(f"SELECT * FROM {team_code.lower()}_hits WHERE events = 'home_run'", con)
        con.close()
        return roster, hits, hr_hits

    if type == 'pitches':
        pitches = get_team_pitches(roster)
        store(pitches, db_name, f"{team_code.lower()}_pitches")
        hr_pitches = pd.read_sql_query(f"SELECT * FROM {team_code.lower()}_pitches WHERE events = 'home_run'", con)
        con.close()
        return roster, pitches, hr_pitches

def fetch_pitch_distribution(team_code: str, team_roster: Dict, webscrape_id: int, pitches: pd.DataFrame, hr_pitches: pd.DataFrame, game_date: str):
    """
    Fetch and store pitch distribution according to weights

    Args:
    team_code (str): Three letter team code
    team_roster (Dict): team roster
    webscrape_id (int): Helper variable for past data
    pitches (pd.DataFrame): Pitches of team
    hr_pitches (pd.DataFrame): Home run pitches of team
    game_date (str): Date of game we're examining
    Returns:
    pitch_distribution (pd.DataFrame): probability of each pitch being thrown and the associated average and stddev of each statistic
    """

    roster_positions = get_roster_depth_chart(team_code, webscrape_id)
    total_weights = calculate_total_weights(team_roster, roster_positions, pitches, game_date)
    total_weights_adj = flip_add_dict(total_weights)
    player_pitch = get_player_pitch_statistics(hr_pitches)

    pitch_distribution = calculate_pitch_stats(total_weights_adj, player_pitch)

    return pitch_distribution
