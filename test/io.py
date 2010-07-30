from cotatools import *

import unittest, numpy


__all__ = ["IOTestCase"]


class IOTestCase(unittest.TestCase):

    def test_nothing(self):
     dirname = "/network-home/an/work/langmuir-validation/"
     import pylab
     pylab.figure(1)
     for frameworkname in ["MFI-maciej","MOR-maciej","RHO-maciej"]:
        print "="*20
        molecule = "co2"

        # 1. get widom He
        subdirname = "void-He/"
        jobname = frameworkname+"[0]_1.1.1_298.150000"
        filename = frameworkname+"/Output/System[0]/output_"+jobname+".data"
        averages = load_averages(dirname+subdirname+filename)

        widomHe = averages.widom
        volume  = averages.volume
        volumevoid = volume * widomHe
        print "volumevoid", volumevoid
        print "volumevoid", volumevoid/meter**3, "m^3"

        # 2. get widom CO2 or Henry
        subdirname = "henry/"
        averages = load_averages(dirname+subdirname+filename)
        framework = load_framework(dirname+subdirname+filename)

        print "henry", averages.henry
        print "henry", averages.henry / (avogadro/kg/pascal), "mol/kg/Pa"
        print "henry alternative",
        widom = averages.widom
        #temp  = averages.temperature
        temp = 298.15
        henry = widom / (boltzmann*temp)/framework.density
        print henry

# [-] * [1/energy] * [vol/mass]
# = [vol/(energy*mass)]
# = [vol/(N*length*mass)]
# = [surface/(N*mass)]
# = [1/(pressure*mass)]  e.g. 1/kg/Pa
# Convert to per mol?
# => x [XXXX]

        print "henry alternative", henry / (1/kg/pascal) , "1/kg/Pa"
        print "henry alternative", henry / (avogadro/kg/pascal) , "mol/kg/Pa"


        # get the pressures for particular T
        pressurenames = ['1.0e1pa','1.0e2pa','1.0e3pa','1.0e5pa','2.0e4pa','4.0e4pa','5.0e3pa','6.0e4pa','8.0e4pa' ]
        loadings = []
        pressures = []
        for pressurename in pressurenames:
            subdirname = "isotherms/"
            filename = frameworkname+"/co2/298.15K/"+pressurename+"/Output/System[0]/output_"+jobname+".data"
            averages = load_averages(dirname+subdirname+filename)
            loadings.append(averages.loading)
            pressures.append(float(pressurename[:-2])*pascal)

        loadings = numpy.array(loadings)
        pressures = numpy.array(pressures)

        import matplotlib,pylab
        pylab.figure()
        pylab.loglog(pressures/pascal, loadings/(avogadro/kg),"o")
        pylab.xlabel("pressure [Pa]")
        pylab.ylabel("loading [mol/kg framework]")
        pylab.title("temp is "+str(temp)+"K")
        pylab.savefig("output/"+frameworkname+".simul.png")
        pylab.close()

        # theoretical loadings
        print "1."
        maxpress = 1e6*pascal
        print "maxpress", maxpress
        maxnb = maxpress * framework.volume * widomHe / (boltzmann * temp)
        # maxload is now a number of adsorbed particles in volume of a unitcell-framework

        # convert this to something in mol of adsorbed per mass of unitcell-zeolite
        # nb of mol per mass unitcell-framework
        # = nb of particles per volume unitcell-framework / avogadro / (mass unitcell-framework/volume unitcell-framework)
        print "maxnb", maxnb
        maxload = maxnb / framework.density
        print "maxload", maxload, "nb of molecules per mass framework"

        print "2."
        print "alternatively, use just maxs of available data"
        # highest loading available
        maxpress = max(pressures)
        maxload = max(loadings)
        print "maxload", maxload, "nb of molecules per mass framework"

        print "3."
        print "alternatively, use density of liquid CO2"
        # CO2 has 0.770 g/ml
        # mass of CO2 per volume:
        maxdensity = 0.770 * 0.001*kg / (1.e-6*meter**3)
        maxdensity = 464 * kg / meter**3
        # mass in free volume:
        maxmass = maxdensity * (framework.volume*widomHe)
        # nb of particules in free volume:
        # mass of CO2 is 44.010 g/mol
        massco2 = 44.010 * 0.001*kg / avogadro
        maxnb1 = maxdensity / massco2
        maxnb = maxmass / massco2
        maxload1 = maxnb1 * volumevoid
        maxload = maxnb / framework.density
        print "maxload", maxload, "nb of molecules per mass framework"
        print "dens", maxdensity / (kg/meter**3) , "[kg/m**3]"
        print "massco2", massco2 / kg  , "[kg]"
        print "mass", maxmass / kg, "[kg]"
        print "nb1", maxnb1 / (1./meter**3), "[1/m^3]"
        print "volume framework", framework.volume
        print "volume He", framework.volume * widomHe
        print "volume", averages.volume*averages.widom
        print "volumevoid", volumevoid 
        print "nb", maxnb
        print "load1", maxload1, "[nb/volume]"
        print "load",maxload

        b = henry/maxload
        print "b", b
        pminln = numpy.log(min(pressures))-1.
        pmaxln = numpy.log(max(pressures))+100.
        pressures_theor = numpy.exp(numpy.arange(pminln,pmaxln, (pmaxln-pminln)/20))
        loadings_theor = maxload * b * pressures_theor / (1+b*pressures_theor)

        pylab.figure()
        pylab.loglog(pressures_theor/pascal,loadings_theor/(avogadro/kg),"o")
        pylab.xlabel("pressure [Pa]")
        pylab.ylabel("loading [mol/kg framework]")
        pylab.savefig("output/"+frameworkname+".langmuir.png")
        pylab.close()
        
        pylab.figure(1)
        pylab.loglog(pressures_theor/pascal,loadings_theor/(avogadro/kg))
        pylab.loglog(pressures/pascal,loadings/(avogadro/kg),"o")


        pylab.legend(["langmuir","simul"],loc=4)
        pylab.xlabel("pressure [Pa]")
        pylab.ylabel("loading [mol/kg framework]")
        pylab.title("all -- CO2 temp="+str(temp)+"K")
        pylab.savefig("output/"+frameworkname+".both.png")
        #pylab.close()
