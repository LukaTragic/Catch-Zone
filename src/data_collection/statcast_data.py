import pybaseball
from pybaseball import statcast_batter
from pybaseball.datahelpers.statcast_utils import add_spray_angle

import pandas as pd
from typing import List
import importlib

from . import web_scraper
importlib.reload(web_scraper)
from .web_scraper import *

pybaseball.cache.enable()

def get_team_home_runs(curr_team: str, current: bool = True) -> pd.DataFrame:
    """
    Collect home run data for a specific team's roster.
    
    Args:
        curr_team (str): Team acronym
        current (bool): If current roster should be used

        
    Returns:
        pd.DataFrame: Cleaned home run data
    """
    # Get team roster
    team_roster = get_roster(curr_team, current)
    team_roster_ids = list(team_roster.keys())

    # Collect data for each player
    dataframes: List[pd.DataFrame] = []
    for player_id in team_roster_ids:
        try:
            temp_df = statcast_batter('2024-02-22', '2024-10-30', player_id)
            dataframes.append(temp_df)
        except Exception as e:
            print(f"Error collecting data for player {player_id}: {e}")

    # Combine dataframes
    if not dataframes:
        return pd.DataFrame()

    team_at_bat = pd.concat(dataframes, ignore_index=True)

    # Filter for home runs
    team_home_runs = team_at_bat.loc[team_at_bat['events'] == 'home_run']

    # Add spray angle
    team_home_run_angles = add_spray_angle(team_home_runs)

    # Drop deprecated columns
    columns_to_drop = [
        'spin_rate_deprecated', 'break_angle_deprecated', 'break_length_deprecated',
        'tfs_deprecated', 'tfs_zulu_deprecated'
    ]

    team_home_runs_clean = team_home_run_angles.drop(columns_to_drop, axis=1)

    return team_home_runs_clean