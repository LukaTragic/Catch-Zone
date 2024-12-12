import math
from typing import List


def get_air_density(default_conditions: List[float]) -> float:
    """
    Calculate air density based on environmental conditions.
    
    Args:
        default_conditions (List[float]): [temp (deg F), pressure (in Hg), elevation (ft), humidity (%)]
    Returns:
        float: Air density (kg/m^3)
    """
    temp, pressure, elev, humidity = default_conditions
    temp_c = (5/9) * (temp - 32)
    elev_m = elev / 3.2808
    svp = 4.5841 * (math.e**((18.687 - (temp_c/234.5)) * temp_c / (257.14 + temp_c)))
    bar_pressure = pressure * 1000 / 39.37
    
    rho = 1.2929 * (273 / (temp_c + 273) * 
           (bar_pressure * math.e**(-0.0001217 * elev_m) - 
            0.3783 * humidity * svp / 100) / 760)
    
    return rho


def get_constant(rho: float, area: float, mass: float) -> float:
    """
    Calculate the constant K for aerodynamic equations.

    Args:
        rho (float): Air density (kg/m^3)
        area (float): Cross-sectional area (m^2)
        mass (float): Mass (kg)
    Returns:
        float: Aerodynamic constant K (1/m)
    """
    return (rho * area) / (2 * mass)


def get_spin(omega_t: float, phi_s: float) -> List[float]:
    """
    Calculate spin components.
    
    Args:
        omega_t (float): Total spin rate (rad/s)
        phi_s (float): Spin axis angle (radians)
    Returns:
        List[float]: [backSpin, sideSpin, gyroSpin] (rad/s)
    """
    omega_b = omega_t * math.cos(phi_s)
    omega_s = omega_t * math.sin(phi_s)
    omega_g = 0
    return [omega_b, omega_s, omega_g]


def get_coordinate_spin(
    omega_b: float, 
    omega_s: float, 
    omega_g: float, 
    phi: float, 
    theta: float
) -> List[float]:
    """
    Calculate spin coordinates.
    
    Args:
        omega_b (float): Back spin (rad/s)
        omega_s (float): Side spin (rad/s)
        omega_g (float): Gyro spin (rad/s)
        phi (float): Spray angle (radians)
        theta (float): Launch angle (radians)
    Returns:
        List[float]: Spin coordinates [omega_x, omega_y, omega_z] (rad/s)
    """
    omega_x = (
        omega_b * math.cos(phi) - 
        omega_s * math.sin(theta) * math.sin(phi) + 
        omega_g * math.cos(theta) * math.sin(phi)
    )
    omega_y = (
        -omega_b * math.sin(phi) - 
        omega_s * math.sin(theta) * math.cos(phi) + 
        omega_g * math.cos(theta) * math.cos(phi)
    )
    omega_z = omega_s * math.cos(theta) + omega_g * math.sin(theta)
    
    return [omega_x, omega_y, omega_z]


def get_velocities(v_t: float, theta: float, phi: float) -> List[float]:
    """
    Calculate velocity components.
    
    Args:
        v_t (float): Velocity magnitude (m/s)
        theta (float): Launch angle (radians)
        phi (float): Spray angle (radians)
    Returns:
        List[float]: Velocity components [v_x, v_y, v_z] (m/s)
    """
    v_x = v_t * math.cos(theta) * math.sin(phi)
    v_y = v_t * math.cos(theta) * math.cos(phi)
    v_z = v_t * math.sin(theta)

    return [v_x, v_y, v_z]


def get_drag_coefficient(omega_t: float, decay: float = 1.0) -> float:
    """
    Calculate drag coefficient.

    Args:
        omega_t (float): Spin rate (rad/s)
        decay (float, optional): Decay factor
    Returns:
        float: Drag coefficient
    """
    cd0 = 0.3008
    cd_spin = 0.0292
    return cd0 + ((cd_spin * omega_t) / 1000) * decay


def get_lift_coefficient(r: float, omega_t: float, v_t: float, decay: float = 1.0) -> float:
    """
    Calculate lift coefficient.

    Args: 
        r (float): Radius (m)
        omega_t (float): Spin rate (rad/s)
        v_t (float): Velocity magnitude (m/s)
        decay (float, optional): Decay factor
    Returns:
        float: Lift coefficient
    """
    cl0 = 0.583
    cl1 = 2.333
    cl2 = 1.120
    s = (r * omega_t / v_t) * decay
    return (cl2 * s) / (cl0 + cl1 * s)


def get_a_drag(K: float, cd: float, v_t: float, v_x: float, v_y: float, v_z: float) -> List[float]:
    """
    Calculate drag acceleration components

    Args:
        K (float): Aerodynamic constant
        cd (float): Drag coefficient
        v_t (float): Velocity magnitude (m/s)
        v_x (float): Velocity in x-direction (m/s)
        v_y (float): Velocity in y-direction (m/s)
        v_z (float): Velocity in z-direction (m/s)
    Returns:
        List[float]: Drag acceleration components [aDrag_x, aDrag_y, aDrag_z] (m/s^2)
    """
    a_drag_x = -K * cd * v_t * v_x
    a_drag_y = -K * cd * v_t * v_y
    a_drag_z = -K * cd * v_t * v_z
    return [a_drag_x, a_drag_y, a_drag_z]


def get_a_magnus(
        K: float, cl: float, 
        v_t: float, v_x: float, v_y: float, v_z: float, 
        omega_t: float, omega_x: float, omega_y: float, omega_z: float) -> List[float]:
    """
    Calculate magnus acceleration components

    Args:
        K (float): Aerodynamic constant (1/m)
        cl (float): Lift coefficient
        v_t (float): Velocity magnitude (m/s)
        v_x (float): Velocity in x-direction (m/s)
        v_y (float): Velocity in y-direction (m/s)
        v_z (float): Velocity in z-direction (m/s)
        omega_t (float): Total spin rate (rad/s)
        omega_x (float): Spin rate in x-direction (rad/s)
        omega_y (float): Spin rate in y-direction (rad/s)
        omega_z (float): Spin rate in z-direction (rad/s)
    Returns:
        List[float]: Magnus acceleration components [a_mag_x, a_mag_y, a_mag_z] (m/s^2)
    """
    a_mag_x = K*cl*v_t*((omega_y*v_z - omega_z*v_y))/omega_t
    a_mag_y = K*cl*v_t*((omega_z*v_x - omega_x*v_z))/omega_t
    a_mag_z = (K*cl*v_t*(((omega_x*v_y - omega_y*v_x))/omega_t))
    return [a_mag_x, a_mag_y, a_mag_z]