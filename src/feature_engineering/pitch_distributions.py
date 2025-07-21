import pandas as pd


'''
def get_team_pitch_statistics(df: pd.DataFrame):
    """
    Calculate team-level pitch type distributions and characteristics from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be utilized.
    Returns:
        pd.DataFrame: Summary statistics of home_run data
    """
    # Group by 'pitch_type' and calculate required statistics
    grouped = df.groupby('pitch_type').agg(
        count=('pitch_type', 'size'),

        avg_release_speed=('release_speed', 'mean'),
        std_release_speed=('release_speed', 'std'),

        avg_release_spin_rate=('release_spin_rate', 'mean'),
        std_release_spin_rate=('release_spin_rate', 'std'),

        avg_release_pos_x=('release_pos_x', 'mean'),
        std_release_pos_x=('release_pos_x', 'std'),

        avg_release_pos_y=('release_pos_y', 'mean'),
        std_release_pos_y=('release_pos_y', 'std'),

        avg_release_pos_z=('release_pos_z', 'mean'),
        std_release_pos_z=('release_pos_z', 'std'),

        avg_pfx_x=('pfx_x', 'mean'),
        std_pfx_x=('pfx_x', 'std'),

        avg_pfx_z=('pfx_z', 'mean'),
        std_pfx_z=('pfx_z', 'std'),

        avg_plate_x=('plate_x', 'mean'),
        std_plate_x=('plate_x', 'std'),

        avg_plate_z=('plate_z', 'mean'),
        std_plate_z=('plate_z', 'std'),

        avg_vx0=('vx0', 'mean'),
        std_vx0=('vx0', 'std'),

        avg_vy0=('vy0', 'mean'),
        std_vy0=('vy0', 'std'),

        avg_vz0=('vz0', 'mean'),
        std_vz0=('vz0', 'std'),

        avg_ax=('ax', 'mean'),
        std_ax=('ax', 'std'),

        avg_ay=('ay', 'mean'),
        std_ay=('ay', 'std'),
        
        avg_az=('az', 'mean'),
        std_az=('az', 'std'),

        avg_effective_speed=('effective_speed', 'mean'),
        std_effective_speed=('effective_speed', 'std'),

        avg_release_extension=('release_extension', 'mean'),
        std_release_extension=('release_extension', 'std')
    ).reset_index()

    # Calculate total count and percentage for each pitch type
    total_count = grouped['count'].sum()
    grouped['percentage'] = (grouped['count'] / total_count) * 100

    # Sort by count in descending order
    grouped = grouped.sort_values(by='count', ascending=False)

    return grouped
'''

'''
def get_player_pitch_statistics(df: pd.DataFrame):
    """
    Calculate player-level pitch type distributions and characteristics from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be utilized.
    Returns:
        pd.DataFrame: Summary statistics of home_run data
    """
    # Group by 'pitch_type' and calculate required statistics
    grouped = df.groupby(['pitch_type', 'player_name']).agg(
        count=('pitch_type', 'size'),

        avg_release_speed=('release_speed', 'mean'),
        std_release_speed=('release_speed', 'std'),

        avg_release_spin_rate=('release_spin_rate', 'mean'),
        std_release_spin_rate=('release_spin_rate', 'std'),

        avg_release_pos_x=('release_pos_x', 'mean'),
        std_release_pos_x=('release_pos_x', 'std'),

        avg_release_pos_y=('release_pos_y', 'mean'),
        std_release_pos_y=('release_pos_y', 'std'),

        avg_release_pos_z=('release_pos_z', 'mean'),
        std_release_pos_z=('release_pos_z', 'std'),

        avg_pfx_x=('pfx_x', 'mean'),
        std_pfx_x=('pfx_x', 'std'),

        avg_pfx_z=('pfx_z', 'mean'),
        std_pfx_z=('pfx_z', 'std'),

        avg_plate_x=('plate_x', 'mean'),
        std_plate_x=('plate_x', 'std'),

        avg_plate_z=('plate_z', 'mean'),
        std_plate_z=('plate_z', 'std'),

        avg_vx0=('vx0', 'mean'),
        std_vx0=('vx0', 'std'),

        avg_vy0=('vy0', 'mean'),
        std_vy0=('vy0', 'std'),

        avg_vz0=('vz0', 'mean'),
        std_vz0=('vz0', 'std'),

        avg_ax=('ax', 'mean'),
        std_ax=('ax', 'std'),

        avg_ay=('ay', 'mean'),
        std_ay=('ay', 'std'),
        
        avg_az=('az', 'mean'),
        std_az=('az', 'std'),

        avg_effective_speed=('effective_speed', 'mean'),
        std_effective_speed=('effective_speed', 'std'),

        avg_release_extension=('release_extension', 'mean'),
        std_release_extension=('release_extension', 'std')
    ).reset_index()

    # Calculate total count and percentage for each pitch type
    total_count = grouped['count'].sum()
    grouped['percentage'] = (grouped['count'] / total_count) * 100

    # Sort by count in descending order
    grouped = grouped.sort_values(by='player_name', ascending=False)

    return grouped
'''