# COTATools 2010

from cotatools.units import kg, avogadro, meter, pascal, boltzmann
import numpy

class Framework(object):
    def __init__(self, title = None):
        pass
        #self.volume = volume
        #if title != None:
        #    self.title = title

class MCRun(object):
     def __init__(self):
        pass

class PVT(MCRun):
     def __init__(self, pressure, volume, temperature):
        self.pressure = pressure
        self.volume = volume
        self.temperature = temperature

class NVE(MCRun):
     def __init__(self, number, volume, energy):
        self.number = number
        self.volume = volume
        self.energy = energy

class Averages(object):
     def __init__(self, label):
         self.label = label

# LOAD DATA
#==========

def load_framework():
    pass


def gotolinestart(f, text):
    """Get data from line.
    
    Arguments:
     | f  --  file object
     | text	 --	 we are looking for the next line that
    			 starts with this text
    """
    for line in f:
    	if line.startswith(text):
    		#print line
    		break
    return line

def gotoline(f, text):
    """Get data from line.
    
    Arguments:
     | f  --  file object
     | text	 --	 we are looking for the next line that
    			 contains this text
    """
    for line in f:
    	if text in line:
    		#print line
    		break
    return line


def load_molecules(filename):
    # go to section
    gotolinestart(f, "MoleculeDefinitions:")
    line = gotolinestart(f, "Component ")

def load_framework(filename):
        framework = Framework()
        # go to framework line
        f = open(filename)
        gotolinestart(f, "System Properties")

        line = gotolinestart(f, "Helium void fraction") #[-]
        framework.volume = float(line.split()[-1])

        line = gotolinestart(f, "volume of the cell") #[A3]
        framework.volume = float(line.split()[-2])
        line = gotolinestart(f, "Framework Mass:") # [g/mol]
        framework.mass = float(line.split()[-2]) *kg*0.001/avogadro
        line = gotolinestart(f, "Framework Density:") # [kg/m3]
        framework.density = float(line.split()[-2]) *kg/meter**3
        line = gotolinestart(f, "Framework has net charge:") # [electroncharges]
        framework.charge = float(line.split()[-1])

        f.close()
        return framework


def load_averages(filename):

    # this is here the FIRST system only XXXX

        averages = Averages(filename)

        # go to last section
        f = open(filename)
        averages = Averages("test")
        gotolinestart(f, "Average properties of the system[0]:")

        # go to Average temperature
        gotolinestart(f, "Average temperature:")
        line = gotoline(f, "Average")  #[K]
        averages.temperature = float(line.split()[1])
        # go to Average Pressure
        gotolinestart(f, "Average Pressure:")
        line = gotoline(f, "Average")  #[Pa]
        averages.pressure = float(line.split()[1]) *pascal
        # go to Average volume
        gotolinestart(f, "Average Volume:")
        line = gotoline(f, "Average")  #[A3]
        averages.volume = float(line.split()[1])

        # got to Average Density
        gotolinestart(f, "Average Density:")
        line = gotoline(f, "Average")  #[kg/m^3]
        averages.density = float(line.split()[1]) *kg/meter**3
        # and for the Components ... XXX

        # go to Average energy
        gotolinestart(f, "Average energies of the system[0]:")
        gotolinestart(f, "Total energy")
        line = gotoline(f, "Average")  #[K]
        averages.energy = float(line.split()[1])*boltzmann

        # loadings
        gotolinestart(f, "Number of molecules:")
        gotolinestart(f, "Component ")
        line = gotoline(f, "Average loading absolute [mol/kg framework]")  #[mol/kg]
        averages.loading = float(line.split()[5]) *avogadro/kg
        # go to Widom [mol/kg/Pa]
        gotolinestart(f, "Average Widom Rosenbluth factor:")
        line = gotoline(f, "Average Widom:")   #[-]
        averages.widom = float(line.split()[3])

        # go to henry [mol/kg/Pa]
        gotolinestart(f, "Average Henry coefficient:")
        line = gotoline(f,"Average Henry coefficient")  #[mol/kg/Pa]
        averages.henry = float(line.split()[4]) *avogadro/kg/pascal

        # go to last section
        gotolinestart(f, "Average adsorption energy <U_gh>_1-<U_h>_0 obtained from Widom-insertion:")
        f.close()
        return averages

def load_for_isotherm(f, ):
            # ensemble, exttemperature, extpressure
        # go to first section
        line = gotolinestart(f, "Ensemble")
        ensemble = line.split()[1]
        gotolinestart(f, "Thermo/Baro-stat NHC parameters")
        line = gotolinestart(f, "External temperature:")
        exttemperature = float(line.split()[-2])
        line = gotolinestart(f, "External Pressure:")
        extpressure = float(line.split()[-2])

        # go to section
        gotolinestart(f, "Ewald parameters")
        # go to section
        gotolinestart(f, "Forcefield:")
        # go to moleculedefinitions
        # ...
        # go to framework
        # ...
        # go to averages
        # ...


def extract_data(filename,dictionary):
    """Take a file and a dictionary of regular expressions. Return a
    dictionary of values matched by the regular expressions. If more than
    one line matches the regular expression, create a new key from the
    regexp's original key."""
    # Get a list of lines from the file.
    lines = get_lines(filename)
    # Create an empty dictionary.
    outdict = {}
    dictionary = compile_regexps(dictionary)
    for key in dictionary:
    	regex = dictionary[key]
    	matches = []
    	for line in lines:
    		if regex.search(line):
    			matches.append(regex.search(line).group(1))
    	for m in matches:
    		i = matches.index(m)
    		if i == 0:
    			newkey = key
    		else:
    			newkey = ' '.join([key,str(i)])
    		outdict[newkey] = m
    return outdict


def get_lines(filename):
    """Returns a list of lines from the given file."""
    f = open(filename,mode='r')
    lines = f.readlines()
    f.close()
    return lines

def compile_regexps(dictionary):
    """Loads a dictionary of regular expression strings to be used
    for extracting the parameters of the simulation input file."""
    for key in dictionary:
    	dictionary[key] = re.compile(dictionary[key])
    return dictionary



# GENERATE OUTPUT
#================
import csv

def write_results_to_csv(dictlist):
    """Create a csv object if it does not exist, then append the 
    data to the end of csv."""
    csvfile = open('results.csv',mode='a')
    columns = dictlist[0].keys()
    columns = sort_columns(columns)
    # print the column headers, too
    coldict = {}
    i = 0
    for k in columns:
    	i += 1
    	coldict[k] = '%d: %s' % (i,k)
    
    dictlist.insert( 0, coldict )
    
    csvobj = csv.DictWriter(csvfile,columns,restval='n.a.',extrasaction='ignore',quoting=csv.QUOTE_ALL)
    for item in dictlist:
    	csvobj.writerow(item)
    csvfile.close()


def sort_columns(keys):
    	"""Take the list of keys from the data dictionary and sort them based on 
    	the order specified in the list below."""
    	masterlist = ['time',
    				  'seed',				   
    				  'cycles',
    				  'initcycles',
    				  'equilcycles',
    				  'zeolite',
    				  'temperature',
    				  'pressure',
    				  'zeodensity',
    				  'ucx',
    				  'ucy',
    				  'ucz',
    				  'component',
    				  'igrosen',
    				  'parpressure',
    				  'molfraction',
    				  'rosenbluth',
    				  'rosenbluth_err',
    				  'henrycoef',
    				  'henrycoef_err',
    				  'load_uc',
    				  'load_uc_err',
    				  'load_kg',
    				  'load_kg_err',
    				  'ex_load_kg',
    				  'ex_load_kg_err',					 
    				  'adsenergy',
    				  'adsenergy_err']
    	tmplist = []
    	columns = []
    	for key in keys:
    		i = masterlist.index(key.split()[0])
    		tmplist.append((i,key))
    	tmplist.sort()
    	columns[:] = [ t[1] for t in tmplist]
    	return tuple(columns)
