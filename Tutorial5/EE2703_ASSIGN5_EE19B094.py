"""
PURPOSE : EE2703 -- Assignment 5
AUTHOR  : Manvar Nisharg (EE19B094)
INPUT   : Nx,Ny,Radius,Iteration (Commandline in same order)
OUTPUT  : 8 graphs
"""


import numpy as np
import os,sys
import scipy
import scipy.linalg as s
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3


#User Input else default
try:
    if(len(sys.argv)==5):
        Nx=int(sys.argv[1])
        Ny=int(sys.argv[2])
        radius=int(sys.argv[3])  
        Niter=int(sys.argv[4])
    else:
        print("Invalid format of parameters given in commandline")
        Nx=25 # length along x
        Ny=25 # length along y
        radius=8 #radius of central lead
        Niter=1500 #number of iterations
except:
    print("Invalid format of parameters given in commandline")
    Nx=25 # length along x
    Ny=25 # length along y
    radius=8 #radius of central lead
    Niter=1500 #number of iterations

#initialize potential matrix
phi_matrix=np.zeros((Nx,Ny),dtype = float)
#Range of points on X and Y axis
x_range,y_range=np.linspace(-0.5,0.5,num=Nx,dtype=float),np.linspace(-0.5,0.5,num=Ny,dtype=float)
Y,X=np.meshgrid(y_range,x_range,sparse=False)   #Make grid from x and y values
phi_matrix[np.where(X**2+Y**2<(0.35)**2)]=1.0   #Make electorde voltage as 1V

#Contour plot for initial potential
plt.title("Initial potential contour plot")
plt.contourf(X,Y,phi_matrix,cmap=plt.get_cmap('coolwarm'))
plt.xlabel(r"X$\longrightarrow$")
plt.ylabel(r"Y$\longrightarrow$")
plt.colorbar()
plt.show()

#Function to update voltage matrix for every iteration
def update_phi_voltage(phi_matrix,phiold):
    phi_matrix[1:-1,1:-1]=0.25*(phiold[1:-1,0:-2]+ phiold[1:-1,2:]+ phiold[0:-2,1:-1] + phiold[2:,1:-1])
    return phi_matrix

#Function to set the boundary conditions on voltage matrix for every iteration
def set_boundary_conditions_voltage(phi_matrix):
    phi_matrix[:,Nx-1]=phi_matrix[:,Nx-2] # Right Boundary
    phi_matrix[:,0]=phi_matrix[:,1] # Left Boundary
    phi_matrix[0,:]=phi_matrix[1,:] # Top Boundary
    phi_matrix[Ny-1,:]=0    #Grounded
    center = np.where(X**2+Y**2<(0.35)**2)
    phi_matrix[center]=1.0  #Make electorde voltage as 1V
    return phi_matrix


#Function to get exponential fit for the error plot
def get_exponential_fit(y,Niter,iteration_start):
    log_error = np.log(error)[-iteration_start:]
    X = np.vstack([(np.arange(Niter)+1)[-iteration_start:],np.ones(log_error.shape)]).T
    log_error = np.reshape(log_error,(1,log_error.shape[0])).T
    return s.lstsq(X, log_error)[0]

#Function to plot the error
def plot_error(error,Niter,A1,A2,B1,B2):
    plt.title("Best fit for error on loglog scale")
    plt.xlabel(r"Iterations$\longrightarrow$")
    plt.ylabel(r"Error$\longrightarrow$")
    x = np.asarray(range(Niter))+1
    plt.loglog(x,error,label="Error")
    plt.loglog(x[::100],np.exp(A1+B1*np.asarray(range(Niter)))[::100],'ro',label="fit1")
    plt.loglog(x[::100],np.exp(A2+B2*np.asarray(range(Niter)))[::100],'go',label="fit2")
    plt.legend()
    plt.show()
    
    plt.title("Best fit for error on semilog scale")
    plt.xlabel(r"Iterations$\longrightarrow$")
    plt.ylabel(r"Error$\longrightarrow$")
    plt.semilogy(x,error,label="Error")
    plt.semilogy(x[::100],np.exp(A1+B1*np.asarray(range(Niter)))[::100],'ro',label="fit1")
    plt.semilogy(x[::100],np.exp(A2+B2*np.asarray(range(Niter)))[::100],'go',label="fit2")
    plt.legend()
    plt.show()

#Function to update temperature matrix
def update_phi_temperature(temp,oldtemp,Jx,Jy):
    temp[1:-1,1:-1]=0.25*(tempold[1:-1,0:-2]+ tempold[1:-1,2:]+ tempold[0:-2,1:-1] + tempold[2:,1:-1]+(Jx)**2 +(Jy)**2)
    return temp


#Function to set boundary conditions for temperature matrix
def set_boundary_conditions_temperature(phi_matrix):
    phi_matrix[:,Nx-1]=phi_matrix[:,Nx-2] # Right Boundary
    phi_matrix[:,0]=phi_matrix[:,1] # Left Boundary
    phi_matrix[0,:]=phi_matrix[1,:] # Top Boundary
    phi_matrix[Ny-1,:]=300.0
    center = np.where(X**2+Y**2<(0.35)**2)
    phi_matrix[center]=300.0    #Make electode temperature as 300K
    return phi_matrix


#Function to find net error
find_net_error = lambda a,b,Niter : -a/b*np.exp(b*(Niter+0.5))






#Initialize error matrix
error = np.zeros(Niter)
#Iterate and update the voltage matrix
for iteration in range(Niter):
    phiold = phi_matrix.copy()
    phi_matrix = update_phi_voltage(phi_matrix,phiold)  #Update matrix
    phi_matrix = set_boundary_conditions_voltage(phi_matrix)    #Set boundary condition
    error[iteration] = np.max(np.abs(phi_matrix-phiold))    #Error between old and new voltage matrix
    if(error[iteration] == 0):  #Break if error reaches steady state
        break


#Expoential fit with all entries
B1,A1 = get_exponential_fit(error,Niter,0)
#Expoential fit with entries only after 500 iterations
B2,A2 = get_exponential_fit(error,Niter,500)
plot_error(error,Niter,A1,A2,B1,B2)
#plotting cumulative error
iteration=np.arange(100,1501,100)
plt.grid(True)
plt.title(r'Cumulative Error on loglog scale')
plt.xlabel(r"Iterations$\longrightarrow$")
plt.ylabel(r"Net maximum error$\longrightarrow$")
plt.loglog(iteration,np.abs(find_net_error(A2,B2,iteration)),'ro')
plt.show()


#plotting 2d contour of final potential
plt.title("2D Contour plot of final potential")
plt.xlabel(r"X$\longrightarrow$")
plt.ylabel(r"Y$\longrightarrow$")
plt.contourf(Y,X[::-1],phi_matrix)  #Contour plot
x_electrode,y_electrode=np.where(X**2+Y**2<(0.35)**2)   #Points with electode
plt.plot((x_electrode-Nx/2)/Nx,(y_electrode-Ny/2)/Ny,'ro')  #Mark those points as red
plt.colorbar()
plt.show()


#Plotting 3d contour of final potential
fig1=plt.figure(4)     # open a new figure
ax=p3.Axes3D(fig1) # Axes3D is the means to do a surface plot
plt.title('The 3-D surface plot of the final potential')
surf = ax.plot_surface(Y, X, phi_matrix.T, rstride=1, cstride=1, cmap=plt.cm.jet)
plt.show()


#finding and plotting current density
Jx,Jy = (1/2*(phi_matrix[1:-1,0:-2]-phi_matrix[1:-1,2:]),1/2*(phi_matrix[:-2,1:-1]-phi_matrix[2:,1:-1]))
plt.title("Vector plot of current flow")
plt.quiver(Y[1:-1,1:-1],-X[1:-1,1:-1],-Jx[:,::-1],-Jy)
x_electrode,y_electrode=np.where(X**2+Y**2<(0.35)**2)   #Points with electode
plt.plot((x_electrode-Nx/2)/Nx,(y_electrode-Ny/2)/Ny,'ro')  #Mark those points as red
plt.show()


#initialize temperature matrix
temp=300 * np.ones((Nx,Ny),dtype = float)

#Iterate and update the temperature matrix
for k in range(Niter):
    tempold = temp.copy()
    temp = update_phi_temperature(temp,tempold,Jx,Jy)   #Update step
    temp = set_boundary_conditions_temperature(temp)    #Set boundary condition after every iteration


#plotting 2d contour of final temp
plt.title("Contour plot of temperature")
plt.xlabel(r"X$\longrightarrow$")
plt.ylabel(r"Y$\longrightarrow$")
x_electrode,y_electrode=np.where(X**2+Y**2<(0.35)**2)   #Points with electode
plt.plot((x_electrode-Nx/2)/Nx,(y_electrode-Ny/2)/Ny,'ro')  #Mark those points as red
plt.contourf(Y,X[::-1],temp)
plt.colorbar()
plt.show()