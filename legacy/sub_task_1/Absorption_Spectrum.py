## -*- coding: utf-8-sig -*-
## Import libraries
#import matplotlib.pyplot as plt
#import numpy as np
#import Utility_Code_ as uc
#import importlib

## Import specific functions
## Reload changes
#importlib.reload(uc)

## Rename for simplicity
#g = uc.Line_Broadening_Function

## Import necessary constants
#c,hbar,kb,pi=uc.Constants('c','hbar','kb','pi')

## Convert constants to desired units
#c = uc.Hz_to_fHz(uc.m_to_cm(c)) # m/s -> cm/fs
#hbar = uc.s_to_fs(hbar) # Js -> Jfs

## Get material parameters
#dk = np.array([0.08,0.06,0.06,0.08,0.08,0.12,0.15,0.02,0.0,0.19,0.13,0.12]) # Dimensionless displacements
#wk = np.array([667,724,1030,1172,1248,1274,1316,1404,1485,1529,1554,1608]) # Mode frequencies (cm^-1)
##dk = np.array([0.19,0.13,0.12]) # Dimensionless displacements
##wk = np.array([1529,1554,1608]) # Mode frequencies (cm^-1)
#Temperature = 298.16 # Temperature (K)
#LAM = 0.001 # The inverse of LAM is the time scale of the bath (fHz)
#lam = 870 # Solvent reorganization energy (cm^-1) 4190
#weg = 1500 # Electronic energy gap (cm^-1)

## Calculated material parameters
##hbar = uc.J_to_wavenumber(hbar) # Planck's reduced constant (fs/cm)
##kb = #c.J_to_wavenumber(kb) # Boltzman constant (J/K -> cm^-1 K^-1)
#kT = kb * Temperature # Temperture (cm^-1)
#lam = lam * c # Solvent reorganization energy (fHz)
#var = 2 * lam * kT / hbar # Variance: linewidth parameter (fHz^2)
#weg = weg *2*pi*c#/ hbar # Electronic energy gap (fHz)
#wk = 2*pi*wk * c # Mode frequencies (fHz)

## Define time and frequency objects
#ti = 0 # Initial time (fs)
#tf = 1e4 # Final Time (fs)
#dt = 0.1 # Time step (fs)
#nt = (tf-ti)/dt # Number of time steps
#t = np.arange(ti,tf,dt) # Time axis (fs)
#dw = 1 / c / dt / nt # Frequency step (cm^-1)
#nw = nt # Number of frequency steps
#wi = -(dw * nw) / 2 # Inital frequency (cm^-1)
#wf = dw * nw / 2 # Final Frequency (cm^-1)
#w = np.arange(wi,wf,dw) # Frequency axis (cm^-1)
#w[abs(w) < dw * 1e-3]=0 # Set center of axis to 0
#delta_w = np.arange(1.6e4,3.2e4,10)[np.newaxis].T

## Compute 
## Line broadening function
#gfunc=g(dk,kT,LAM,lam,var,wk,t)

## Linear component
#fS1 = 0
#S1 = 0
#wegs=1e7/np.array([650,0])*2*pi*c#458,424
#As=np.array([1,0])
#for i in range(1):
#    weg=wegs[i];A=As[i]
#    j = A*np.exp(-1j * (weg ) * t-gfunc)
#    j = j-np.conj(j)
#    s1 = j
#    S1 = S1 + j
#    fs1 = np.fft.fftshift(np.fft.ifft(s1,norm='ortho')) / pi
#    fs1 = fs1 - fs1[-1]
##    fs1 = A * fs1 / np.max(fs1)
#    fS1 = fS1 + fs1
    
##J = np.exp(-1j * weg*t-gfunc)

## Linear response function (cm^-1/2/pi)
##S1 = 1/hbar * (J-np.conj(J))
## Convert Linear response function to fHZ
##S1 = S1 * hbar
## Fourier transform linear response function ==> Linear line shape function
##fS1 = np.fft.fftshift(np.fft.ifft(S1,norm='ortho')) / pi
#fS1 = fS1 - fS1[-1]
#wln = 1e7 / w[np.where(w==0)[0][0]+1:-1]
#wlnS1 = fS1[np.where(w==0)[0][0]+1:-1]

## Plot
#plt.figure(0)
#from Import_Plot_Abs_Data import Import_Abs_Data
#w,AbsData = Import_Abs_Data()
#plt.plot(w,AbsData,'k-',linewidth=4)
##plt.xlim(2.0e2,6.5e2)#3.5e2
#plt.plot(wln,np.abs(wlnS1)/max(np.abs(wlnS1)),'b--',linewidth=4)
#plt.show()

##plt.figure(1)
##plt.xlim(0,2.5e2)
##plt.plot(t,np.abs(S1)/np.max(np.abs(S1)),'b-',linewidth=4)
##plt.show()


################################################################
#Veg = uc.wavenumber_to_J(10)
#k = 2*pi/hbar *Veg**2/uc.wavenumber_to_J(np.sqrt(2*var))*np.exp(-((-15000+lam/c)*c)**2/2/var)
#kr = k * np.exp(-15000/207)
#print(k,kr)
################################################################

## Testing built in frequency axis tool
#ww=np.fft.fftshift(np.fft.fftfreq(int(nw)))*dw*nw