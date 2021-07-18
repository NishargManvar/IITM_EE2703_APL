"""**************************************************************************
Purpose : EE2703 - Assignment 3
Author : Manvar Nisharg (EE19B094)
Input : Coloums of data of file named 'fitting.dat'
Output : Various plots as asked according to the assignment
***************************************************************************"""


#Import necessary files
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.special as sp

#True parameter values
Ao = 1.05
Bo = -0.105

#Varying noise levels
variance = np.logspace(-1,-3,9)

#Function to load file and generate X and Y matrix
def load_file(file_name):
	try:
		data_matrix = np.loadtxt(file_name)
	except:
		print("Can't load file")
		exit()
	x_matrix = data_matrix[:,0]
	y_matrix = data_matrix[:,1:]
	return x_matrix,y_matrix

#Function to plot raw data
def plot_noised_data(x_matrix,y_matrix):
	plt.figure(0)
	for i in range(1,10,1):
		plt.plot(x_matrix,y_matrix[:,i-1],label=r'$\sigma_{%d}$ = %.3f'%(i,variance[i-1]))
	plt.title('Q4:Data to be fitted to theory')
	plt.ylabel(r'$f(t)\ +\ noise \longrightarrow$',size=12)
	plt.xlabel(r't$\longrightarrow$',size=12)
	plt.legend()

#Function to calulate true value for given X matrix
def g(t,A,B):
	return A*sp.jn(2,t)+(B*t)

#Fumction to plot true function
def plot_true_graph(x_matrix):
	plt.figure(0)
	plt.grid(True)
	plt.plot(x_matrix,g(x_matrix,Ao,Bo),label='True Value')
	plt.legend()
	plt.show()

#Function to plot error bar graph for given error coloumn in Y matrix
def plot_error_bar(x_matrix,y_matrix,coloumn):
	plt.figure(1)
	plt.grid(True)
	plt.plot(x_matrix,g(x_matrix,Ao,Bo),label='True Value')
	plt.errorbar(x_matrix[::5],y_matrix[::5,coloumn],variance[coloumn],fmt='ro',label='errorbar')
	plt.title(r'Q5: Data points for $\sigma = %.3f$ along with exact function'%variance[coloumn])
	plt.xlabel(r't$\longrightarrow$',size=12)
	plt.legend()
	plt.show()

#Function to generate M matrix
def generate_M(x_matrix):
	vector1 = sp.jn(2,x_matrix)
	M = np.c_[vector1,x_matrix]
	return M

#Function to generate ME matrix
def generate_error_matrix(A_vector,B_vector,x_matrix,y_matrix_coloumn):
	mean_sq_error = np.zeros((np.size(A_vector),np.size(B_vector)))

	row = 0
	for A in A_vector:
		coloumn = 0
		for B in B_vector:
			temp_g = g(x_matrix,A,B)

			error = 0
			for index in range(np.size(x_matrix)):
				error += (y_matrix[index][y_matrix_coloumn]-temp_g[index])**2

			mean_sq_error[row][coloumn] = error/np.size(x_matrix)

			coloumn += 1
		row += 1

	return mean_sq_error

#Function to plot contour plot of ME matrix
def plot_contour_plots(A_vector,B_vector,mean_sq_error):
	plt.figure(2)
	plt.title(r'Q8: Contour plot of $\epsilon_{ij}$')
	plt.xlabel(r'A$\longrightarrow$',size=12)
	plt.ylabel(r'B$\longrightarrow$',size=12)
	contour_plot = plt.contour(A_vector,B_vector,mean_sq_error,levels=np.arange(0,20*0.025,0.025))
	plt.clabel(contour_plot,contour_plot.levels[:6],inline=True,fontsize=10)
	plt.plot(Ao,Bo,'ro')
	plt.annotate("True Value", (Ao, Bo))
	plt.show()

#Function to predict parameters using lstsq() function for given coloumn
def predict_parameters(M,y_matrix,coloumn):
	predicted_parameters,_,_,_ = scipy.linalg.lstsq(M,y_matrix[:,coloumn])
	return predicted_parameters

#Function to plot error in linear scale
def plot_error_plot(p,predicted_parameters):
	plt.figure(3)
	plt.grid(True)
	plt.title(r'Q10: Variation of error with noise')
	plt.xlabel(r'Noise standard deviation$\longrightarrow$')
	plt.ylabel(r'Error$\longrightarrow$')
	error_A = np.zeros(np.size(predicted_parameters[:,0]))
	error_B = np.zeros(np.size(predicted_parameters[:,0]))
	for row in range(np.size(predicted_parameters[:,0])):
		error_A[row] = abs(p[0]-predicted_parameters[row][0])
		error_B[row] = abs(p[1]-predicted_parameters[row][1])
	plt.plot(variance,error_A,'ro-',label='Aerr',linestyle='dotted')
	plt.plot(variance,error_B,'bo-',label='Berr',linestyle='dotted')
	plt.legend()
	plt.show()

	return error_A,error_B

#Function to plot error in loglog scale
def plot_loglog_error(error_A,error_B):
	plt.figure(4)
	plt.grid(True)
	plt.title(r'Q11: loglog Variation of error with noise')
	plt.xlabel(r'Noise standard deviation$\longrightarrow$')
	plt.ylabel(r'loglog Error$\longrightarrow$')
	plt.stem(variance,error_A,'ro')
	plt.stem(variance,error_B,'bo')
	plt.loglog(variance,error_A,'ro-',label='Aerr',linestyle='dotted')
	plt.loglog(variance,error_B,'bo-',label='Berr',linestyle='dotted')
	plt.legend()
	plt.show()



x_matrix,y_matrix = load_file("fitting.dat")	#Loading file
plot_noised_data(x_matrix,y_matrix)				#Plotting raw data
plot_true_graph(x_matrix)						#Plotting true function
plot_error_bar(x_matrix,y_matrix,0)				#Plotting error bar

M = generate_M(x_matrix)		#Generating matrix M
p = np.array([Ao,Bo])
answer = np.matmul(M,p)			#Multiply M and p
g_vector = g(x_matrix,Ao,Bo)	#True function values
if (answer==g_vector).all():	#Compare both
	print("They are equal")


A_vector = np.arange(0,2.1,0.1)			#Defining range of A
B_vector = np.arange(-0.2,0.001,0.01)	#Defining range of B
mean_sq_error = generate_error_matrix(A_vector,B_vector,x_matrix,0)		#Calculating MS error matrix
plot_contour_plots(A_vector,B_vector,mean_sq_error)		#PLotting contour plots


predicted_parameters = np.zeros((np.size(y_matrix[0,:]),2))		#Matrix to store error for all coloumns
for coloumn in range(9):
	predicted_parameters[coloumn] = predict_parameters(M,y_matrix,coloumn)	#Calculate error

error_A,error_B = plot_error_plot(p,predicted_parameters)	#Plot error in linear scale
plot_loglog_error(error_A,error_B)		#PLot error in loglog scale

