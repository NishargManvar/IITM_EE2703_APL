'''
PURPOSE : EE2703 - Assignment 8
AUTHOR  : Manvar Nisharg (EE19B094)
INPUT   : NULL
OUTPUT  : Spectrum of various functions
'''
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from pylab import *
from numpy.fft import fftshift, fft, ifft, ifftshift

#Plotting function
def customplot(func,x,y,xlim):
    plt.figure()

    plt.subplot(2,1,1)
    plt.plot(x,np.abs(y),lw=2)
    plt.xlim(-1*xlim,xlim)
    plt.ylabel(r"$|y|$")
    plt.title(f"Spectrum of %s"%func)
    plt.grid(True)

    plt.subplot(2,1,2)
    #plt.plot(x,np.angle(y),'go',lw=2)
    ii = np.where(np.abs(y)>1e-3)
    plt.plot(x[ii], np.angle(y[ii]),'ro',lw=2)
    plt.xlim(-1*xlim,xlim)
    plt.ylim(-5,5)
    plt.xlabel(r"$k$")
    plt.ylabel(r"Phase of $Y$")
    plt.grid(True)
    plt.show()

#Cos^3 function
cos3 = lambda x : np.cos(x)**3

#Sin^3 function
sin3 = lambda x : np.sin(x)**3

#Gaussian function
gauss = lambda x : np.exp(-x**2/2)

#cos(cos(x)) function 
coscos = lambda x : np.cos(20*x+5*np.cos(x))

#Sin(5x) function
sin5 = lambda x : np.sin(5*x)

#Modulated signal
modulated = lambda x : (1+0.1*np.cos(x))*np.cos(10*x)

#Dictionary of functions
func_dict = {'sin':sin5,
			'modul':modulated,
			'cos^3' : cos3,
			'sin^3' : sin3,
			'coscos' : coscos,
			'gauss' : gauss }

#Function to perform dft and plot spectrum
def perform_dft(func,N=512,steps = 513, r=4*np.pi, phase_limit=1e-3, xlim=40, w_lim=64):
	t = np.linspace(-r,r,steps)[:-1]	#Time range
	y = func_dict[func](t)				#Sampled function values
	Y = fftshift(fft(y))/N 				#Shifting freq
	w = np.linspace(-w_lim,w_lim,steps)[:-1]	#Frequency values to be plotted

	customplot(func,w,Y,xlim)
	


def perform_dft_gaussian(func,tolerance=1e-6,N=128):
	T = 8*np.pi
	Y_old = 0

	while 1:

		#Time resolution
		dt = T/N
		#Frequency resolution
		dw = 2*np.pi/T

		#Freq window size
		W = N*dw

		#Time samples
		t = np.linspace(-T/2,T/2,N+1)[:-1]
		#Freq samples
		w = np.linspace(-W/2,W/2,N+1)[:-1]

		y = gauss(t)

		Y_new = dt/(2*np.pi) * fftshift(fft(ifftshift(y)))

		error = sum(abs(Y_new[::2]) - Y_old)
		Y_old = Y_new

		if error < tolerance:
			customplot(func,w,Y_new,5)
			print("Error in Gaussian case is {}".format(error))
			return

		T*=2
		N*=2

#Calculate error between actual and inversed values of dft of series of random values
x=np.random.rand(100)
X=fft(x)
y=ifft(X)
c_[x,y]
maxError = max(np.abs(y-x))
print('Magnitude of maximum error between actual and computed values of the random sequence:', maxError)

#DFT of various functions
perform_dft('sin',xlim=10)
perform_dft('modul',xlim=40)
perform_dft('cos^3',xlim=15, steps= 129 , w_lim=16, N = 128)
perform_dft('sin^3',xlim=15)
perform_dft('coscos',xlim=40)
perform_dft_gaussian('gauss')