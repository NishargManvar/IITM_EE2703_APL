"""
PURPOSE : EE2703 -- Assignment 6
AUTHOR  : Manvar Nisharg (EE19B094)
INPUT   : Various parameters as mentioned in README
OUTPUT  : Intensity plot, Population plot, phase plot, intensity vs position .txt file
"""
import numpy as np    
import matplotlib.pyplot as plt
import sys
from pylab import *
import pandas as pd    # pandas for showing in tabular form



class General_Plotter():
    ''' Class used for plotting different plots. Shortens the code by quite a bit'''
    
    def __init__(self,xlabel,ylabel,title,fig_num=0):
        ''' xlabel,ylabel,title are used in every graph''' 

        self.xlabel=xlabel
        self.ylabel=ylabel
        self.title=title
        self.fig=plt.figure(fig_num)
    
    def general_funcs(self,ax):
        ''' General functions for every graph'''
        
        ax.set_ylabel(self.ylabel)
        ax.set_xlabel(self.xlabel)
        ax.set_title(self.title)
        plt.show()
        #self.fig.savefig(self.title+".png")

    def population_plot(self,values):
        axes=self.fig.add_subplot(111)
        axes.hist(values,histtype='bar',ec='black',bins=100)
        self.general_funcs(axes)

    def scatter_plot(self,X,Y):
        axes=self.fig.add_subplot(111)
        a=list(zip(X, Y))
        a=set(a)
        X,Y=zip(*a)
        axes.scatter(X,Y,c='r',marker='x')
        self.general_funcs(axes)



#Taking inputs from sys.argv if given, if not give use the default values
try:
    if(len(sys.argv)==8):
        M=int(sys.argv[1])
        n=int(sys.argv[2])
        nk=int(sys.argv[3])  
        u0=float(sys.argv[4])
        p=float(sys.argv[5])
        Msig=float(sys.argv[6])
        accurate=int(sys.argv[7])
    else:
        print("Invalid format of parameters given in commandline")
        M = 5                                          #Number of electrons injected per turn.
        n=100                                           #Spatial grid size.
        nk=500                                          #Number of turns to simulate.
        u0=5                                           #Threshold velocity.
        p=0.25                                         #Probability that ionization will occur                
        Msig=1                                          #Taking sigma of normal distribution to be 1
        accurate = 1                                    #Whether to make more accurate calculations
except:
    print("Invalid format of parameters given in commandline")
    M = 5                                          #Number of electrons injected per turn.
    n=100                                           #Spatial grid size.
    nk=500                                          #Number of turns to simulate.
    u0= 5                                           #Threshold velocity.
    p=0.25                                          #Probability that ionization will occur                
    Msig=1                                          #Taking sigma of normal distribution to be 1
    accurate = 1                                    #Whether to make more accurate calculations

xx = np.zeros(n*M)      #Electron position
u = np.zeros(n*M)       #Electron velocity  
dx = np.zeros(n*M)      #Electron displacement per time step

I = []          #Stores value of intensity of emitted light at every time-step
V = []          #Stores value of electron velocity at every time-step
X = []          #Stores value of electron position at every time-step    


#Carrying the iterations
for i in range(1,nk):
    ii = np.where(xx>0)[0]      #Electrons currently inside the tubelight
    
    dx[ii] = u[ii] + 0.5        #Displacement of electron with velocity u[ii]
    xx[ii] = xx[ii] + dx[ii]    #New position of electron
    u[ii] = u[ii] + 1.0         #New velocity of electron
    
    npos = np.where(xx>n)[0]    #Finding electrons which left the tubelight
    xx[npos] = 0.0              #Equate their parameters values to initial values
    dx[npos] = 0.0
    u[npos] = 0.0
    
    kk=np.where(u>=u0)[0]               #Incides of electrons capable of collision
    ll=np.where(rand(len(kk))<=p)[0]    #Chosing random electrons with probability p
    kl=kk[ll]                           #Indices of electrons undergone collision
    
    if accurate == 0:   #Less accurate calculations
        P = np.random.rand(len(kl))             #Choosing random 'position' between x_i and x_i+1
        xx[kl] = xx[kl]-np.multiply(dx[kl],P)   #and equating that as the position of collision
        u[kl] = 0                               #Also, velocity = 0 as collision is inelastic

    else:               #More accurate calculations
        dt = rand(len(kl))                              #Choosing random 'time' between 0 and 1
        xx[kl]=xx[kl]-dx[kl]+((u[kl]-1)*dt+0.5*dt*dt)   #Corresponding position of collision
        u[kl]=0                                         #Velocity = 0 after collision

        u[kl]+=1-dt                                     #Velocity of electron gained after collison
        xx[kl]+=0.5*(1-dt)**2                           #Distance travelled after collision

    
    I.extend(xx[kl].tolist())               #Increasing intensity at point of collision
    
    m=np.random.randn()*Msig+M              #Number of electrons inserted
    empty_xpos = np.where(xx==0)[0]         #Finding indices in position array to insert electrons
    electrons_generated = min(len(empty_xpos),(int)(m)) #If not enough space for all electrons, add as much as we can
    xx[empty_xpos[0:electrons_generated]] = 1.0
    u[empty_xpos[0:electrons_generated]] = 0.0
    
    X.extend(xx[ii].tolist())
    V.extend(u[ii].tolist()) 
       
     
# Plotting graphs

p1=General_Plotter("Grid_Space","Number of Electrons","Population_Plot_of_Electrons",0)
p1.population_plot(X)
p2=General_Plotter("Grid_Space","Intensity of Light","Intensity of Light",1)
p2.population_plot(I)
p3=General_Plotter("X","V","X vs V",2)
p3.scatter_plot(X,V)




# Tabulating data for intensity vs position
bins = plt.hist(I,bins=np.arange(1,n,n/100))[1]    # Bin positions are obtained
count = plt.hist(I,bins=np.arange(1,n,n/100))[0]   # Population counts obtained
xpos = 0.5*(bins[0:-1] + bins[1:])     # As no. of end-points of bins would be 1 more than actual no. of bins, the mean of bin end-points are used to get population of count a particular bin
df = pd.DataFrame()   # A pandas dataframe is initialized to do the tabular plotting of values.
df['Xpos'] = xpos
df['count'] = count

base_filename = 'values.txt'
with open(base_filename,'w') as outfile:
    df.to_string(outfile)

