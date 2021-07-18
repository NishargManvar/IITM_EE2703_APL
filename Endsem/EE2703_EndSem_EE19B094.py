"""
PURPOSE : EE2703 - EndSem
AUTHOR  : Manvar Nisharg -- EE19B094 
INPUT   : Number of points on wire (N) and radius of conductor (R) -- Commandline input
OUTPUT  : 4 plots (Refer title of graphs for description)
"""

import numpy as np
from pylab import *


#Function calc(l) to calculate norm of r-rl for a single point 'l'
def calc(r,r_l,l):                                         
	return norm(r-r_l[l],axis=-1)

#Extended vectorized function of calc(l) to calculate R for all points
def extended_calc(r,r_l):
	return norm(r-r_l,axis=-1)

#Function that returns value of the Green's function of R used in calculating Magnetic Vector Potential         
def Green(R):
	return (e**(-1j*k*R))/R

#Function to get Bz from A using curl
def get_Bz(Ay,Ax):
	#Taking Bz as the right side derivative of A
	Bz = (Ay[2,1,:]-Ay[0,1,:]-(Ax[1,2,:]-Ax[1,0,:]))
	return Bz

#Function to fit the magnetic filed values on exponential curve using lstsq
#As Bz follows a linear graph in log scale only after a certain point, we ignore first 'ignore_points' points
#for a better fit
def exponential_fit(Bz,z,ignore_points):

	function_value = log(abs(Bz[ignore_points:]))                       
	x = log(z[ignore_points:])                                 
	coefficients = column_stack((x,ones(1000)[ignore_points:]))
	b,c = lstsq(coefficients,function_value,rcond=None)[0]
	return b,c


#Creating grid of the (3,3,1000) volume
x_points=np.linspace(-1,1,3)
y_points=np.linspace(-1,1,3)
z_points=np.linspace(1,1000,1000)        
xx,yy,zz = np.meshgrid(x_points,y_points,z_points,indexing='ij')
meshgrid = np.stack((xx,yy,zz),axis=3)
position_vectors = np.tile(meshgrid,100).reshape(3,3,1000,100,3) #Position vector of all points


N = 100 #Number of current elements
radius = 10	#Radius of conductor

#Converting positions of current elements from (r,phi,z) to (x,y,z)
phi_vector = linspace(0,2*np.pi,N)
x_cap = radius*cos(phi_vector)
y_cap = radius*sin(phi_vector)
z_cap = zeros(N)
r_l = column_stack((x_cap , y_cap , z_cap))

#Plot current elements
title("Current elements on the conductor")
scatter(r_l[:,0],r_l[:,1])
ylabel(r"$Y\longrightarrow$")
xlabel(r"$X\longrightarrow$")
show()
close()


#Calculating dl
dphi_vector = column_stack((-sin(phi_vector),cos(phi_vector),zeros(N)))*(2*np.pi/N)
dl_vector = dphi_vector*radius



#Calculate current
mu = 4*np.pi*pow(10,-7)         

I_x = 4*np.pi/mu*(-cos(phi_vector)*sin(phi_vector))
I_y = 4*np.pi/mu*cos(phi_vector)*cos(phi_vector)
I_z = zeros(N)
I = column_stack((I_x , I_y , I_z))

#Quiver plot for I vs r
title("Quiver plot of current")
quiver(r_l[:,0],r_l[:,1],I[:,0],I[:,1])
ylabel(r"$Y\longrightarrow$")
xlabel(r"$X\longrightarrow$")
grid()
show()
close()



#Calculate R values for all points in the (3,3,1000) volume for all N current elements
R_vector = extended_calc(position_vectors,r_l)



dphi_magnitude = 2*np.pi/N
k = 0.1

#Calculating A,Bz for dynamic case
A_x_dynamic = np.sum((mu/(4*np.pi))*I[:,0]*Green(R_vector)*dphi_magnitude*radius,axis=-1)
A_y_dynamic = np.sum((mu/(4*np.pi))*I[:,1]*Green(R_vector)*dphi_magnitude*radius,axis=-1)

#Bz using right side derivative
Bz_dyanmic = get_Bz(A_y_dynamic,A_x_dynamic)

#Fitting the values of Bz on bz^c
ignore_points = 15
b_dyanmic,c_dynamic = exponential_fit(Bz_dyanmic,z_points,ignore_points)
print("The dynamic magnetic field when fitted to cz^b gives log(c)=%f and b=%f"%(c_dynamic,b_dyanmic))

#Plotting absolute value of Bz vs z in loglog scale
x_range = log(z_points[ignore_points:])
title("Absolute value of Calculated and fitted values of Bz for dynamic case")
ylabel(r"log(|Bz|)$\longrightarrow$")
xlabel(r"log(z)$\longrightarrow$")
loglog(z_points,abs(Bz_dyanmic), label="Calculated values")
loglog(exp(x_range),exp(b_dyanmic*x_range+c_dynamic),label="Fitted values")
legend()
grid()
show()
close()



#Calculating A,Bz for static case
A_x_static = np.sum((mu/(4*np.pi))*I[:,0]*dphi_magnitude*radius/R_vector,axis=-1)
A_y_static = np.sum((mu/(4*np.pi))*I[:,1]*dphi_magnitude*radius/R_vector,axis=-1)

Bz_static = get_Bz(A_y_static,A_x_static)

b_static,c_static = exponential_fit(Bz_static,z_points,ignore_points)
print("The static magnetic field when fitted to cz^b gives log(c)=%f and b=%f"%(c_static,b_static))


#Plotting absolute value of Bz vs z in loglog scale
x_range = log(z_points[ignore_points:])
title("Absolute value of Calculated and fitted values of Bz for static case")
ylabel(r"log(|Bz|)$\longrightarrow$")
xlabel(r"log(z)$\longrightarrow$")
loglog(z_points,abs(Bz_static), label="Calculated values")
loglog(exp(x_range),exp(b_static*x_range+c_static),label="Fitted values")
legend()
grid()
show()
close()
