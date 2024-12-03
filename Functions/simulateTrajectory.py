import math
from trajectoryCalculate import *
from dataCollecting import *

def simulateTrajectory(positions, t, rho, C, m, omega_b, omega_g, theta, phi, phi_s, v_t, g, dt, Tau):
    # Step 1: Calculate initial values
    [Konst, radius, spin_t, coordSpins, coordVelocities, accelerations, coeff] = calculateValues(
        rho, C, m, omega_b, omega_g, theta, phi, phi_s, v_t, g
    )

    trajectory = {}  # Store trajectory data

    while positions[2] >= 0:  # Continue until the z-coordinate (height) reaches 0 or below

        # Step 2: Record the current state
        trajectory[round(t,2)] = [positions, coordVelocities, accelerations]

        # Step 3: Update values using iterateValues
        [t, positions, coordVelocities, coeff, accelerations] = iterateValues(
            dt, t, Tau, Konst, radius, positions, spin_t, coordSpins, coordVelocities, accelerations, coeff, g
        )

    return trajectory

def simulateRow(row):
    positions = [0, 0.6096, 0.9144] # m
    t = 0 # s    
    rho = 1.194 # kg/m**3
    C = 9.136 # in
    m = 0.14529131 # kg
    omega_b = float(row[['release_spin_rate']].iloc[0]) # rpm
    omega_g = 0 # rpm
    theta = float(row[['launch_angle']].iloc[0]) # deg
    phi = float(row[['spray_angle']].iloc[0]) # deg
    phi_s = float(row[['spin_axis']].iloc[0]) # deg
    v_t = float(row[['launch_speed']].iloc[0]) # mph
    g = 9.8 # m/s**2
    dt = 0.01 # s
    Tau = 30 # s

    return simulateTrajectory(positions, t, rho, C, m, omega_b, omega_g, theta, phi, phi_s, v_t, g, dt, Tau)

row1 = getTeamHomeRuns("NYY").head(1)

print(simulateRow(row1)[4.6])