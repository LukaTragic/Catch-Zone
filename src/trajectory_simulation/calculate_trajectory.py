import math
from typing import List
import importlib

from . import physics_calculations
importlib.reload(physics_calculations)
from .physics_calculations import *

def calculate_values(
        default_conditions: List[float], v_t: float, omega_t: float, 
        theta: float, phi: float, phi_s: float, C: float, m: float, g: float):
    """
    Perform initial calculations for aerodynamic simulation

    Args:
        default_conditions (List[float]): [temp (deg F), pressure (in Hg), elevation (ft), humidity (%)]
        omega_t (float): Total spin rate (rpm)
        v_t (float): Velocity magnitude (mph)
        theta (float): Launch angle (degrees)
        phi (float): Spray angle (degrees)
        phi_s (float): Spin axis angle (degrees)
        C (float, optional): Circumference (in)
        m (float, optional): Mass (oz)
        g (float, optional): Gravitational acceleration (m/s^2)
    Returns:
        float: Aerodynamic constant K (1/m)
        List[float]: Coefficients [drag coefficient, lift coefficient]
        float: Radius (m)
        float: Total spin rate (rad/s)
        List[float]: Velocity components [v_x, v_y, v_z] (m/s)
        List[float]: Acceleration components [a_x, a_y, a_z] (m/s)
    """

    rho = get_air_density(default_conditions)
    radius = (C / (2*math.pi)) * 0.0254 # Conversion from meters to inches
    area = math.pi * (radius**2)

    omega_t_rad = (omega_t / 60) * 2*math.pi # Conversion from rpm to rad/s
    [theta_rad, phi_rad, phi_s_rad] = [math.radians(i) for i in [theta, phi, phi_s]]
    v_t_ms = v_t * 0.44704 # Conversion from mph to m/s

    type_spins = [back_spin, side_spin, gyro_spin] = get_spin(omega_t_rad, phi_s_rad)
    coord_spins = [omega_x, omega_y, omega_z] = get_coordinate_spin(back_spin, side_spin, gyro_spin, phi_rad, theta_rad)
    coord_velos = [v_x, v_y, v_z] = get_velocities(v_t_ms, theta_rad, phi_rad)

    K = get_constant(rho, area, m*0.0283495) # Conversion from oz to kg

    cd = get_drag_coefficient(omega_t, 1.0)
    cl = get_lift_coefficient(radius, omega_t_rad, v_t_ms, 1.0)
    coeff = [cd, cl]

    [a_drag_x, a_drag_y, a_drag_z] = get_a_drag(K, cd, v_t, v_x, v_y, v_z)
    [a_mag_x, a_mag_y, a_mag_z] = get_a_magnus(K, cl, v_t_ms, v_x, v_y, v_z, omega_t_rad, omega_x, omega_y, omega_z)

    accelerations = [a_drag_x + a_mag_x, a_drag_y + a_mag_y, a_drag_z + a_mag_z -g]


    return [K, coeff, radius, omega_t, coord_spins, coord_velos, accelerations]

def iterate_values(
        K: float, coeff: List[float], radius: float, 
        omega_t: float, coord_spins: List[float], coord_velos: List[float], accelerations: List[float], 
        positions: List[float], g: float, t: float, dt: float, Tau: float):
    """
    Iterate upon initial calculations for aerodynamic solution
    
    Args:
        K (float): Aerodynamic constant (1/m)
        coeff (List[float]): Lift and Drag coefficients
        radius (float): Radius (m)
        omega_t (float): Total spin rate (rad/s)
        coord_spins (List[float]): Spin rate components [omega_x, omega_y, omega_z] (rad/s)
        coord_velos (List[float]): Velocity components [v_x, v_y, v_z] (m/s)
        accelerations (List[float]): Acceleration components [a_x, a_y, a_z] (m/s^2)
        positions (List[float], optional): Initial position ball is struck [x0, y0, z0] (m)
        g (float, optional): Gravitational acceleration (m/s^2)
        dt (float, optional): Time step (s)
        Tau (float, optional): Total simulation time
    Returns:
        float: New current time (s)
        List[float]: New current positions [xi, yi, zi] (m)
        List[float]: New current component velocities [vx_i, vy_i, vz_i] (m/s)
        List[float]: New current coefficients [drag coefficient, lift coefficient]
        List[float]: New current components accelerations [ax_i, ay_i, az_i] (m/s^2)
    """
    
    t += dt
    
    [cd, cl] = coeff
    [x0, y0, z0] = positions
    [omega_x, omega_y, omega_z] = coord_spins
    [vx, vy, vz] = coord_velos
    [ax, ay, az] = accelerations
    

    # Kinematics for new positions
    x_i = x0 + vx*dt + 0.5 *ax*dt**2
    y_i = y0 + vy*dt + 0.5 *ay*dt**2
    z_i = z0 + vz*dt + 0.5 *az*dt**2

    r_i = math.sqrt(x_i**2 + y_i**2)
    phi_i = math.atan2(y_i, x_i)
    omega_t_rad = (omega_t / 60) * 2 * math.pi # Conversion to rad/s

    vx_i = vx + ax*dt
    vy_i = vy + ay*dt
    vz_i = vz + az*dt
    vt_i = math.sqrt(vx_i**2 + vy_i**2 + vz_i**2)   

    decay_component = math.e**(-t/(Tau*100/vt_i)) # Decay component
    cd_i = get_drag_coefficient(omega_t, decay_component)
    cl_i = get_lift_coefficient(radius, omega_t_rad, vt_i, decay_component)

    [a_dragx_i, a_dragy_i, a_dragz_i] = get_a_drag(K, cd_i, vt_i, vx_i, vy_i, vz_i)
    [a_magx_i, a_magy_i, a_magz_i] = get_a_magnus(K, cl_i, vt_i, vx_i, vy_i, vz_i, omega_t_rad, omega_x, omega_y, omega_z)
    [ax_i, ay_i, az_i] = [a_dragx_i + a_magx_i, a_dragy_i + a_magy_i, a_dragz_i + a_magz_i - g]

    positions_i = [x_i, y_i, z_i]
    velocities_i = [vx_i, vy_i, vz_i]
    coeff_i = [cd_i, cl_i]
    accelerations_i = [ax_i, ay_i, az_i]

    return [t, positions_i, velocities_i, coeff_i, accelerations_i]

