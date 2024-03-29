'''
This code presents an approach for implementing the gravitational field
produced by a rectangular prism by using the analytical formulas of
Nagy et al (2000, 2002). This code is highly inspired on
[Harmonica](https://www.fatiando.org/harmonica/latest/index.html)
(Uieda et al, 2020). It makes use of the modified arctangent function proposed
by Fukushima (2020, eq. 72).

References

* Nagy, D., Papp, G., and Benedek, J. (2000). The gravitational potential and
    its derivatives for the prism: Journal of Geodesy, 74, 552–560,
    http://doi.org/10.1007/s001900000116.
* Nagy, D., Papp, G., and Benedek, J. (2002). Corrections to "The gravitational
    potential and its derivatives for the prism": Journal of Geodesy, 76, 475,
    http://doi.org/10.1007/s00190-002-0264-7
* Fukushima, T. (2020). Speed and accuracy improvements in standard algorithm
    for prismatic gravitational field. Geophysical Journal International,
    222(3), 1898–1908. http://doi.org/10.1093/gji/ggaa240
* Uieda, Leonardo, Soler, Santiago R., Pesce, Agustina, Oliveira Jr,
    Vanderlei C, and Shea, Nicholas. (2020, February 27). Harmonica: Forward
    modeling, inversion, and processing gravity and magnetic data
    (Version v0.1.0). Zenodo. http://doi.org/10.5281/zenodo.3628742
'''


import numpy as np
from numba import njit

#: The magnetic permeability of free space in Henry*m^{-1}
MAGNETIC_PERM = 0.000001256

@njit
def safe_atan2(y, x):
    """
    Principal value of the arctangent expressed as a two variable function

    This modification has to be made to the arctangent function so the
    gravitational field of the prism satisfies the Poisson's equation.
    Therefore, it guarantees that the fields satisfies the symmetry properties
    of the prism. This modified function has been defined according to
    Fukushima (2020, eq. 72).
    """
    if x != 0:
        result = np.arctan(y / x)
    else:
        if y > 0:
            result = np.pi / 2
        elif y < 0:
            result = -np.pi / 2
        else:
            result = 0
    return result

@njit
def safe_log(x):
    """
    Modified log to return 0 for log(0).
    The limits in the formula terms tend to 0.
    """
    if np.abs(x) < 1e-10:
        result = 0
    else:
        result = np.log(x)
    return result

def _check_prisms(prisms):
    """
    Check if prisms boundaries are well defined

    Parameters
    ----------
    prisms : 2d-array
        Array containing the boundaries of the prisms in the following order:
        ``w``, ``e``, ``s``, ``n``, ``top``, ``bottom``.
        The array must have the following shape: (``n_prisms``, 6), where
        ``n_prisms`` is the total number of prisms.
        This array of prisms must have valid boundaries.
        Run ``_check_prisms`` before.
    """
    west, east, south, north, top, bottom = tuple(prisms[:, i] for i in range(6))
    err_msg = "Invalid prism or prisms. "
    bad_we = west > east
    bad_sn = south > north
    bad_bt = top > bottom
    if bad_we.any():
        err_msg += "The west boundary can't be greater than the east one.\n"
        for prism in prisms[bad_we]:
            err_msg += "\tInvalid prism: {}\n".format(prism)
        raise ValueError(err_msg)
    if bad_sn.any():
        err_msg += "The south boundary can't be greater than the north one.\n"
        for prism in prisms[bad_sn]:
            err_msg += "\tInvalid prism: {}\n".format(prism)
        raise ValueError(err_msg)
    if bad_bt.any():
        err_msg += "The top boundary can't be greater than the bottom one.\n"
        for prism in prisms[bad_bt]:
            err_msg += "\tInvalid prism: {}\n".format(prism)
        raise ValueError(err_msg)

def magnetics(coordinates,prisms,intensities,directions,field):
    """
    Computing the magnetic field effect generated by a rectangular prism.
    """
    
    kernels = {"b_z": kernel_b_z,
               "b_x": kernel_b_x,
               "b_y": kernel_b_y}
    
    # Checking input field
    if field not in kernels:
        raise ValueError("Gravitational field {} not recognized".format(field))

    # Checking input parameters
    if coordinates.ndim != 2:
        raise ValueError(
            "coordinates ndim ({}) ".format(coordinates.ndim)
            + "not equal to 2"
        )
    if coordinates.shape[0] != 3:
        raise ValueError(
            "Number of lines in coordinates ({}) ".format(coordinates.shape[0])
            + "not equal to 3"
        )
    if prisms.ndim != 2:
        raise ValueError(
            "prisms ndim ({}) ".format(prisms.ndim)
            + "not equal to 2"
        )
    if prisms.shape[1] != 6:
        raise ValueError(
            "Number of columns in prisms ({}) ".format(prisms.shape[1])
            + "not equal to 6"
        )
    if intensities.ndim != 1:
        raise ValueError(
            "intensities ndim ({}) ".format(intensities.ndim)
            + "not equal to 1"
        )
    if intensities.size != prisms.shape[0]:
        raise ValueError(
            "Number of elements in intensities ({}) ".format(intensities.size)
            + "mismatch the number of prisms ({})".format(prisms.shape[0])
        )
    

    _check_prisms(prisms)

    # Create the array to store the result
    result = np.zeros(coordinates[0].size, dtype="float64")

    # Compute magnetic field
    jit_magnetic(coordinates,prisms,intensities,directions,kernels[field],result)
    result *= (MAGNETIC_PERM/(4*np.pi))
    # Convert from T to nanoTesla
    if field in ["b_z","b_x","b_y"]:
        result *= 1e9
    return result

@njit
def jit_magnetic(coordinates,prisms,intensities,directions,kernel,out):
    """
    Compute magnetic field at the observation points
    """
    # Iterate over coordinates
    for l in range(coordinates[0].size):
        # Iterate over prisms
        for m in range(prisms.shape[0]):
            # Iterate over the prism boundaries
            for i in range(2,0,-1):
                for j in range(2,0,-1):
                    for k in range(2,0,-1):
                        Y = prisms[m, -1 + j] - coordinates[0, l]
                        X = prisms[m, 1 + i] - coordinates[1, l]
                        Z = prisms[m, 3 + k] - coordinates[2, l]
                        out[l] += (intensities[m] * (-1) ** (i + j + k)*kernel(Y, X, Z,directions[m]))

@njit
def kernel_xx(Y, X, Z):
    """
    Kernel xx for second derivative of the potential generated by a prism
    """
    radius = np.sqrt(Y ** 2 + X ** 2 + Z ** 2)
    kernel = (- safe_atan2(Y * Z, X * radius) )
    return kernel

@njit
def kernel_yy(Y, X, Z):
    """
    Kernel yy for second derivative of the potential generated by a prism
    """
    radius = np.sqrt(Y ** 2 + X ** 2 + Z ** 2)
    kernel = (- safe_atan2(X * Z, Y * radius) )
    return kernel

@njit
def kernel_zz(Y, X, Z):
    """
    Kernel zz for second derivative of the potential generated by a prism
    """
    radius = np.sqrt(Y ** 2 + X ** 2 + Z ** 2)
    kernel = (- safe_atan2(X * Y, Z * radius) )
    return kernel

@njit
def kernel_xy(Y, X, Z):
    """
    Kernel xy for second derivative of the potential generated by a prism
    """
    radius = np.sqrt(Y ** 2 + X ** 2 + Z ** 2)
    kernel = (safe_log(Z + radius) )
    return kernel

@njit
def kernel_xz(Y, X, Z):
    """
    Kernel xz for second derivative of the potential generated by a prism
    """
    radius = np.sqrt(Y ** 2 + X ** 2 + Z ** 2)
    kernel = (safe_log(Y + radius) )
    return kernel

@njit
def kernel_yz(Y, X, Z):
    """
    Kernel yz for second derivative of the potential generated by a prism
    """
    radius = np.sqrt(Y ** 2 + X ** 2 + Z ** 2)
    kernel = (safe_log(X + radius) )
    return kernel

@njit
def kernel_b_z(Y, X, Z,direction):
    """
    Vertical component of the magnetic field generated by a prism
    """
    
    inclination,declination = direction
    jx = np.cos(np.deg2rad(inclination))*np.cos(np.deg2rad(declination))
    jy = np.cos(np.deg2rad(inclination))*np.sin(np.deg2rad(declination))
    jz = np.sin(np.deg2rad(inclination))

    kernel = jx*kernel_xz(Y,X,Z) + jy*kernel_yz(Y,X,Z) + jz*kernel_zz(Y,X,Z)
    return kernel

@njit
def kernel_b_x(Y, X, Z,direction):
    """
    Computing x component of the magnetic field generated by a prism
    """    
    inclination,declination = direction
    jx = np.cos(np.deg2rad(inclination))*np.cos(np.deg2rad(declination))
    jy = np.cos(np.deg2rad(inclination))*np.sin(np.deg2rad(declination))
    jz = np.sin(np.deg2rad(inclination))

    kernel = jx*kernel_xx(Y,X,Z) + jy*kernel_xy(Y,X,Z) + jz*kernel_xz(Y,X,Z)
    return kernel

@njit
def kernel_b_y(Y, X, Z,direction):
    """
    Computing y component of the magnetic field generated by a prism
    """
    inclination,declination = direction
    jx = np.cos(np.deg2rad(inclination))*np.cos(np.deg2rad(declination))
    jy = np.cos(np.deg2rad(inclination))*np.sin(np.deg2rad(declination))
    jz = np.sin(np.deg2rad(inclination))

    kernel = jx*kernel_xy(Y,X,Z) + jy*kernel_yy(Y,X,Z) + jz*kernel_yz(Y,X,Z)
    return kernel
