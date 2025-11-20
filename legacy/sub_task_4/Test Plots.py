import tkinter as tk
from tkinter import filedialog,messagebox
import numpy as np
from tc_windows.get_ta_files import get_ta_files
import matplotlib.pyplot as mplot
from scipy.signal import savgol_filter
from utilities_chirp import find_index,scorrect
from utilities_raw_ta_processing import subtract_baseline, fit_frequency_domain

initial_directory = "C:\\Users\\tpcheshire\\Documents\\Project_Dye Kinetics\\Moran Data\\" \
    + "Fitted Data for ALL SAMPLES\\1\\In Solution\\Ru(bpy) Complex 1\\Chirp Corrected"

root = tk.Tk()
root.initial_directory = initial_directory

ta_files = get_ta_files(root,"Get TA files")
root.iconify()

delay_file = ta_files.delay[0]#"initial_directory + \\td1.dat"
wvln_file = ta_files.wvln[0]#initial_directory + "\\wvlnCCS200.dat"
ta_file = ta_files.ta[0]#initial_directory + "\\log1.dat"

delay = np.loadtxt(delay_file, delimiter = ",")
wvln = np.loadtxt(wvln_file)
ta = np.loadtxt(ta_file, delimiter = "\t")




nt, = delay.shape;nw, = wvln.shape;d1,d2 = ta.shape

ns = int(d1/nw);index_time = np.arange(0, nt);index_wvln = np.arange(0, nw) # Pixel points indices

# Deal with NaNs and infs
ta[~np.isfinite(ta)] = 0;ta = subtract_baseline(ta, 17)

# Adjust sign of spectrum
A2 = np.zeros(ta.shape)
for iw in index_wvln: # loop over pixels
    A2[iw, :] = -10**3 * np.sign(ta[1386, :]) * ta[iw, :]
# End loop over pixels

# AVERAGE SPECTRUM
A3 = np.zeros((nw,nt))
for iw in np.arange(0, nw):
    A3[iw,:] = np.sum(A2[np.arange(iw,d1,nw),:],axis = 0)/ns
ta=A3

delay=delay-delay[0]

ta[ta<-7.5]=0
good_indices = np.arange(find_index(wvln,490),find_index(wvln,700))
#good_indices = np.append(good_indices,np.arange(find_index(wvln,870),find_index(wvln,885)))
mplot.figure("Chirp")
mplot.contourf(delay, wvln[good_indices],
              (ta[good_indices,:]), 20)
mplot.colorbar()
mplot.jet()
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\lambda$ (nm)')
mplot.pause(0.001)


parameters, covar = fit_frequency_domain(wvln[good_indices], delay[:], ta[good_indices,:])
#mplot.figure("Fit GSB")
#mplot.subplot(1,3,1)
#mplot.plot(delay, parameters[0,:], 'b-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel('mOD')
#mplot.subplot(1,3,2)
#mplot.plot(delay, 1e7/parameters[1,:], 'b-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel(r'Center (cm$^{-1}$)')
#mplot.subplot(1,3,3)
#mplot.plot(delay, parameters[2,:], 'b-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel('STD')
#mplot.pause(0.001)

#mplot.figure("Fit ESE")
#mplot.subplot(1,3,1)
#mplot.plot(delay, parameters[3,:], 'r-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel('mOD')
#mplot.subplot(1,3,2)
#mplot.plot(delay, 1e7/parameters[4,:], 'r-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel(r'Center (cm$^{-1}$)')
#mplot.subplot(1,3,3)
#mplot.plot(delay, parameters[5,:], 'r-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel('STD')
#mplot.pause(0.001)

#mplot.figure("Fit ESE2")
#mplot.subplot(1,3,1)
#mplot.plot(delay, parameters[6,:], 'k-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel('mOD')
#mplot.subplot(1,3,2)
#mplot.plot(delay, 1e7/parameters[7,:], 'k-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel(r'Center (cm$^{-1}$)')
#mplot.subplot(1,3,3)
#mplot.plot(delay, parameters[8,:], 'k-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel('STD')
#mplot.pause(0.001)

#A5 =np.zeros(ta.shape)
#p1=np.mean(parameters[1,:])
#p4=np.mean(parameters[4,:])
#p7=np.mean(parameters[7,:])
#p2=np.mean(parameters[2,:])
#p5=np.mean(parameters[5,:])
#p8=np.mean(parameters[8,:])
#for idelay in np.arange(0,delay.size):
#    A5[:,idelay] = \
#        parameters[0,idelay]*np.exp(-(1e7/wvln-parameters[1,idelay])**2/(2*p2**2))\
#        +parameters[3,idelay]*np.exp(-(1e7/wvln-parameters[4,idelay])**2/(2*p5**2))\
#        +parameters[6,idelay]*np.exp(-(1e7/wvln-parameters[7,idelay])**2/(2*p8**2))
#mplot.figure("2dfit")
#mplot.contourf(delay, wvln, (A5), 20)
#mplot.colorbar()
#mplot.jet()
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel(r'$\lambda$ (nm)')
#mplot.pause(0.001)


mplot.figure("time")
color = np.array([[0,0,1],[0,1,0],[1,0,0]])
windex = np.array([find_index(wvln,470),find_index(wvln,490),find_index(wvln,510),
                   find_index(wvln,600),find_index(wvln,610),find_index(wvln,620),
                   find_index(wvln,670),find_index(wvln,680),find_index(wvln,690)])
c=-1
for ii in windex:
    c+=1
    mplot.plot(np.log10(delay),savgol_filter(ta[ii,:],5,3), color = tuple(color[c//3,:]*(c%3+1)/4))
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel('mOD')
mplot.pause(0.001)

mplot.figure("freq")
color = np.array([0.1,0.3,0.5,0.7,0.9])
tindex = np.array([find_index(delay,0.2+157),find_index(delay,1+157),
                   find_index(delay,5+157),find_index(delay,100+157)])
c=-1
for ii in tindex:
    c+=1
    mplot.plot(wvln[good_indices],savgol_filter(ta[good_indices,ii],15,7), color = (color[c],0,0))
mplot.xlabel(r'$\lambda$ (nm)')
mplot.ylabel('mOD')
mplot.pause(0.001)




root.mainloop()
