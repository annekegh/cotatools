# COTATools 2010
"""A set of units, conversions, ..."""

# COTA CONVENTIONS
#=================

# Mutual consistent basic set of units:
# ======================================
# Unit of temperature: Kelvin
# Unit of length:      1e-10 [m]
# Unit of time:        1e-12 [s]
# Unit of mass:        1.66054e-27 [kg]
# Unit of charge:      1.60218e-19 [C/particle]
# 
# Derived units and their conversion factors:
# ===========================================
# Unit of energy:              1.66054e-23 [J]
# Unit of force:               1.66054e-13 [N]
# Unit of pressure:            1.66054e+07 [Pa]
# Unit of velocity:            100 [m/s]
# Unit of acceleration:        1e-08 [m^2/s]
# Unit of dipole moment:       1.60218e-29 [C.m]
# Unit of electric potential:  0.000103643 [V]
# Unit of electric field:      1.03643e+06 [V]
# Unit of Coulomb potential:   138935.4834964017  [J]
# Unit of dielectric constant: 0.0000154587       [s^2 C^2/(kg m^3)]
# Unit of wave vectors:        5.3088374589       [cm^1]
# Boltzmann constant:          0.8314464919       [-]
# 
# Internal conversion factors:
# ===========================================
# Energy to Kelvin:                              1.20272
# Heat capacity conversion factor:               10



meter = 1.e10
second = 1.e12
kg = 1./1.66054e-27
#kgpermol = kg*avogadro

avogadro = 6.02e23   # mol
boltzmann = 0.8314464919

joule = 1./1.66054e-23
newton = 1/1.66054e-13
pascal = 1/1.66054e+07


# energy internally expressed in 'energy-units'
# energy to kelvin = 1/boltzmann
# energy expressed in K = c K corresponds to c*boltzmann energy-units



