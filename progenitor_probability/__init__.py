from __future__ import print_function
import numpy as np
from scipy.io import FortranFile
from scipy.interpolate import griddata
import os


def progenitor_probability(density=None, sfr=None, mass=None, redshift=None):
    """
    Return the progenitor fraction for input values.
    >>> progenitor_probability(redshift=0.4, mass=10.8)
    0.266751184855
    """
    density = np.nan if density is None else density
    sfr = np.nan if sfr is None else sfr
    mass = np.nan if mass is None else mass
    redshift = np.nan if redshift is None else redshift

    values = [density, sfr, mass, redshift]

    if values.count(np.nan) > 3:
        raise ValueError('Incorrect number of arguments')

    # Read datacube
    f = FortranFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fractions.dat'))
    dims = f.read_record(dtype=np.int32)
    data = f.read_record(dtype=np.float32)
    data_size = np.product(dims)
    n_galaxies = np.reshape(data[0:data_size], dims, order='F')
    n_spiral_progenitors = np.reshape(data[data_size:2*data_size], dims, order='F')
    bins = np.stack([np.reshape(f.read_record(dtype=np.float32), dims, order='F') for _ in range(dims.size)], axis=0)

    # Marginalise over dimensions that are not specified
    while np.nan in values:
        i = values.index(np.nan)
        dims = np.delete(dims, i)
        values.pop(i)
        weights = n_galaxies
        n_galaxies = np.sum(n_galaxies, axis=i)
        n_spiral_progenitors = np.sum(n_spiral_progenitors, axis=i)
        bins = np.delete(np.nanmean(bins, axis=i+1), i, axis=0)
    data_size = np.product(dims)

    n_galaxies = np.reshape(n_galaxies, data_size)
    n_spiral_progenitors = np.reshape(n_spiral_progenitors, data_size)

    # Only use bins where there are at least 4 galaxies
    pick = n_galaxies > 3

    # Calculate progenitor fractions
    with np.errstate(divide='ignore', invalid='ignore'):
        frac = np.true_divide(n_spiral_progenitors[pick], n_galaxies[pick])

    bins = np.array([np.reshape(bins[i], data_size)[pick] for i in range(len(values))]).transpose()

    # Do n-D linear interpolation to get progenitor fraction for input values
    return griddata(bins, frac, values, method='linear')

