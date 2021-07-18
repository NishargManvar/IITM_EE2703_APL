'''***************************************************************
PURPOSE : EE2703 - Assignment 4
AUTHOR : Manvar Nisharg (EE19B094)
INPUT : NULL
OUTPUT : 12 images saved into local directory 
***************************************************************'''
import math
import scipy
import scipy.integrate as integ
import scipy.special as sp
from pylab import *
import numpy as np

COEFF_COUNT = 25    #Max index of coeffs we want to calculate

generate_exp = lambda x: np.exp(x)  #Function to generate aperodic e^x function
generate_coscos = lambda x: np.cos(np.cos(x))   #Function to generate cos(cos(x)) function
generate_perodic_exp = lambda x: np.exp(x%(2*math.pi))  #Function to generate periodic e^x function


#Function to plot both kind of exponential functions
def plot_raw_exponential():
    x = np.linspace(-2*math.pi,4*math.pi,300)     
    figure(1)
    semilogy(x,generate_exp(x),'m',label=r'Aperiodic $e^x$ in log scale')      
    semilogy(x,generate_perodic_exp(x),'g',label=r'Periodically extended $e^x$ in log scale')
    title("Q1 : Plotting original functions")
    xlabel(r'$x\longrightarrow$',fontsize=12)
    ylabel(r'$log(e^{x})\longrightarrow$',fontsize=12)
    grid()
    legend()
    #show()
    savefig("Q1-1.png")
    close()

#Function to plot cos(cos(x)) function
def plot_raw_coscosx():
    x = np.linspace(-2*np.pi,4*np.pi,300)
    figure(2)
    plot(x,generate_coscos(x))
    title(r'y = cos(cos(x))')
    xlabel(r'$x\longrightarrow$', fontsize = 12)
    ylabel(r'$cos(cos(x))\longrightarrow$', fontsize = 12)
    grid()
    #show()
    savefig("Q1-2.png")
    close()

#Function to calculate 'k' Fourier Coefficients for given function f
def calculate_fourier_coefficients(f,k):                       
    coeffs=[]   #List storing combined coefficients
    a_n=[]      #List storing a_n coefficients
    b_n=[]      #List storing b_n coefficients
                            
    u = lambda x, n: f(x)*math.cos(n*x)     #Functions to be integrated
    v = lambda x, n: f(x)*math.sin(n*x)
                                                                        
    a_n.append((1/(2*math.pi))*integ.quad(u, 0, 2*math.pi, args=0)[0])      #a_0
    coeffs.append((1/(2*math.pi))*integ.quad(u, 0, 2*math.pi, args=0)[0])
    b_n.append(0) 

    for n in range(1,k):
        a_n.append((1/math.pi)*integ.quad(u, 0, 2*math.pi, args=n)[0])    
        coeffs.append((1/math.pi)*integ.quad(u, 0, 2*math.pi, args=n)[0])
        
        b_n.append((1/math.pi)*integ.quad(v, 0, 2*math.pi, args=n)[0])   
        coeffs.append((1/math.pi)*integ.quad(v, 0, 2*math.pi, args=n)[0]) 
    
    return coeffs,a_n,b_n


#Function to plot the coefficients
def plot_coefficients():
    #Coefficients of e^x on a log scale
    figure(3)
    semilogy(np.abs(a_n_exp),'ro',label=r'$a_n$ of $e^x$')
    semilogy(np.abs(b_n_exp),'bo',label=r'$b_n$ of $e^x$')    
    grid(True)
    title(r'Magnitudes of coefficients in log scale', fontsize = 10)
    xlabel(r'n$\longrightarrow$')
    ylabel(r'log(coeffs)$\longrightarrow$')
    legend()
    #show()
    savefig("Q3-1.png")
    close()
    
    #Coefficients of cos(cos(x)) on a log scale
    figure(4)
    semilogy(np.abs(a_n_coscos),'ro',label=r'$a_n$ of $cos(cos(x))$')
    semilogy(np.abs(b_n_coscos),'bo',label=r'$b_n$ of $cos(cos(x))$')
    grid(True)
    title(r'Magnitudes of coefficients in log scale', fontsize = 10)
    xlabel(r'n$\longrightarrow$')
    ylabel(r'log(coeff)$\longrightarrow$')
    legend()
    #show()
    savefig("Q3-2.png")
    close()
    
    #Coefficients of e^x on a loglog scale
    figure(5)
    loglog(np.abs(a_n_exp),'ro',label=r'$a_n$ of $e^x$')
    loglog(np.abs(b_n_exp),'bo',label=r'$b_n$ of $e^x$')
    grid(True)
    title(r'Magnitudes of coefficients in loglog scale', fontsize = 10)
    xlabel(r'n$\longrightarrow$')
    ylabel(r'log(log(coeff))$\longrightarrow$')
    legend()
    #show()
    savefig("Q3-3.png")
    close()
    
    #Coefficients of cos(cos(x)) on a loglog scale
    figure(6)
    loglog(np.abs(a_n_coscos),'ro',label=r'$a_n$ of $cos(cos(x))$')
    loglog(np.abs(b_n_coscos),'bo',label=r'$b_n$ of $cos(cos(x))$')
    grid(True)
    title(r'Magnitudes of coefficients in loglog scale', fontsize = 10)
    xlabel(r'n$\longrightarrow$')
    ylabel(r'log(log(coeff))$\longrightarrow$')
    legend()
    #show()
    savefig("Q3-4.png")
    close()


#Plot coefficients obtained from integration and lstsq methods
def plot_comparing_coeff():
    #Coefficients of e^x on a log scale
    figure(7)
    fig, axs = plt.subplots(2)
    axs[0].semilogy(np.abs(a_n_exp_lstsq), 'bo', label = 'Least Squares Approach')
    axs[0].semilogy(np.abs(a_n_exp), 'go', label = 'Integration Approach')
    axs[1].semilogy(np.abs(b_n_exp_lstsq), 'bo', label = 'Least Squares Approach')
    axs[1].semilogy(np.abs(b_n_exp), 'go', label = 'Integration Approach')
    fig.suptitle(r'Magnitudes of coefficients in log scale for e^x')
    axs[0].set(ylabel=r'log(|$a_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[1].set(ylabel=r'log(|$b_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[0].grid()
    axs[1].grid()
    axs[0].legend()
    axs[1].legend()
    #show()
    savefig("Q5-1.png")
    close()

    #Coefficients of cos(cos(x)) on a log scale
    figure(8)
    fig, axs = plt.subplots(2)
    axs[0].semilogy(np.abs(a_n_coscos_lstsq), 'bo', label = 'Least Squares Approach')
    axs[0].semilogy(np.abs(a_n_coscos), 'go', label = 'Integration Approach')
    axs[1].semilogy(np.abs(b_n_coscos_lstsq), 'bo', label = 'Least Squares Approach')
    axs[1].semilogy(np.abs(b_n_coscos), 'go', label = 'Integration Approach')
    fig.suptitle(r'Magnitudes of coefficients in log scale for cos(cos(x))')
    axs[0].set(ylabel=r'log(|$a_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[1].set(ylabel=r'log(|$b_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[0].grid()
    axs[1].grid()
    axs[0].legend()
    axs[1].legend()
    #show()
    savefig("Q5-2.png")
    close()

    #Coefficients of e^x on a loglog scale
    figure(9)
    fig, axs = plt.subplots(2)
    axs[0].loglog(np.abs(a_n_exp_lstsq), 'bo', label = 'Least Squares Approach')
    axs[0].loglog(np.abs(a_n_exp), 'go', label = 'Integration Approach')
    axs[1].loglog(np.abs(b_n_exp_lstsq), 'bo', label = 'Least Squares Approach')
    axs[1].loglog(np.abs(b_n_exp), 'go', label = 'Integration Approach')
    fig.suptitle(r'Magnitudes of coefficients in log scale for e^x')
    axs[0].set(ylabel=r'log(|$a_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[1].set(ylabel=r'log(|$b_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[0].grid()
    axs[1].grid()
    axs[0].legend()
    axs[1].legend()
    #show()
    savefig("Q5-3.png")
    close()

    #Coefficients of cos(cos(x)) on a loglog scale
    figure(10)
    fig, axs = plt.subplots(2)
    axs[0].loglog(np.abs(a_n_coscos_lstsq), 'bo', label = 'Least Squares Approach')
    axs[0].loglog(np.abs(a_n_coscos), 'go', label = 'Integration Approach')
    axs[1].loglog(np.abs(b_n_coscos_lstsq), 'bo', label = 'Least Squares Approach')
    axs[1].loglog(np.abs(b_n_coscos), 'go', label = 'Integration Approach')
    fig.suptitle(r'Magnitudes of coefficients in log scale for cos(cos(x))')
    axs[0].set(ylabel=r'log(|$a_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[1].set(ylabel=r'log(|$b_n$|)$\longrightarrow$',xlabel=r'$n\longrightarrow$')
    axs[0].grid()
    axs[1].grid()
    axs[0].legend()
    axs[1].legend()
    #show()
    savefig("Q5-4.png")
    close()


#Plotting graph obtained from fourier coefficients alongside the original graph
def plotting_convergence():
    fourier_exp = np.matmul(A,coeffs_exp_lstsq)
    fourier_coscos = np.matmul(A,coeffs_coscos_lstsq)

    #e^x
    figure(11)
    semilogy(fourier_exp, 'm', label = 'Fourier representation')
    semilogy(generate_perodic_exp(x), 'c', label = 'Original function')
    grid(True)
    title(r'Convergence of Fourier Series representation to actual function for e^x')
    xlabel(r'$x\longrightarrow$')
    ylabel(r'Value in log scale$\longrightarrow$')
    legend()
    #show()
    savefig("Q7-1.png")
    close()

    #cos(cos(x))
    figure(12)
    semilogy(fourier_coscos, 'm', label = 'Fourier representation')
    semilogy(generate_coscos(x), 'b', label = 'Original function')
    grid(True)
    title(r'Convergence of Fourier Series representation to actual function for cos(cos(x))', fontsize = 10)
    xlabel(r'$x\longrightarrow$')
    ylabel(r'Value in log scale$\longrightarrow$', fontsize = 8)
    legend()
    #show()
    savefig("Q7-2.png")
    close()

#Calculating fourier coefficients using integration method
coeffs_exp,a_n_exp,b_n_exp = calculate_fourier_coefficients(generate_exp,COEFF_COUNT+1)
coeffs_coscos,a_n_coscos,b_n_coscos = calculate_fourier_coefficients(generate_coscos,COEFF_COUNT+1)



#Defining A,x arrays for lstsq method
x = np.linspace(0,2*pi,401)
x=x[:-1]  
A = np.zeros((400,2*COEFF_COUNT+1)) 
A[:,0]=1 
for k in range(1,COEFF_COUNT+1):
    A[:,2*k-1] = np.cos(k*x) 
    A[:,2*k] = np.sin(k*x) 

 
#Calculating coefficients for e^x using lstsq method
coeffs_exp_lstsq = scipy.linalg.lstsq(A,generate_exp(x))[0] #List storing combined coefficients
a_n_exp_lstsq = []  #List storing a_n coefficients
b_n_exp_lstsq = []  #List storing b_n coefficients

#Deriving a_n and b_n from combined coefficients
a_n_exp_lstsq.append(coeffs_exp_lstsq[0])
b_n_exp_lstsq.append(0)
for i in range(1,2*COEFF_COUNT+1,2):
    a_n_exp_lstsq.append(coeffs_exp_lstsq[i])
for i in range(2,2*COEFF_COUNT+1,2):
    b_n_exp_lstsq.append(coeffs_exp_lstsq[i])


#Calculating coefficients for cos(cos(x)) using lstsq method
coeffs_coscos_lstsq = scipy.linalg.lstsq(A,generate_coscos(x))[0] #List storing combined coefficients
a_n_coscos_lstsq = []   #List storing a_n coefficients
b_n_coscos_lstsq = []   #List storing b_n coefficients

#Deriving a_n and b_n from combined coefficients
a_n_coscos_lstsq.append(coeffs_coscos_lstsq[0])
b_n_coscos_lstsq.append(0)
for i in range(1,2*COEFF_COUNT+1,2):
    a_n_coscos_lstsq.append(coeffs_coscos_lstsq[i])
for i in range(2,2*COEFF_COUNT+1,2):
    b_n_coscos_lstsq.append(coeffs_coscos_lstsq[i])



#Calculating max error in the two methods
error_exp = np.abs(coeffs_exp - coeffs_exp_lstsq)
error_coscos = np.abs(coeffs_coscos - coeffs_coscos_lstsq)
max_error_exp = np.max(error_exp)
max_error_coscos = np.max(error_coscos)

print("Maximum error between the two methods for e^x is ",max_error_exp)
print("Maximum error between the two methods for cos(cos(x)) is ",max_error_coscos)


plot_raw_exponential()     #Q1 plots function call
plot_raw_coscosx()
plot_coefficients()     #Q3 plots function call
plot_comparing_coeff()  #Q5 plots function call
plotting_convergence()      #Q7 plots function call