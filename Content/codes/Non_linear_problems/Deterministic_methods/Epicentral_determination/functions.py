import numpy as np

def time_arrival(x,y,x0,y0,vp,vs):
    '''
    Calculate the difference of time arrival for a set of stations.

    input

    x,y : arrays - Cartesian coordinates of stations
    p : array - parameter vector
    vp,vs : floats - seismic velocities

    return

    dt : array - time arrival for all stations

    '''
    if vp <= vs:
        raise ValueError('vp must be greater than vs')

    if x.size != y.size:
        raise ValueError('x and y must have the same dimension')

    if (vp!=0) & (vs!=0):
        alpha = (1./vs) - (1./vp)
    else:
        raise('vp and vs must have non-null')

    dt = alpha*(np.sqrt((x - x0)**2 + (y - y0)**2))
    return dt

def sensitivity(x,y,x0,y0,vp,vs):
    '''
    Calculate the sensitivity matrix.

    input

    x,y : arrays - Cartesian coordinates of stations
    p : array - parameter vector
    vp,vs : floats - seismic velocities

    return

    dt : array - time arrival for all stations

    '''
    if vp <= vs:
        raise ValueError('vp must be greater than vs')

    if x.size != y.size:
        raise ValueError('x and y must have the same dimension')

    if (vp!=0) & (vs!=0):
        alpha = (1./vs) - (1./vp)
    else:
        raise('vp and vs must have non-null')

    N = x.size
    A = np.zeros((N,2))
    A[:,0] = (x0 - x)*alpha/(np.sqrt((x - x0)**2 + (y - y0)**2))
    A[:,1] = (y0 - y)*alpha/(np.sqrt((x - x0)**2 + (y - y0)**2))
    return A

def solver(dobs,x,y,x0,y0,vp,vs,itmax,mu):
    '''
    Apply the Gauss-Newton Method to solve a non-linerar problem.

    input

    dobs: array - Observed data vector
    x,y : array - Cartesian coordinates of stations
    p : array - parameter vector
    vp,vs : floats - seismic velocities
    itmax : integer - maximum iteration for the code
    mu : float - parameter barrier

    return

    p0 : array - Epicenter estimation#

    '''
    eps = 1e-8

    p0 = np.array([x0,y0])
    px = [p0[0]]
    py = [p0[1]]
    phi_it = []
    iteration  = []

    for i in range(itmax):

        d0 = time_arrival(x,y,p0[0],p0[1],vp,vs)
        r0 = dobs - d0
        phi0 = np.sum(r0*r0) + mu*np.sum(p0*p0)

        A = sensitivity(x,y,p0[0],p0[1],vp,vs)
        AtA = np.dot(A.T,A)
        J = -np.dot(A.T,r0) + mu*np.dot(np.identity(2),p0)
        H = AtA + mu*np.identity(2)
        dp = np.linalg.solve(H,-J)
        p0 += dp

        d = time_arrival(x,y,p0[0],p0[1],vp,vs)
        r = dobs - d
        phi = np.sum(r*r) + mu*np.sum(p0*p0)

        r0 = r[:]
        phi0 = phi
        d0=d[:]

        px.append(p0[0])
        py.append(p0[1])
        iteration.append(i)
        phi_it.append(phi0)

    return p0,px,py,phi_it,iteration
