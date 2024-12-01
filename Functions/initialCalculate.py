import math

def getTotalSpin(omega_b, phi_s):
    return omega_b / math.cos(phi_s)

def getSideSpin(omega_b, phi_s):
    return math.tan(phi_s) * omega_b

def getXSpin(omega_b, omega_s, omega_g, phi, theta):
    return omega_b*math.cos(phi) - omega_s*math.sin(theta)*math.sin(phi) + omega_g*math.cos(theta)*math.sin(phi)

def getYSpin(omega_b, omega_s, omega_g, phi, theta):
    return -omega_b*math.sin(phi) - omega_s*math.sin(theta)*math.cos(phi) + omega_g*math.cos(theta)*math.cos(phi)

def getZSpin(omega_s, omega_g, theta):
    return omega_s*math.cos(theta) + omega_g*math.sin(theta)

def get_initial_x_Velocity(v_t, theta, phi):
    return v_t * math.cos(theta) * math.sin(phi)

def get_initial_y_Velocity(v_t, theta, phi):
    return v_t * math.cos(theta) * math.cos(phi)

def get_initial_z_Velocity(v_t, theta):
    return v_t * math.sin(theta)

def getConstant(rho, A, m):
    return (rho * A) / (2 * m)

def getDragCoefficient(omega):
    cd0 = 0.3008
    cdSpin = 0.0292
    return cd0 + ((cdSpin*omega)/1000) *  9.549297 

def getLiftCoefficient(r, omega, v):
    cl0 = 0.583
    cl1 = 2.333
    cl2 = 1.120
    S = r * omega / v
    return (cl2 * S) / (cl0 + cl1*S)


def get_aDrag_x(K, cd, v, v_x):
    return -K*cd*v*v_x

def get_aDrag_y(K, cd, v, v_y):
    return -K*cd*v*v_y

def get_aDrag_z(K, cd, v, v_z):
    return -K*cd*v*v_z

def get_aMag_x(K, cl, v, omega_y, v_z, omega_z, v_y, omega):
    return K*cl*v*((omega_y*v_z - omega_z*v_y))/omega

def get_aMag_y(K, cl, v, omega_z, v_x, omega_x, v_z, omega):
    return K*cl*v*((omega_z*v_x - omega_x*v_z))/omega

def get_aMag_z(K, cl, v, omega_x, v_y, omega_y, v_x, omega, g):
    return K*cl*v*(((omega_x*v_y - omega_y*v_x))/omega) - g

def get_initial_x_acceleration(aDrag_x, aMag_x):
    return aDrag_x + aMag_x

def get_initial_y_acceleration(aDrag_y, aMag_y):
    return aDrag_y + aMag_y

def get_initial_z_acceleration(aDrag_z, aMag_z):
    return aDrag_z + aMag_z



def calculateValues(rho, C, m, omega_b, omega_g, theta, phi, phi_s, v_t, g):
    #rho kg/m^3
    #A m
    #m kg
    #omega_b 
    #v_t mphs


    radius = C / (2*math.pi) * 0.0254
    area = math.pi * (radius**2)

    omega_b_rate = (omega_b / 60) * 2 * math.pi
    omega_g_rate = (omega_g / 60) * 2 * math.pi


    rad_theta = math.radians(theta)
    rad_phi = math.radians(phi)
    rad_phi_s = math.radians(phi_s)

    ms_v_t = v_t * 0.44704

    sideSpin = getSideSpin(omega_b, rad_phi_s)

    v_x = get_initial_x_Velocity(ms_v_t, rad_theta, rad_phi)
    v_y = get_initial_y_Velocity(ms_v_t, rad_theta, rad_phi)
    v_z = get_initial_z_Velocity(ms_v_t, rad_theta)

    spin_x = getXSpin(omega_b_rate, sideSpin, omega_g_rate, rad_phi, rad_theta)
    spin_y = getYSpin(omega_b_rate, sideSpin, omega_g_rate, rad_phi, rad_theta)
    spin_z = getZSpin(sideSpin, omega_g_rate, rad_theta)

    Konst = getConstant(rho, area, m)
    spin = math.sqrt(omega_b_rate**2 + sideSpin**2 + omega_g_rate**2)
    c_d = getDragCoefficient(spin)
    c_l = getLiftCoefficient(radius, spin, ms_v_t)

    aDrag_x = get_aDrag_x(Konst, c_d, ms_v_t, v_x)
    aDrag_y = get_aDrag_y(Konst, c_d, ms_v_t, v_y)
    aDrag_z = get_aDrag_z(Konst, c_d, ms_v_t, v_z)

    aMag_x = get_aMag_x(Konst, c_l, ms_v_t, spin_y, v_z, spin_z, v_y, spin)
    aMag_y = get_aMag_y(Konst, c_l, ms_v_t, spin_z, v_x, spin_x, v_z, spin)
    aMag_z = get_aMag_z(Konst, c_l, ms_v_t, spin_x, v_y, spin_y, v_x, spin, g)


    a_x = get_initial_x_acceleration(aDrag_x, aMag_x)
    a_y = get_initial_y_acceleration(aDrag_y, aMag_y)
    a_z = get_initial_z_acceleration(aDrag_z, aMag_z)

    return [v_x, v_y, v_z, a_x, a_y, a_z]


print(calculateValues(1.194, 9.125, 0.14529131, 2500, 0, 27.5, 0, 0, 103, 9.8))

'''

def iterateValues(x0, y0, z0, dt, v_x, v_y, v_z, a_x, a_y, a_z):
    xi = x0 + v_x*dt + (a_x*dt**2)/2
    yi = y0 + v_y*dt + (a_y*dt**2)/2
    zi = z0 + v_z*dt + (a_z*dt**2)/2

    return [xi, yi, zi]

'''




