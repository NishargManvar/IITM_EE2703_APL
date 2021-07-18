"""
PURPOSE : EE2703 - Assignment 1
AUTHOR  : Manvar Nisharg (EE19B094)
"""
import sys

#Global Variables 
start_keyword = ".circuit"
end_keyword = ".end"



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

#Finding the values of start_index and end_index
for line in file_lines:

	if (str(line[:len(start_keyword)])).lower() == start_keyword:
		start_index = file_lines.index(line)

	elif (str(line[:len(end_keyword)])).lower() == end_keyword:
		end_index = file_lines.index(line)

#Error if either of the directives are missing or are in the wrong order
if (start_index > end_index or end_index < 0 or start_index < 0):
	print("Invalid circuit definition... please check '%s' and '%s' directives\n"%(start_keyword,end_keyword))
	exit()



#Print the lines in reverse order
for line in reversed(file_lines[start_index+1:end_index]):	#Looping the lines in reverse order
	words = (line.split('#')[0].split())	#Removing the comment and then splitting the words
	words.reverse()		#Reversing the words
	if(len(words)!=0):	#If the whole line was not a comment then print the line
		for word in words:
			print(word,end=" ")
		print()
