import math


def get_Spin(omega_b, omega_g, phi_s):
    omega_t = omega_b / math.cos(phi_s)
    omega_s = math.tan(phi_s) * omega_b
    return [omega_b, omega_s, omega_g]

def get_Coordinate_Spin(omega_b, omega_s, omega_g, phi, theta):
    omega_x = omega_b*math.cos(phi) - omega_s*math.sin(theta)*math.sin(phi) + omega_g*math.cos(theta)*math.sin(phi)
    omega_y = -omega_b*math.sin(phi) - omega_s*math.sin(theta)*math.cos(phi) + omega_g*math.cos(theta)*math.cos(phi)
    omega_z = omega_s*math.cos(theta) + omega_g*math.sin(theta)

    return [omega_x, omega_y, omega_z]

def get_Velocities(v_t, theta, phi):
    v_x = v_t * math.cos(theta) * math.sin(phi)
    v_y = v_t * math.cos(theta) * math.cos(phi)
    v_z = v_t * math.sin(theta)

    return [v_x, v_y, v_z]

def get_Constant(rho, A, m):
    return (rho * A) / (2 * m)

def get_Drag_Coefficient(omega, decay):
    cd0 = 0.3008
    cdSpin = 0.0292
    return cd0 + ((cdSpin*omega)/1000)  * decay

def get_Lift_Coefficient(r, omega, v_t, decay):
    cl0 = 0.583
    cl1 = 2.333
    cl2 = 1.120
    S = (r * omega / v_t) * decay
    return (cl2*S) / (cl0 + cl1*S)

def get_aDrag(K, cd, v_t, v_x, v_y, v_z):
    aDrag_x = -K*cd*v_t*v_x
    aDrag_y = -K*cd*v_t*v_y
    aDrag_z = -K*cd*v_t*v_z
    return [aDrag_x, aDrag_y, aDrag_z]

def get_aMag(K, cl, v_t, v_x, v_y, v_z, omega, omega_x, omega_y, omega_z, g):
    aMag_x = K*cl*v_t*((omega_y*v_z - omega_z*v_y))/omega
    aMag_y = K*cl*v_t*((omega_z*v_x - omega_x*v_z))/omega
    aMag_z = (K*cl*v_t*(((omega_x*v_y - omega_y*v_x))/omega))
    return [aMag_x, aMag_y, aMag_z]


def calculateValues(rho, C, m, omega_b, omega_g, theta, phi, phi_s, v_t, g):

    radius = C / (2*math.pi) * 0.0254
    area = math.pi * (radius**2)

    omega_b_rate = (omega_b / 60) * 2 * math.pi
    omega_g_rate = (omega_g / 60) * 2 * math.pi


    rad_theta = math.radians(theta)
    rad_phi = math.radians(phi)
    rad_phi_s = math.radians(phi_s)

    ms_v_t = v_t * 0.44704

    typeSpins = [backSpin, sideSpin, gyroSpin] = get_Spin(omega_b_rate, omega_g_rate, rad_phi_s)
    coordSpins = [spin_x, spin_y, spin_z] = get_Coordinate_Spin(backSpin, sideSpin, gyroSpin, rad_phi, rad_theta)

    coordVelocities = [v_x, v_y, v_z] = get_Velocities(ms_v_t, rad_theta, rad_phi)

    Konst = get_Constant(rho, area, m)

    spin_t = math.sqrt(omega_b_rate**2 + sideSpin**2 + omega_g_rate**2)
    spin_t_rpm = (spin_t / (2 * math.pi)) * 60

    c_d = get_Drag_Coefficient(spin_t_rpm, 1)
    c_l = get_Lift_Coefficient(radius, spin_t, ms_v_t, 1)

    coeff = [c_d, c_l]


    aDrag = [aDrag_x, aDrag_y, aDrag_z] = get_aDrag(Konst, c_d, ms_v_t, v_x, v_y, v_z)
    aMag = [aMag_x, aMag_y, aMag_z] = get_aMag(Konst, c_l, ms_v_t, v_x, v_y, v_z, spin_t, spin_x, spin_y, spin_z, g)

    accelerations = [a_x, a_y, a_z] = [aDrag_x + aMag_x, aDrag_y + aMag_y, aDrag_z + aMag_z - g]
    
    
    return [Konst, radius, spin_t, coordSpins, coordVelocities, accelerations, coeff]


def iterateValues(dt, t, Tau, Konst, radius, positions, spin_t, coordSpins, velocities, accelerations, coeff, g):

    t += dt

    [x0, y0, z0] = positions
    [vx, vy, vz] = velocities
    [ax, ay, az] = accelerations

    xi = x0 + vx*dt + 0.5 *ax*dt**2
    yi = y0 + vy*dt + 0.5 *ay*dt**2
    zi = z0 + vz*dt + 0.5 *az*dt**2

    newPositions = [xi, yi, zi]

    r_i = math.sqrt(xi**2 + yi**2)
    phi_i = math.atan2(yi, xi)
    vt = math.sqrt(vx**2 + vy**2 + vz**2)

    vx_i = vx + ax*dt
    vy_i = vy + ay*dt
    vz_i = vz + az*dt

    newVelocities = [vx_i, vy_i, vz_i] 
    vt_i = math.sqrt(vx_i**2 + vy_i**2 + vz_i**2)

    [spin_x, spin_y, spin_z] = coordSpins

    decayComponent = math.e**(-t/(Tau*100/vt_i))

    [cd, cl] = coeff
    spin_t_rpm = (spin_t / (2 * math.pi)) * 60
    cd_i = get_Drag_Coefficient(spin_t_rpm, decayComponent)
    cl_i = get_Lift_Coefficient(radius, spin_t, vt_i, decayComponent)

    newCoeff = [cd_i, cl_i]

    aDrag_i = [aDragx_i, aDragy_i, aDragz_i] = get_aDrag(Konst, cd_i, vt_i, vx_i, vy_i, vz_i)
    aMag_i = [aMagx_i, aMagy_i, aMagz_i] = get_aMag(Konst, cl_i, vt_i, vx_i, vy_i, vz_i, spin_t, spin_x, spin_y, spin_z, g)

    newAccelerations = [ax_i, ay_i, az_i] = [aDragx_i + aMagx_i, aDragy_i + aMagy_i, aDragz_i + aMagz_i - g]

    return [t, newPositions, newVelocities, newCoeff, newAccelerations]
