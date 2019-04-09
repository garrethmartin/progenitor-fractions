## *README* for `tabulate_progenitor_probability.py`

### Reference:
[Martin et al. 2018a](https://doi.org/10.1093/mnras/stx3057 "Martin+18a")
*Martin, G., Kaviraj, S., Devriendt J. E. G., Dubois Y., Pichon C., Laigle C.*


### Contact:
[g.martin4@herts.ac.uk](mailto:g.martin4@herts.ac.uk "email")


### Purpose:
Reads `fractions.dat` binary file and returns the joint progenitor probability for given redshift, mass, environment (percentile) and star-formation rate (i.e. the probability that a galaxy with given properties has spheroidal morphology at z=0). If one or more dimensions are not specified, the joint progenitor probability is returned with missing dimensions marginalised out.


### Prerequisites:
* `fractions.dat`
* numpy
* scipy

### Installation:
    
    pip install progenitor-probability
    

### Usage:

#### Using the built-in script:
    
    tabulate_progenitor_probability.py -z 0.4 -m 10.8
    0.266751184855
    
    
    tabulate_progenitor_probability.py --help

    usage: tabulate_progenitor_probability.py [-h] [-z REDSHIFT] [-m MASS]
                                              [-p DENSITY] [-s SFR]

    optional arguments:
      -h, --help            show this help message and exit
      -z REDSHIFT, --redshift REDSHIFT
                            Redshift
      -m MASS, --mass MASS  Log10 stellar mass/M_sun
      -p DENSITY, --density DENSITY
                            Local number density percentile [0,100]
      -s SFR, --SFR SFR     SFR in M_sun/yr
    

**-z** *redshift*

**-m** *log10(stellar mass / M_sun)*

**-p** *percentile of local number density* in the range [0,100] (see [Martin et al. 2018a](https://doi.org/10.1093/mnras/stx3057 "Martin+18a"))

**-s** *star formation rate in M_sun/yr*

#### Importing the package
```
from progenitor_probability import progenitor_probability
>>> progenitor_probability(redshift=0.4, mass=10.8)
0.266751184855
```
