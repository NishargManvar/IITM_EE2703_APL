"""
PURPOSE : EE2703 - Assignment 2 (INCLUDING DEPENDENT SOURCES)
AUTHOR  : Manvar Nisharg (EE19B094)
INPUT : netlist file with below given syntax
OUTPUT : Values of all variables of Adjacency matrix
"""

"""
---------------------------------- SYNTAX ----------------------------------
.circuit	#This is a comment
V1 node1 node2 dc value 			#DC VOLTAGE SOURCE -- (node1 == +ve terminal) (node2 == -ve terminal)
V2 node1 node2 ac Vp-p phase 		#AC VOLTAGE SOURCE -- Vp-p is peak to peak voltage, phase in degrees
R1 node1 node2 value 				#RESISTANCE
L1 node1 node2 value 				#INDUCTOR
C1 node1 node2 value 				#CAPACITOR
I1 node1 node2 value 				#CURRENT SOURCE -- arrow from node1 to node2
E1 node1 node2 node3 node4 value 	#VCVS -- (element connected between node1 & node2)(node3 & node4 == +ve & -ve node on which dependent)
G1 node1 node2 node3 node4 value 	#VCCS -- similar as above
H1 node1 node2 V1 value 			#CCVS -- V1 is the voltage source whose current will be taken. (Add a 0 volt battery if necessary)
F1 node1 node2 V1 value 			#CCCS -- same as above
.end
.ac V1 frequency 						#frequency of AC voltage source -- Currently only one AC voltage source is supported
"""

import sys
import numpy as np
import math


"""-------------------------------------------------------------------------------------------------
									CLASS DEFINITION OF ALL ELEMENTS
-------------------------------------------------------------------------------------------------"""
node_count = 0
node_list = {}	#Dictionary of nodes of the format -- {name : object_pointer,node_number }
class Node:
	def __init__(self,user_name):
		self.name=user_name
		self.resi=[]	#List of resistors connected to a node
		self.vols=[]	#List of voltage source connected to a node
		self.curs=[]	#List of current source connected to a node
		self.capa=[]	#List of capacitor connected to a node
		self.indu=[]	#List of inductor connected to a node
		self.vcvs=[]	#List of VCVS connected to a node
		self.vccs=[]	#List of VCCS connected to a node
		self.ccvs=[]	#List of CCVS connected to a node
		self.cccs=[]	#List of CCVS connected to a node

		

resi_list={}	#Dictionary of resistance of the format -- {resistance_number : object_pointer}
resi_name_list={}	#Dictionary of resistance of the format -- {name : resistance_number}
resi_count = 0
class Resi :
	def __init__(self,user_name,user_node1,user_node2,user_value):
		self.name = user_name
		self.node1 = user_node1
		self.node2 = user_node2
		self.value = user_value



vols_list={}	#Dictionary of voltage source of the format -- {voltage_source_number : object_pointer}
vols_name_list={}	#Dictionary of voltage source of the format -- {name : voltage_source_number}
vols_count = 0
class Vols :
	def __init__(self,user_name,user_node1,user_node2,user_value,user_phase,is_AC):
		self.name = user_name
		self.node1 = user_node1		#Postive terminal of voltage source
		self.node2 = user_node2		#Negative terminal of voltage source
		if is_AC == 1:	#AC value
			self.value = complex(user_value*math.cos(user_phase*math.pi/180),user_value*math.sin(user_phase*math.pi/180))
		else:	#DC value
			self.value = user_value


curs_list={}	#Dictionary of current source of the format -- {current_source_number : object_pointer}
curs_name_list={}	#Dictionary of current source of the format -- {name : current_source_number}
curs_count = 0
class Curs :
	def __init__(self,user_name,user_node1,user_node2,user_value):
		self.name = user_name
		self.node1 = user_node1
		self.node2 = user_node2
		self.value = user_value


capa_list={}	#Dictionary of capacitor of the format -- {capacitor_number : object_pointer}
capa_name_list={}	#Dictionary of capacitor of the format -- {name : capacitor_number}
capa_count = 0
class Capa :
	def __init__(self,user_name,user_node1,user_node2,user_value,frequency):
		self.name = user_name
		self.node1 = user_node1
		self.node2 = user_node2
		if frequency != 0:	#AC Impedance
			self.value = complex(0,-1/(frequency*user_value*2*math.pi))
		else:	#DC Impedance
			self.value = 10**20


indu_list={}	#Dictionary of inductor of the format -- {inductor_number : object_pointer}
indu_name_list={}	#Dictionary of inductor of the format -- {name : inductor_number}
indu_count = 0
class Indu :
	def __init__(self,user_name,user_node1,user_node2,user_value,frequency):
		self.name = user_name
		self.node1 = user_node1
		self.node2 = user_node2
		if frequency == 0:	#DC Impedance
			self.value = 10**(-20)
		else:	#AC Impedance
			self.value = complex(0,frequency*user_value*math.pi*2)


vcvs_list={}	#Dictionary of vcvs of the format -- {vcvs_number : object_pointer}	
vcvs_name_list={}	#Dictionary of vcvs of the format -- {name : vcvs_number}
vcvs_count = 0
class Vcvs :
	def __init__(self,user_name,user_node1,user_node2,user_node3,user_node4,user_value):
		self.name = user_name
		self.node1 = user_node1		#Positive terminal of VCVS
		self.node2 = user_node2		#Negative terminal of VCVS
		self.node3 = user_node3		#Dependent positive terminal
		self.node4 = user_node4		#Dependent negative terminal
		self.value = user_value


vccs_list={}	#Dictionary of vccs of the format -- {vccs_number : object_pointer} 
vccs_name_list={}	#Dictionary of vccs of the format -- {name : vccs_number}
vccs_count = 0
class Vccs :
	def __init__(self,user_name,user_node1,user_node2,user_node3,user_node4,user_value):
		self.name = user_name
		self.node1 = user_node1		#Positive terminal of VCCS
		self.node2 = user_node2		#Negative terminal of VCCS
		self.node3 = user_node3		#Dependent positive terminal
		self.node4 = user_node4		#Dependent negative terminal
		self.value = user_value


ccvs_list={}	#Dictionary of ccvs of the format -- {ccvs_number : object_pointer} 
ccvs_name_list={}	#Dictionary of ccvs of the format -- {name : ccvs_number}
ccvs_count = 0
class Ccvs :
	def __init__(self,user_name,user_node1,user_node2,user_voltage_source,user_value):
		self.name = user_name
		self.node1 = user_node1		#Positive terminal of CCVS
		self.node2 = user_node2		#Negative terminal of CCVS
		self.voltage_source = user_voltage_source	#Voltage source on which dependent
		self.value = user_value


cccs_list={}	#Dictionary of cccs of the format -- {cccs_number : object_pointer}
cccs_name_list={}	#Dictionary of cccs of the format -- {name : cccs_number}
cccs_count = 0
class Cccs :
	def __init__(self,user_name,user_node1,user_node2,user_voltage_source,user_value):
		self.name = user_name
		self.node1 = user_node1		#Positive terminal of CCCS
		self.node2 = user_node2		#Negative terminal of CCCS
		self.voltage_source = user_voltage_source	#Voltage source on which dependent
		self.value = user_value


"""-------------------------------------------------------------------------------------------------
											READING LINES OF FILE
-------------------------------------------------------------------------------------------------"""
#Global Variables 
start_keyword = ".circuit"
end_keyword = ".end"
ac_keyword = ".ac"


#Opening file
try:
	if(len(sys.argv)!=2):
		raise Exception()
	filename = sys.argv[1]
except:
	print("Please enter file name as the second and only command-line argument other than run command.")
	print("Example : $ %s <filename>\n"%sys.argv[0])
	exit()
else:
	try:
		file = open(filename)
	except:
		print("File with given file name does not exist.")
		exit()

#Reading all the lines
try:
	file_lines = file.readlines()
except:
	print("Invalid file")
finally:
	file.close()



start_index = -1	#Index of line for the .circuit directive
end_index = -2		#Index of line for the .end directive
frequency = 0		#Default frequency value
is_AC = 0			#Variable to check if circuit is AC

#Finding the values of start_index , end_index and frequency
index = 0 
for line in file_lines:

	if (str(line[:len(start_keyword)])).lower() == start_keyword:
		start_index = index

	elif (str(line[:len(end_keyword)])).lower() == end_keyword:
		end_index = index

	elif (str(line[:len(ac_keyword)])).lower() == ac_keyword:
		words = ((line.split('#')[0].lower()).split())
		try:
			AC_source_name = words[1].lower()	#Storing name of votage source for which frequency is defined
			words[2] = float(words[2])
		except:
			print("Wrong definition of frequency")
			exit()
		else:
			frequency = words[2]
	index += 1

#Error if either of the directives are missing or are in the wrong order
if (start_index > end_index or end_index < 0 or start_index < 0):
	print("Invalid circuit definition... please check '%s' and '%s' directives\n"%(start_keyword,end_keyword))
	exit()


"""-------------------------------------------------------------------------------------------------
									ADDING ELEMENTS (AND NUMBERING) AS OBJECTS
-------------------------------------------------------------------------------------------------"""

"""-----> UTILITY FUNCTIONS FOR ADDING ELEMENTS <-----"""

#Check syntax for each element
def check_length_and_numerical(words,required_length,numerical_index):
	if len(words) != required_length:
		return 0
	else:
		try:
			words[numerical_index] = float(words[numerical_index])
		except:
			return 0
	return 1

#Check if new node is connected
def check_for_new_node(words,node_list,node_count):
	if words[1] == words[2]:
		print("Element %s is connected between same node"%words[0])
		exit()

	if words[1] not in node_list:
		node_count += 1
		node_list[words[1]]=[Node(words[1]),node_count]
	if words[2] not in node_list:
		node_count += 1
		node_list[words[2]]=[Node(words[2]),node_count]
	return node_count

#Check if element with given name already exisits
def check_if_element_exists(element_name_list,element_name):
	if element_name in element_name_list.keys():
		print("Two elements with same name defined")
		exit()


"""-----> ADDING ELEMENTS <-----"""

for line in (file_lines[start_index+1:end_index]):	#Looping the lines
	words = ((line.split('#')[0].lower()).split())	#Removing the comment and then splitting the words
	
	if(len(words)!=0):	#If the whole line was not a comment then add element


		#If element is VOLTAGE SOURCE
		if words[0][0] == "v" :

			if check_length_and_numerical(words,5,4) == 0 and check_length_and_numerical(words,6,4)==0:	#Check for syntax errors
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)	#Update new node if any
			check_if_element_exists(vols_name_list,words[0])	#Check if element with given name already exists

			if words[3] == "ac":	#If source is AC
				if is_AC == 1:
					print("This code only supports only one AC voltage currently")
					exit()
				if frequency == 0:
					print("Either .ac directive was not defined or frequency was set to 0 in which case please use DC voltage")
					exit()
				if AC_source_name != words[0]:
					print("Frequency for AC source defined at line %d not found"%(file_lines.index(line)+1))
					exit()
				try:	#Check if phase is a number
					words[5] = float(words[5])
				except:
					print("Phase of element is not a number")
					exit()
				is_AC = 1
				vols_count += 1		#Update vols_count
				vols_list[vols_count]=Vols(words[0],words[1],words[2],words[4]/2,words[5],is_AC)	#Add element into vols_list
				vols_name_list[words[0]]=vols_count		#Adding element into vols_name_list
				node_list[words[1]][0].vols.append(vols_count)	#Adding element in the elements list at both nodes
				node_list[words[2]][0].vols.append(vols_count)

			elif words[3] == "dc":		#If source is DC
				vols_count += 1		#Update vols count
				vols_list[vols_count]=Vols(words[0],words[1],words[2],words[4],0,is_AC)		#Add element into vols_list
				vols_name_list[words[0]]=vols_count		#Adding element into vols_name_list
				node_list[words[1]][0].vols.append(vols_count)		#Adding element in the elements list at both nodes
				node_list[words[2]][0].vols.append(vols_count)


		#if element is RESISTOR
		#NOTE : All elements below this follow same code pattern (Thus refer here for commenting)
		elif words[0][0] == "r" :
			if check_length_and_numerical(words,4,3) == 0:	#Check for syntax error
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)		#Update new nodes if any
			check_if_element_exists(resi_name_list,words[0])		#Check if element with same name exists
			
			resi_count += 1		#Update resi_count (Or appropriate variable depending on the element)
			resi_list[resi_count]=Resi(words[0],words[1],words[2],words[3])		#Adding element in resi_list (Appropriate list for other elements)
			resi_name_list[words[0]]=resi_count		#Adding element in resi_name_list (Appropriate name_list for other elements)
			node_list[words[1]][0].resi.append(resi_count)	#Add element in the element list at both nodes
			node_list[words[2]][0].resi.append(resi_count)

		#if element is INDUCTOR
		#NOTE : Refer resistor block for code pattern and commenting
		elif words[0][0] == "l" :
			if check_length_and_numerical(words,4,3) == 0:
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)
			check_if_element_exists(indu_name_list,words[0])

			indu_count += 1
			indu_list[indu_count]=Indu(words[0],words[1],words[2],words[3],frequency)
			indu_name_list[words[0]]=indu_count
			node_list[words[1]][0].indu.append(indu_count)
			node_list[words[2]][0].indu.append(indu_count)


		#if element is CAPACITOR
		#NOTE : Refer resistor block for code pattern and commenting
		elif words[0][0] == "c" :
			if check_length_and_numerical(words,4,3) == 0:
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)
			check_if_element_exists(capa_name_list,words[0])

			capa_count += 1
			capa_list[capa_count]=Capa(words[0],words[1],words[2],words[3],frequency)
			capa_name_list[words[0]]=capa_count
			node_list[words[1]][0].capa.append(capa_count)
			node_list[words[2]][0].capa.append(capa_count)


		#if element is CURRENT SOURCE
		#NOTE : Refer resistor block for code pattern and commenting
		elif words[0][0] == "i" :
			if check_length_and_numerical(words,4,3) == 0:
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)
			check_if_element_exists(curs_name_list,words[0])

			curs_count += 1
			curs_list[curs_count]=Curs(words[0],words[1],words[2],words[3])
			curs_name_list[words[0]]=curs_count
			node_list[words[1]][0].curs.append(curs_count)
			node_list[words[2]][0].curs.append(curs_count)


		#if element is VCVS
		#NOTE : Refer resistor block for code pattern and commenting
		elif words[0][0] == "e" :
			if check_length_and_numerical(words,6,5) == 0:
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)
			check_if_element_exists(vcvs_name_list,words[0])

			vcvs_count+=1
			vcvs_list[vcvs_count]=Vccs(words[0],words[1],words[2],words[3],words[4],words[5])
			vcvs_name_list[words[0]]=vcvs_count
			node_list[words[1]][0].vcvs.append(vcvs_count)
			node_list[words[2]][0].vcvs.append(vcvs_count)


		#if element is VCCS
		#NOTE : Refer resistor block for code pattern and commenting
		elif words[0][0] == "g" :
			if check_length_and_numerical(words,6,5) == 0:
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)
			check_if_element_exists(vccs_name_list,words[0])

			vccs_count += 1
			vccs_list[vccs_count]=Vccs(words[0],words[1],words[2],words[3],words[4],words[5])
			vccs_name_list[words[0]]=vccs_count
			node_list[words[1]][0].vccs.append(vccs_count)
			node_list[words[2]][0].vccs.append(vccs_count)


		#if element is CCVS
		#NOTE : Refer resistor block for code pattern and commenting
		elif words[0][0] == "h" :
			if check_length_and_numerical(words,5,4) == 0:
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)
			check_if_element_exists(ccvs_name_list,words[0])

			ccvs_count += 1
			ccvs_list[ccvs_count]=Ccvs(words[0],words[1],words[2],words[3],words[4])
			ccvs_name_list[words[0]]=ccvs_count
			node_list[words[1]][0].ccvs.append(ccvs_count)
			node_list[words[2]][0].ccvs.append(ccvs_count)


		#if element is CCCS
		#NOTE : Refer resistor block for code pattern and commenting
		elif words[0][0] == "f" :
			if check_length_and_numerical(words,5,4) == 0:
				print("Invalid syntax at line %d"%(file_lines.index(line)+1))
				exit()

			node_count = check_for_new_node(words,node_list,node_count)
			check_if_element_exists(cccs_name_list,words[0])

			cccs_count += 1
			cccs_list[cccs_count]=Cccs(words[0],words[1],words[2],words[3],words[4])
			cccs_name_list[words[0]]=cccs_count
			node_list[words[1]][0].cccs.append(cccs_count)
			node_list[words[2]][0].cccs.append(cccs_count)

		#Invalid Element
		else :
			print("Invalid element definition at line %d"%(file_lines.index(line)+1))
			exit()

"""-------------------------------------------------------------------------------------------------
								GENERATING ADJACENCY AND CONSTANT MATRICES
--------------------------------------------------------------------------------------------------"""
"""----> Utility Functions <----"""
def check_if_node_exists(object_pointer):	#Function to check if nodes on which VCVS and VCCS depend do exist
	global node_list
	if object_pointer.node3 not in node_list or object_pointer.node4 not in node_list:
		print("Dependent node of %s does not exist"%object_pointer.name)
		exit()

def check_if_voltage_exists(object_pointer):	#Function to check if voltage source on which CCVS and CCCS depend do exist
	global vols_name_list
	if object_pointer.voltage_source not in vols_name_list:
		print("Dependent voltage source of %s does not exist"%object_pointer.name)
		exit()


"""----> Functions to add values into Adjacency and Constant Matrices <----"""

#Function to add entries corresponding to resistors connected to a node
def node_add_resistance(current_node_o,current_node_n,adjacency):
	for resistance_n in current_node_o.resi:	#Loop through resistors connected to the given node

		resistance_o = resi_list[resistance_n]

		#Check if current node is node1 or node2 for the element
		if resistance_o.node1 == current_node_o.name:
			other_node_n = node_list[resistance_o.node2][1]
		else:
			other_node_n = node_list[resistance_o.node1][1]

		#Update entries in the matrix
		adjacency[current_node_n-1,current_node_n-1] += (1/resistance_o.value)
		adjacency[current_node_n-1,other_node_n-1] += (-1)*(1/resistance_o.value)

#Function to add entries corresponding to capacitors connected to a node
def node_add_capacitor(current_node_o,current_node_n,adjacency):
	for capacitor_n in current_node_o.capa:		#Loop through capacitors connected to the given node

		capacitor_o = capa_list[capacitor_n]

		#Check if current node is node1 or node2 for the element
		if capacitor_o.node1 == current_node_o.name:
			other_node_n = node_list[capacitor_o.node2][1]
		else:
			other_node_n = node_list[capacitor_o.node1][1]

		#Update entries in the matrix
		adjacency[current_node_n-1,current_node_n-1] += (1/capacitor_o.value)
		adjacency[current_node_n-1,other_node_n-1] += (-1)*(1/capacitor_o.value)

#Function to add entries corresponding to inductors connected to a node
def node_add_inductor(current_node_o,current_node_n,adjacency):
	for inductor_n in current_node_o.indu:		#Loop through inductors connected to the given node

		inductor_o = indu_list[inductor_n]

		#Check if current node is node1 or node2 for the element
		if inductor_o.node1 == current_node_o.name:
			other_node_n = node_list[inductor_o.node2][1]
		else:
			other_node_n = node_list[inductor_o.node1][1]

		#Update entries in the matrix
		adjacency[current_node_n-1,current_node_n-1] += (1/inductor_o.value)
		adjacency[current_node_n-1,other_node_n-1] += (-1)*(1/inductor_o.value)

#Function to add entries corresponding to voltage sources connected to a node
def node_add_voltage(current_node_o,current_node_n,adjacency):
	for voltage_n in current_node_o.vols:		#Loop through voltage sources connected to the given node

		voltage_o = vols_list[voltage_n]

		#Update entries in the matrix
		if voltage_o.node1 == current_node_o.name:
			adjacency[current_node_n-1,node_count+voltage_n-1] += 1	
		else:
			adjacency[current_node_n-1,node_count+voltage_n-1] += -1
			
#Function to add entries corresponding to current sources connected to a node
def node_add_current(current_node_o,current_node_n,constant):
	for current_n in current_node_o.curs:		#Loop through current sources connected to the given node

		current_o = curs_list[current_n]

		#Update entries in the matrix
		if current_o.node1 == current_node_o.name:
			constant[current_node_n-1] += (-1)*current_o.value
		else:
			constant[current_node_n-1] += current_o.value

#Function to add entries corresponding to VCVS connected to a node
def node_add_vcvs(current_node_o,current_node_n,adjacency):
	for vcvs_n in current_node_o.vcvs:		#Loop through VCVS connected to the given node

		vcvs_o = vcvs_list[vcvs_n]
		check_if_node_exists(vcvs_o)	#Check if dependent nodes exists

		#Update entries in the matrix
		if vcvs_o.node1 == current_node_o.name:
			adjacency[current_node_n-1,node_count+vols_count+vcvs_n-1] += 1
		else:
			adjacency[current_node_n-1,node_count+vols_count+vcvs_n-1] += -1

#Function to add entries corresponding to CCVS connected to a node
def node_add_ccvs(current_node_o,current_node_n,adjacency):
	for ccvs_n in current_node_o.ccvs:		#Loop through CCVS connected to the given node

		ccvs_o = ccvs_list[ccvs_n]
		check_if_voltage_exists(ccvs_o)		#Check if dependent voltage source exists

		#Update entries in the matrix
		if ccvs_o.node1 == current_node_o.name:
			adjacency[current_node_n-1,node_count+vols_count+vcvs_count+ccvs_n-1] += 1
		else:
			adjacency[current_node_n-1,node_count+vols_count+vcvs_count+ccvs_n-1] += -1

#Function to add entries corresponding to VCCS connected to a node
def node_add_vccs(current_node_o,current_node_n,adjacency):
	for vccs_n in current_node_o.vccs:		#Loop through VCCS connected to the given node

		vccs_o = vccs_list[vccs_n]
		check_if_node_exists(vccs_o)	##Check if dependent nodes exists

		#Update entries in the matrix
		if vccs_o.node1 == current_node_o.name:
			adjacency[current_node_n-1,node_list[vccs_o.node3][1]-1] += vccs_o.value
			adjacency[current_node_n-1,node_list[vccs_o.node4][1]-1] += (-1)*vccs_o.value
		else:
			adjacency[current_node_n-1,node_list[vccs_o.node3][1]-1] += (-1)*vccs_o.value
			adjacency[current_node_n-1,node_list[vccs_o.node4][1]-1] += vccs_o.value

#Function to add entries corresponding to CCCS connected to a node
def node_add_cccs(current_node_o,current_node_n,adjacency):
	for cccs_n in current_node_o.cccs:		#Loop through CCCS connected to the given node

		cccs_o = cccs_list[cccs_n]
		check_if_voltage_exists(cccs_o)		#Check if dependent voltage source exists

		#Update entries in the matrix
		if cccs_o.node1 == current_node_o.name:
			adjacency[current_node_n-1,node_count+vols_name_list[cccs_o.voltage_source]-1] += cccs_o.value
		else:
			adjacency[current_node_n-1,node_count+vols_name_list[cccs_o.voltage_source]-1] += (-1)*cccs_o.value

#Function to add entries corresponding to voltage source condition
def voltage_add_voltage(vols_list,vols_name_list,adjacency,constant):
	for voltage_n in vols_list:		#Loop through all the voltage sources in the circuit
		voltage_o = vols_list[voltage_n]

		#Update entries in the matrix
		adjacency[node_count+voltage_n-1,node_list[voltage_o.node1][1]-1] += 1
		adjacency[node_count+voltage_n-1,node_list[voltage_o.node2][1]-1] += -1
		constant[node_count+voltage_n-1] += voltage_o.value

#Function to add entries corresponding to VCVS condition
def voltage_add_vcvs(vcvs_list,vols_name_list,adjacency):
	for vcvs_n in vcvs_list:		#Lopp through all the VCVS in the circuit
		vcvs_o = vcvs_list[vcvs_n]

		#Update entries in the matrix
		adjacency[node_count+vols_count+vcvs_n-1,node_list[vcvs_o.node1][1]-1] += 1
		adjacency[node_count+vols_count+vcvs_n-1,node_list[vcvs_o.node2][1]-1] += -1
		adjacency[node_count+vols_count+vcvs_n-1,node_list[vcvs_o.node3][1]-1] += (-1)*(vcvs_o.value)
		adjacency[node_count+vols_count+vcvs_n-1,node_list[vcvs_o.node4][1]-1] += vcvs_o.value

#Function to add entries corresponding to CCVS condition
def voltage_add_ccvs(ccvs_list,vols_name_list,adjacency):
	for ccvs_n in ccvs_list:		#Loop through all the CCVS in the circuit
		ccvs_o = ccvs_list[ccvs_n]

		#Update entries in the matrix
		adjacency[node_count+vols_count+vcvs_count+ccvs_n-1,node_list[ccvs_o.node1][1]-1] += 1
		adjacency[node_count+vols_count+vcvs_count+ccvs_n-1,node_list[ccvs_o.node2][1]-1] += -1
		adjacency[node_count+vols_count+vcvs_count+ccvs_n-1,node_count+vols_name_list[ccvs_o.voltage_source]-1] += (-1)*(ccvs_o.value)


"""----> Defining and adding entries to the matrices <----"""
dimension = node_count+vols_count+vcvs_count+ccvs_count		#Dimension of the marices

if is_AC == 1:	#Matrices with complex values in case of AC circuit
	adjacency = np.zeros(shape=(dimension,dimension),dtype=np.complex_)
	constant = np.zeros(shape=(dimension),dtype=np.complex)
else:	#Matrices with real values in case of DC circuit
	adjacency = np.zeros(shape=(dimension,dimension))
	constant = np.zeros(shape=(dimension))

check = 1
for nodes in node_list:		#Check if GND node is present
	if nodes == "gnd":
		check = 0
		adjacency[node_list[nodes][1]-1,node_list[nodes][1]-1] = 1
if check:
	print("No GND node present")
	exit()


for nodes in node_list:		#Update values in the matrices corresponding to the KCL equations at all nodes
	current_node_o = node_list[nodes][0]
	current_node_n = node_list[nodes][1]
	if current_node_o.name != "gnd":
		node_add_resistance(current_node_o,current_node_n,adjacency)
		node_add_capacitor(current_node_o,current_node_n,adjacency)
		node_add_inductor(current_node_o,current_node_n,adjacency)
		node_add_voltage(current_node_o,current_node_n,adjacency)
		node_add_current(current_node_o,current_node_n,constant)
		node_add_vcvs(current_node_o,current_node_n,adjacency)
		node_add_ccvs(current_node_o,current_node_n,adjacency)
		node_add_vccs(current_node_o,current_node_n,adjacency)
		node_add_cccs(current_node_o,current_node_n,adjacency)

voltage_add_voltage(vols_list,vols_name_list,adjacency,constant)	#Update values in matrix corresponding to the voltage source conditions
voltage_add_vcvs(vcvs_list,vols_name_list,adjacency)	#Update values in matrix corresponding to the VCVS conditions
voltage_add_ccvs(ccvs_list,vols_name_list,adjacency)	#Update values in matrix corresponding to the CCVS conditions

#print(adjacency)
#print(constant)

"""-------------------------------------------------------------------------------------------------
									CALCULATING ANSWER MATRIX AND PRINTING VALUES
--------------------------------------------------------------------------------------------------"""
try:	#Inversing the matrix and printing error if matrix is singular
	inverse = np.linalg.inv(adjacency)
except:
	print("Adjacency matrix has determinant value = 0. Please check for some bad connections in the circuit.")
	exit()
answer = np.matmul(inverse,constant)
#print(answer)

#Printing the values of the unknowns
for nodes in node_list:
	print("Voltage at node %s is "%nodes,end="")
	print(answer[node_list[nodes][1]-1],end="V\n")
for vols in vols_name_list:
	print("Current through the voltage source %s is "%vols,end="")
	print(answer[node_count+vols_name_list[vols]-1],end="A\n")
for vcvs in vcvs_name_list:
	print("Current through the vcvs %s is "%vcvs,end="")
	print(answer[node_count+vols_count+vcvs_name_list[vcvs]-1],end="A\n")
for ccvs in ccvs_name_list:
	print("Current through the ccvs %s is "%ccvs,end="")
	print(answer[node_count+vols_count+vcvs_count+ccvs_name_list[ccvs]-1],end="A\n")