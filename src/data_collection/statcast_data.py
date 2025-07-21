import pybaseball
from pybaseball import statcast_batter, statcast_pitcher
from pybaseball.datahelpers.statcast_utils import add_spray_angle

import pandas as pd
from typing import List, Dict
import importlib
from datetime import date

from . import web_scraper
importlib.reload(web_scraper)
from .web_scraper import *

pybaseball.cache.enable()
today = date.today()

def get_team_hits(team_roster: Dict) -> pd.DataFrame:
    """
    Collect hit data for a specific team's roster.
    
    Args:
        team_roster (dict): Team roster        
    Returns:
        pd.DataFrame: Cleaned hit data
    """
    # Get team roster
    team_roster_ids = list(team_roster.keys())

    # Collect data for each player
    dataframes: List[pd.DataFrame] = []
    for player_id in team_roster_ids:
        try:
            temp_df = statcast_batter('2008-04-01', today.strftime("%Y-%m-%d"), player_id)
            dataframes.append(temp_df)
        except Exception as e:
            print(f"Error collecting data for player {player_id}: {e}")

    # Combine dataframes
    if not dataframes:
        return pd.DataFrame()

    team_at_bat = pd.concat(dataframes, ignore_index=True)

    # Add spray angle
    team_filtered_angles = add_spray_angle(team_at_bat)

    # Drop deprecated columns
    columns_to_drop = [
        'spin_rate_deprecated', 'break_angle_deprecated', 'break_length_deprecated',
        'tfs_deprecated', 'tfs_zulu_deprecated'
    ]

    team_filtered_clean = team_filtered_angles.drop(columns_to_drop, axis=1)

    return team_filtered_clean


'''
def get_team_pitches(team_roster: dict) -> pd.DataFrame:
    """
    Collect hit data for a specific team's roster.
    
    Args:
        team_roster (dict): Team roster
    Returns:
        pd.DataFrame: Cleaned hit data
    """
    team_roster_ids = list(team_roster.keys())

    # Collect data for each player
    dataframes: List[pd.DataFrame] = []
    for player_id in team_roster_ids:
        try:
            temp_df = statcast_pitcher('2024-02-22', '2024-10-30', player_id)
            dataframes.append(temp_df)
        except Exception as e:
            print(f"Error collecting data for player {player_id}: {e}")

    # Combine dataframes
    if not dataframes:
        return pd.DataFrame()

    team_at_pitch = pd.concat(dataframes, ignore_index=True)

    # Add spray angle
    team_filtered_angles = add_spray_angle(team_at_pitch)

    # Drop deprecated columns
    columns_to_drop = [
        'spin_rate_deprecated', 'break_angle_deprecated', 'break_length_deprecated',
        'tfs_deprecated', 'tfs_zulu_deprecated'
    ]

    team_filtered_clean = team_filtered_angles.drop(columns_to_drop, axis=1)

    return team_filtered_clean
'''