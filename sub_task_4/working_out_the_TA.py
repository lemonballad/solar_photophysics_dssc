
import tkinter as tk
from tkinter import filedialog,messagebox
import numpy as np
from tc_windows.get_ta_files import get_ta_files
import matplotlib.pyplot as mplot
from scipy.signal import savgol_filter
from utilities_chirp import find_index,scorrect
from utilities_raw_ta_processing import subtract_baseline, fit_frequency_domain

initial_directory = "C:\\Users\\tpcheshire\\Documents\\Project_Dye Kinetics\\Moran Data\\" \
    + "Fitted Data for ALL SAMPLES\\2\\In Solution\\Ru(bpy) Complex 2\\" \
    + "Long Scan_Magic Angle_1.5uJ (10-4-11)"#5
#    + "Short Scan_Magic Angle_1.5uJ (10-2-11)"
#    + "Short Scan_Magic Angle_1.5uJ (9-30-11)"#30

root = tk.Tk()
root.initial_directory = initial_directory

#ta_files = get_ta_files(root,"Get TA files")
root.iconify()

delay_file = initial_directory + "\\td1.dat"
wvln_file = initial_directory + "\\wvlnCCS200.dat"
ta_file = initial_directory + "\\log1.dat"

delay = np.loadtxt(delay_file)#;delay=delay[0:75]
wvln = np.loadtxt(wvln_file)
ta = np.loadtxt(ta_file)

p = np.loadtxt("C:\\Users\\tpcheshire\\Documents\\Project_Dye Kinetics\\Cheshire Data\\"
               + "Moran fsTA\\Chirp Fits Solution\\chirp_parameters2 11-15-18.dat")
p = np.poly1d(p)
chirp = p(wvln)


nt, = delay.shape # number of time points
nw, = wvln.shape # number of wavelengths
d1,d2 = ta.shape # shape of ta data

ns = int(d1/nw) # number of scans
index_scan = np.arange(0, ns) # Range of scans
index_time = np.arange(0, nt) # Time points indices
index_wvln = np.arange(0, nw) # Pixel points indices

# Deal with NaNs and infs
ta[~np.isfinite(ta)] = 0
# Correct baseline
#ta = subtract_baseline(ta, 1)

# Adjust sign of spectrum
iwvln = find_index(wvln,490)#1400 is the index of 493
ibleaches0 = np.arange(find_index(wvln,490),find_index(wvln,500))
A2 = np.zeros(ta.shape)
for iscan in index_scan: # loop over pixels
    ibleach = iwvln + iscan * nw
    ibleaches = ibleaches0 + iscan * nw
    indices = np.arange(iscan * nw, (iscan + 1) * nw)
    # ADJUST SIGN relative to pump scatter. 1000 converts units to mOD
    A2[indices, :] = -10**3 * np.sign(ta[ibleach, :]) * ta[indices, :]
#    A2[indices, :] = -10**3 * np.sign(np.mean(np.sign(ta[ibleaches, :]),axis = 0)) * ta[indices, :]
# End loop over pixels

# AVERAGE SPECTRUM
A3 = np.zeros((nw,nt))
for iw in np.arange(0, nw):
    A3[iw,:] = np.sum(A2[np.arange(iw,d1,nw),:],axis = 0)/ns
# End loop over wavelengths

# Correct for chirp in probe
iwvlns = np.arange(find_index(wvln,440),find_index(wvln,690))
#iwvlns = np.append(iwvlns,np.arange(find_index(wvln,775),find_index(wvln,880)))
wvln = wvln[iwvlns]
chirp = chirp[iwvlns]
A4 = A3[iwvlns,:]
delay, ta = scorrect(A4, wvln, delay, chirp)
A4=ta
#ta=A4
# Correct baseline
A4 = subtract_baseline(A4, 8)
print(A4[find_index(wvln,490),0:10])
print(delay[0:10])
# Plot results
mplot.figure("Chirp")
mplot.contourf(delay, wvln, savgol_filter(savgol_filter(A4,11,3,axis = 0),3,2), 20)
mplot.colorbar()
mplot.jet()
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\lambda$ (nm)')
mplot.pause(0.001)

mplot.figure("time")
color = np.array([[0,0,1],[0,1,0],[1,0,0]])
windex = np.array([find_index(wvln,470),find_index(wvln,490),find_index(wvln,510),
                   find_index(wvln,600),find_index(wvln,610),find_index(wvln,620),
                   find_index(wvln,670),find_index(wvln,680),find_index(wvln,690)])
c=-1
for ii in windex:
    c+=1
    mplot.plot(np.log10(delay),savgol_filter(A4[ii,:],5,3), color = tuple(color[c//3,:]*(c%3+1)/4))
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('mOD')
mplot.pause(0.001)

mplot.figure("freq")
#color = np.array([0.1,0.3,0.5,0.7,0.9])
c1 = np.array([0,0,1,0])
c2 = np.array([0,1,0,0])
c3 = np.array([0,0,0,1])
tindex = np.array([find_index(delay,0.2+0.5),find_index(delay,1+0.5),
                   find_index(delay,5+0.5),find_index(delay,100+0.5)])
c=-1
for ii in tindex:
    c+=1
#    mplot.plot(1e7/wvln,savgol_filter(A4[:,ii],55,3), color = (color[c],0,0))
    mplot.plot(1e7/wvln,savgol_filter(A4[:,ii],17,3), color = (c1[c],c2[c],c3[c]))
mplot.plot([15500,24500],[0,0],"k-", linewidth = 1)
mplot.xlabel(r'$\lambda$ (nm)')
mplot.ylabel('mOD')
mplot.xlim(15500,24500)
mplot.ylim(-300,15)
mplot.pause(0.001)

c=-1
for ii in tindex:
    c+=1
#    mplot.plot(1e7/wvln,savgol_filter(A4[:,ii],55,3), color = (color[c],0,0))
    mplot.plot(wvln,savgol_filter(A4[:,ii],17,3), color = (c1[c],c2[c],c3[c]))
mplot.plot([490,690],[0,0],"k-", linewidth = 1)
mplot.xlabel(r'$\lambda$ (nm)')
mplot.ylabel('mOD')
mplot.xlim(440,690)
mplot.ylim(-300,15)
mplot.pause(0.001)

#save_location = filedialog.asksaveasfilename(parent = root, title = "Save Parameters")
#print(save_location)
#np.savetxt(save_location,avg_t_coeffs)

parameters, covar = fit_frequency_domain(wvln, delay, 
                                         savgol_filter(savgol_filter(A4,5,3,axis=0),7,2))
mplot.figure("Fit GSB")
mplot.subplot(1,3,1)
mplot.plot(delay, parameters[0,:], 'b-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('mOD')
mplot.subplot(1,3,2)
mplot.plot(delay, 1e7/parameters[1,:], 'b-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'Center (cm$^{-1}$)')
mplot.subplot(1,3,3)
mplot.plot(delay, parameters[2,:], 'b-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('STD')
mplot.pause(0.001)

mplot.figure("Fit ESE")
mplot.subplot(1,3,1)
mplot.plot(delay, parameters[3,:], 'r-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('mOD')
mplot.subplot(1,3,2)
mplot.plot(delay, 1e7/parameters[4,:], 'r-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'Center (cm$^{-1}$)')
mplot.subplot(1,3,3)
mplot.plot(delay, parameters[5,:], 'r-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('STD')
mplot.pause(0.001)

mplot.figure("Fit ESE2")
mplot.subplot(1,3,1)
mplot.plot(delay, parameters[6,:], 'k-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('mOD')
mplot.subplot(1,3,2)
mplot.plot(delay, 1e7/parameters[7,:], 'k-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'Center (cm$^{-1}$)')
mplot.subplot(1,3,3)
mplot.plot(delay, parameters[8,:], 'k-')
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('STD')
mplot.pause(0.001)

A5 =np.zeros(A4.shape)
p1=np.mean(parameters[1,:])
p4=np.mean(parameters[4,:])
p7=np.mean(parameters[7,:])
p2=np.mean(parameters[2,:])
p5=np.mean(parameters[5,:])
p8=np.mean(parameters[8,:])
for idelay in np.arange(0,delay.size):
    A5[:,idelay] = \
        parameters[0,idelay]*np.exp(-(1e7/wvln-parameters[1,idelay])**2/(2*p2**2))\
        + parameters[3,idelay]*np.exp(-(1e7/wvln-parameters[4,idelay])**2/(2*p5**2))\
        + parameters[6,idelay]*np.exp(-(1e7/wvln-parameters[7,idelay])**2/(2*p8**2))\
        + parameters[9,idelay]
mplot.figure("2dfit")
mplot.contourf(delay, wvln, (A5), 20)
mplot.colorbar()
mplot.jet()
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\lambda$ (nm)')
mplot.pause(0.001)


root.mainloop()