'''Return the progenitor fraction for input values.'''

import numpy as np
from scipy.io import FortranFile
import sys
import argparse
from scipy.interpolate import griddata

parser = argparse.ArgumentParser()
parser.add_argument('-z','--redshift', type=float, default=np.nan, help='Redshift')
parser.add_argument('-m','--mass', type=float, default=np.nan, help='Log10 stellar mass/M_sun')
parser.add_argument('-p','--density', type=float, default=np.nan,
                    help='Local number density percentile [0,100]')
parser.add_argument('-s','--SFR', type=float, default=np.nan, help='SFR in M_sun/yr')

args = parser.parse_args()

values = [args.density, args.SFR, args.mass, args.redshift]

if values.count(np.nan) > 3:
    print 'Incorrect number of arguments'
    sys.exit()

# Read datacube
f = FortranFile('fractions.dat')
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
fit = griddata(bins, frac, values, method='linear')
        
print fit[0]
