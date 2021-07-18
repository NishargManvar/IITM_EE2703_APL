# EE2703 - Assignment 6

This folder contains the code, TeX file, plots used in the TeX file, the report PDF and a .txt file which is generated from the code.

## Run command
```bash
python3 EE2703_ASSIGN6_EE19B094.py 5 500 100 500 2.5 0.9 1 1
```
The order of input parameters are
M -- Number of electrons injected per turn.\
n -- Spatial grid size.\
nk -- Number of turns to simulate.\
u0 -- Threshold velocity.\
p -- Probability that ionization will occur\
Msig -- Taking sigma of normal distribution\
accurate -- Whether to make more accurate calculations

Any ill given input will result in the code taken default values which are,
M = 5
n=100
nk=500
u0=5
p=0.25
Msig=1
accurate = 1

## Output
Code, will output Intensity plot, Population plot, phase plot and .txt file of intensity vs position