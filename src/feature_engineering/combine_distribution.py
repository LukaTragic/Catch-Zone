import pandas as pd
import numpy as np
from typing import Dict

def calculate_pitch_stats(pitcher_weights: Dict[str, float], player_pitches: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate pitch statistics weighted by pitcher appearance probabilities using pre-aggregated pitcher stats.
    Includes weighted means, standard deviations, pitch type counts, and overall likelihood.

    Args:
    pitcher_weight (Dict[str, float]): Dictionary of pitcher names and their appearance weights
    player_pitches (pd.DataFrame): Pre-aggregated pitcher statistics

    Returns:
    pd.DataFrame: Weighted pitch statistics across all pitchers including standard deviations, pitch type counts, and overall likelihood
    """
    pitch_stats = {}
    squared_diff_stats = {}
    pitch_type_counts = {}  # New dictionary to track pitch type counts
    
    total_weight = sum(pitcher_weights.values())

    for pitcher_name, weight in pitcher_weights.items():
        pitcher_data = player_pitches[player_pitches['player_name'] == pitcher_name]

        if pitcher_data.empty:
            continue

        for _, row in pitcher_data.iterrows():
            pitch_type = row['pitch_type']

            # Initialize pitch type in the dictionary if it doesn't exist
            if pitch_type not in pitch_stats:
                pitch_stats[pitch_type] = {
                    'usage_pct': 0,
                    'overall_likelihood': 0,
                    'release_speed': 0,
                    'spin_rate': 0,
                    'release_pos_x': 0,
                    'release_pos_y': 0,
                    'release_pos_z': 0,
                    'pfx_x': 0,
                    'pfx_z': 0,
                    'plate_x': 0,
                    'plate_z': 0,
                    'vx0': 0,
                    'vy0': 0,
                    'vz0': 0,
                    'ax': 0,
                    'ay': 0,
                    'az': 0,
                    'effective_speed': 0,
                    'release_extension': 0,
                }
                squared_diff_stats[pitch_type] = {
                    'release_speed': 0,
                    'spin_rate': 0,
                    'release_pos_x': 0,
                    'release_pos_y': 0,
                    'release_pos_z': 0,
                    'pfx_x': 0,
                    'pfx_z': 0,
                    'plate_x': 0,
                    'plate_z': 0,
                    'vx0': 0,
                    'vy0': 0,
                    'vz0': 0,
                    'ax': 0,
                    'ay': 0,
                    'az': 0,
                    'effective_speed': 0,
                    'release_extension': 0,
                }
                pitch_type_counts[pitch_type] = 0  # Initialize the count for the pitch type

            # Calculate weighted means
            weighted_usage = row['percentage'] * weight
            
            # Update means
            pitch_stats[pitch_type]['usage_pct'] += weighted_usage
            pitch_stats[pitch_type]['overall_likelihood'] += weighted_usage

            # Update the pitch type count
            pitch_type_counts[pitch_type] += row['count']  # Add the count of this pitch type

            stats_mapping = {
                'release_speed': 'avg_release_speed',
                'spin_rate': 'avg_release_spin_rate',
                'release_pos_x': 'avg_release_pos_x',
                'release_pos_y': 'avg_release_pos_y',
                'release_pos_z': 'avg_release_pos_z',
                'pfx_x': 'avg_pfx_x',
                'pfx_z': 'avg_pfx_z',
                'plate_x': 'avg_plate_x',
                'plate_z': 'avg_plate_z',
                'vx0': 'avg_vx0',
                'vy0': 'avg_vy0',
                'vz0': 'avg_vz0',
                'ax': 'avg_ax',
                'ay': 'avg_ay',
                'az': 'avg_az',
                'effective_speed': 'avg_effective_speed',
                'release_extension': 'avg_release_extension'
            }

            std_mapping = {
                'release_speed': 'std_release_speed',
                'spin_rate': 'std_release_spin_rate',
                'release_pos_x': 'std_release_pos_x',
                'release_pos_y': 'std_release_pos_y',
                'release_pos_z': 'std_release_pos_z',
                'pfx_x': 'std_pfx_x',
                'pfx_z': 'std_pfx_z',
                'plate_x': 'std_plate_x',
                'plate_z': 'std_plate_z',
                'vx0': 'std_vx0',
                'vy0': 'std_vy0',
                'vz0': 'std_vz0',
                'ax': 'std_ax',
                'ay': 'std_ay',
                'az': 'std_az',
                'effective_speed': 'std_effective_speed',
                'release_extension': 'std_release_extension'
            }

            # Update means and track squared differences for std calculation
            for stat_name, col_name in stats_mapping.items():
                value = row[col_name]
                pitch_stats[pitch_type][stat_name] += value * weighted_usage

                if std_mapping[stat_name] in row:
                    std_value = row[std_mapping[stat_name]]
                    if not pd.isna(std_value):
                        squared_diff_stats[pitch_type][stat_name] += (std_value ** 2) * weighted_usage

    # Create DataFrame and normalize means
    result_df = pd.DataFrame.from_dict(pitch_stats, orient='index')

    # Add the pitch type counts to the result DataFrame
    result_df['count'] = result_df.index.map(pitch_type_counts)

    # Normalize overall likelihood to sum to 100%
    total_likelihood = result_df['overall_likelihood'].sum()
    result_df['overall_likelihood'] = (result_df['overall_likelihood'] / total_likelihood * 100)

    # Normalize weighted statistics and calculate final standard deviations
    stats_to_normalize = [
        'release_speed', 'spin_rate', 'release_pos_x', 'release_pos_y', 'release_pos_z',
        'pfx_x', 'pfx_z', 'plate_x', 'plate_z', 'vx0', 'vy0', 'vz0', 
        'ax', 'ay', 'az', 'effective_speed', 'release_extension'
    ]

    for stat in stats_to_normalize:
        result_df[stat] = result_df[stat] / result_df['usage_pct']

        std_col = f'{stat}_std'
        result_df[std_col] = np.sqrt(
            pd.DataFrame.from_dict(squared_diff_stats, orient='index')[stat] / result_df['usage_pct']
        )

    result_df = result_df.sort_values('overall_likelihood', ascending=False)

    return result_df.round(4)
