import math
from typing import List
import importlib


from . import calculate_trajectory
importlib.reload(calculate_trajectory)
from .calculate_trajectory import *

def simulate(
        t: float, omega_t: float, v_t: float, theta: float, phi: float, phi_s: float,
        positions: List[float], C: float, m: float, default_conditions: List[float], 
        g: float, dt: float, Tau: float):
    
    """
    Simulate path of baseball in each time step
    
    Args:
        t (float): Current time step (s)
        omega_t (float): Total spin rate (rad/s)
        v_t (float): Velocity magnitude (mph)
        theta (float): Launch angle (degrees)
        phi (float): Spray angle (degrees)
        phi_s (float): Spin axis angle (degrees)
        positions (List[float], optional): Initial position ball is struck [x0, y0, z0] (m)
        C (float, optional): Circumference (in)
        m (float, optional): Mass (oz)
        default_conditions (List[float]): [temp (deg F), pressure (in Hg), elevation (ft), humidity (%)]
        g (float, optional): Gravitational acceleration (m/s^2)
        dt (float, optional): Time step (s)
        Tau (float, optional): Total simulation time
    Returns:
        Dict[float] = [float, List[float], List[float], List[float]]: [time] (s) = [positions (m), component velocities (m/s), component accelerations (m/s^2)]
    """

    [K, coeff, radius, omega_t, coord_spins, coord_velos, accelerations] = calculate_values(default_conditions, v_t, omega_t, theta, phi, phi_s, C, m, g)
    trajectory = {}

    while positions[2] >= 0:
        trajectory[round(t,4)] = [positions, coord_velos, accelerations]
        [t, positions, coord_velos, coeff, accelerations] = iterate_values(K, coeff, radius, omega_t, coord_spins, coord_velos, accelerations, positions, g, t, dt, Tau)

    return trajectory


def simulate_row(row: List[float]):

    """
    Simulate baseball trajectory given a pitch

    Args:
        row (List[float]): Row representing a given hit 
    Returns:
        Dict[float] = [float, List[float], List[float], List[float]]: [time] (s) = [positions (m), component velocities (m/s), component accelerations (m/s^2)]
    """


    t = 0 # s
    omega_t = float(row[['release_spin_rate']].iloc[0]) # rpm
    v_t = float(row[['launch_speed']].iloc[0]) # mph
    theta = float(row[['launch_angle']].iloc[0]) # deg
    phi = float(row[['spray_angle']].iloc[0]) # deg
    phi_s = float(row[['spin_axis']].iloc[0]) # deg
    positions = [0, 0.6096, 0.9144] # m
    C = 9.125 # in
    m = 5.125 # oz
    default_conditions = [70, 29.92, 15, 50] # [deg F, inHg, ft, %]
    g = 9.81 # m/s^2
    dt = 0.005 # s
    Tau = 30 # s

    return simulate(t, omega_t, v_t, theta, phi, phi_s, positions, C, m, default_conditions, g, dt, Tau)
