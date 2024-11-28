# Import libraries 
import pybaseball
from pybaseball import statcast_batter
from pybaseball.datahelpers.statcast_utils import add_spray_angle


import pandas as pd
import matplotlib.pyplot as plt
from Functions.webScrape import getRoster
pybaseball.cache.enable()


def getTeamHomeRuns(currTeam):
    teamRoster = getRoster(currTeam)
    teamRosterIDs = list(teamRoster.keys())

    dataframes = []

    for player_id in teamRosterIDs:
        temp_df = statcast_batter('2024-02-26', '2024-10-30', player_id)
        dataframes.append(temp_df)

    # Concatenate all at once
    teamAtBat = pd.concat(dataframes, ignore_index=True)

    #teamAtHome = teamAtBat.loc[teamAtBat['home_team'] == currTeam]
    teamHomeRuns= teamAtBat.loc[teamAtBat['events'] == 'home_run']

    [
        'pitch_type', 'game_date', 'release_speed', 'release_pos_x', 'release_pos_z', 'player_name', 
        'batter', 'pitcher', 'events', 'description', 'spin_dir', 'spin_rate_deprecated', 'break_angle_deprecated',
        'break_length_deprecated', 'zone', 'des', 'game_type', 'stand', 'p_throws', 'home_team', 'away_team', 
        'type', 'hit_location', 'bb_type', 'balls', 'strikes', 'game_year', 'pfx_x', 'pfx_z', 'plate_x', 
        'plate_z', 'on_3b', 'on_2b', 'on_1b', 'outs_when_up', 'inning', 'inning_topbot', 'hc_x', 'hc_y',
        'tfs_deprecated', 'tfs_zulu_deprecated', 'umpire', 'sv_id', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 
        'sz_top', 'sz_bot', 'hit_distance_sc', 'launch_speed', 'launch_angle', 'effective_speed', 'release_spin_rate', 
        'release_extension', 'game_pk', 'fielder_2', 'fielder_3', 'fielder_4', 'fielder_5', 'fielder_6', 
        'fielder_7', 'fielder_8', 'fielder_9', 'release_pos_y', 'estimated_ba_using_speedangle', 
        'estimated_woba_using_speedangle', 'woba_value', 'woba_denom', 'babip_value', 'iso_value', 'launch_speed_angle',
        'at_bat_number', 'pitch_number', 'pitch_name', 'home_score', 'away_score', 'bat_score', 'fld_score',
        'post_away_score', 'post_home_score', 'post_bat_score', 'post_fld_score', 'if_fielding_alignment',
        'of_fielding_alignment', 'spin_axis', 'delta_home_win_exp', 'delta_run_exp', 'bat_speed', 'swing_length', 
        'estimated_slg_using_speedangle', 'delta_pitcher_run_exp', 'hyper_speed', 'home_score_diff', 'bat_score_diff', 
        'home_win_exp', 'bat_win_exp', 'age_pit_legacy', 'age_bat_legacy', 'age_pit', 'age_bat', 'n_thruorder_pitcher', 
        'n_priorpa_thisgame_player_at_bat', 'pitcher_days_since_prev_game', 'batter_days_since_prev_game', 
        'pitcher_days_until_next_game', 'batter_days_until_next_game', 'api_break_z_with_gravity', 'api_break_x_arm', 
        'api_break_x_batter_in', 'arm_angle'
    ]

    teamHomeRunAngles = add_spray_angle(teamHomeRuns)
    teamHomeRunsClean = teamHomeRunAngles.drop([
                        'description', 'spin_rate_deprecated', 'break_angle_deprecated', 'break_length_deprecated', 'des', 'hit_location','game_year',
                        'on_3b', 'on_2b', 'on_1b', 'outs_when_up','inning', 'inning_topbot', 'tfs_deprecated', 'tfs_zulu_deprecated', 'umpire', 'sv_id', 
                        'fielder_2', 'fielder_3', 'fielder_4', 'fielder_5', 'fielder_6', 'fielder_7', 'fielder_8', 'fielder_9', 'home_score', 'away_score', 
                        'bat_score', 'fld_score', 'post_away_score', 'post_home_score', 'post_bat_score', 'post_fld_score', 'home_score_diff', 'bat_score_diff', 
                        'pitcher_days_since_prev_game', 'batter_days_since_prev_game', 'pitcher_days_until_next_game', 'batter_days_until_next_game'], axis=1)

    return teamHomeRunsClean