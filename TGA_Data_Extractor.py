#Oliver Kilbury
#02-25-2014
#Project #1

'''
Project: TGA data extraction script

Scope:
This script imports data that is generated from a Thermo Gravimetric Analyzer
at ETH in Switzerland, clean it, and perform numerical integration on Mass Spec data streams. 

Function:
This will allow our PhD student to evaluate product evolution, 
determine Yield, and make decisions about future experimental runs more efficiently.  

'''

#Importing needed libraries for this script
import numpy as np                                              #Importing numpy as variable np. I saw this on www.stackoverflow.com/questions/10814353/
import scipy.integrate                                          #Import the integrate function from scipy library
from scipy import stats                                         #Import stats module from scipy to enable linear regression of data


#Instructions for User
print('''
To use this script please follow the step by step instructions:
1. Make sure script and *.lvm file are in the same folder.
2. You must have numpy, scipy installed on machine.
3. Enter *.lvm file name when prompted. 
4. H2, O2, CO, and CO2 integrals are automatically calculated.
	 *integrals are evaluated with Simpson numerical integration.
5. Questions, email the help desk at kilbury@colorado.edu
''')


## FILE INPUT
 
filename = input("Enter file name with *lvm extension: ")       #Allowing user to input filename to manipulate   
infile = open(filename,'r', encoding = 'latin-1')               #open for reading, *.lvm file is not in UTF-8 so encoding it as Latin-1 for workaround         
print("Name of the file is: ", filename)                        #Printing name of file for user verification

#Read in all lines of file
entry = infile.readlines()                                      #reading in all lines of .lvm file

#Creating empty variable lists
Time = []                                                       #Initialize a new Time list
H2 = []                                                         #Initialize a new H2 signal list
O2 = []                                                         #Initialize a new O2 signal list
CO = []                                                         #Initialize a new CO signal list
CO2= []                                                         #Initialize a new CO2 signal list
 

##Clean up data, format data, + grab columns of interest

for line in entry[24: ]:                                        #Omitting first 23 lines of header information
	line = line[:-1]                                              #eliminating new line
	value = line.split('\t')                                      #splitting data by "tab" 
	
	#Extracting Columns from source file
	time = value[0]                                             #parsing time data 
	h2 = value[4]                                               #parsing H2 Mass spec data
	o2 = value[7]                                               #parsing O2 Mass spec data
	cO = value [5]                                              #parsing CO Mass spec data
	cO2 = value[6]                                              #parsing CO2 Mass spec data
	
	#Casting and sending data to lists
	H2.append(float(h2))                                        #sending H2 data to list
	CO.append(float(cO))                                        #sending CO data to list
	CO2.append(float(cO2))                                      #sending CO2 data to list
	Time.append(float(time))                                    #sending Time data to list
	O2.append(float(o2))                                        #appending all O2 data to pyfile in list form 

infile.close()                                                  #closing opened file


##Functions


#numerical integration of mass spec signal 
#Integration is based on Simpson's Rule; a Newton-Cotes formula for 
#approximating the integral function using quadratic polynomials
def MassSpecSignalIntegrate(Signal, Rxn_Time):  
	a = np.array(Signal)                                        #Converting Signal list to array using numpy
	b = np.array(Rxn_Time)                                      #Converting Time list to array using numpy
	valueInt = scipy.integrate.simps(a,b)                       #Calculating Simpson Integral of Signal over Rxn_time 
	return valueInt                                             #return integral value

#Linear regression of data to get line formula.Assignment requirement.
def getRegression(Time, Signal):                                             
	a = np.array(Signal)                                        #converting list to array
	b = np.array(Time)                                          #converting list to array   
	slope, intercept, r2_val, p_val, std_err = stats.linregress(Time,Signal) #extracting linear regression variables from data
	print("Slope of line: ", slope)                             #Print out variable
	print("Intercept of line: ", intercept)                     #Print out
	print("R2_val of fit: ", r2_val)                            #Print out  
	print("std_err of fit: ", std_err)                          #Print out 


#find the average mass spec signal. Assignment Requirement
def getAverage(data):
	for value in data:                                          #Looping through data list
		sum = 0                                                 #Initialize sum
		sum += value                                            #Summing all data 
		count = len(data)                                       #Finding the lenght of data 
		average = sum/count                                     #Calculating average 
		return average                                          #return average

#find the max value of the mass spec signal. Assignment Requirement.
def getMax(data):
	max = 0.0                                                     #Initialize max value
	for value in data:                                            #loop through data set
		if value > max:                                             #comparing each item to max 
			max = value                                               #if value is larger than max, it becomes new max
		else:                        
			max = max                                                 #otherwise max stays unchanged
	return max		                                                #return max value

#find the min value of the mass spec signal.Assignment requirement
def getMin(data):
	min = 0.0                                                     #same as above just looking for min
	for value in data:
		if value < min:
			min = value
		else:
			min = min
	return min
		

#Main function

def main():
	print("The integral of the CO signal is: ", MassSpecSignalIntegrate(CO,Time))
	print("The integral of the CO2 signal is: ", MassSpecSignalIntegrate(CO2, Time))
	print("The integral of the H2 signal is: ", MassSpecSignalIntegrate(H2, Time))
	print("The integral of the O2 signal is: ", MassSpecSignalIntegrate(O2, Time))
	print("\nCO regression data")
	getRegression(Time, CO)
	print("\nCO2 regression data")
	getRegression(Time, CO2)
	print("\nThe average CO signal value is: ",getAverage(CO))
	print("The average CO2 signal value is: ",getAverage(CO2))
	print("\nThe max CO signal value is: ", getMax(CO))
	print("The min CO signal value is: ", getMin(CO))
	print("\nThe max O2 signal value is: ", getMax(O2))
	print("The min O2 signal value is: ", getMin(O2))
main()
			


