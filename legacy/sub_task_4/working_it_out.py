import matplotlib.pyplot as mplot
import numpy as np
from scipy.signal import savgol_filter
from tc_windows.get_ta_files import get_ta_files
import tkinter as tk
from tkinter import filedialog,messagebox
from utilities_chirp import find_index
from utilities_raw_ta_processing import subtract_baseline

initial_directory = "C:\\Users\\tpcheshire\\Documents\\Project_Dye Kinetics\\Moran Data\\Fitted Data for ALL SAMPLES\\OKE of visible TA setup"
root = tk.Tk()
#root.initial_directory = initial_directory

#ta_files = get_ta_files(root,"Get TA files")
root.iconify()

#delay = np.loadtxt(ta_files.delay[0])
#wvln = np.loadtxt(ta_files.wvln[0])
#ta = np.loadtxt(ta_files.ta[0])

delay_file = initial_directory + "\\tdFinal2.dat"
wvln_file = initial_directory + "\\wvlnCCS200.dat"
ta_file = initial_directory + "\\logFinal2.dat"

delay = np.loadtxt(delay_file)
wvln = np.loadtxt(wvln_file)
ta = np.loadtxt(ta_file)
nt, = delay.shape
nw, = wvln.shape
d1,d2 = ta.shape
ns = int(d1/nw)
index_scan = np.arange(0,ns)

# Deal with NaNs and infs
ta[~np.isfinite(ta)] = 0
# Correct baseline
ta = subtract_baseline(ta, 5)

# Adjust sign of spectrum
iwvln = find_index(wvln,500)#1400 is the index of 493
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
ta = A2

# AVERAGE SPECTRUM
#ta = np.abs(ta)
ta = savgol_filter(np.abs(ta),3,1,axis = 1)
A2 = np.zeros((nw,nt))
for iw in np.arange(0, nw):
    A2[iw,:] = np.sum(ta[np.arange(iw,d1,nw),:],axis = 0)/ns
ta = A2

good_indices = np.arange(find_index(wvln,470),find_index(wvln,900))#500 540
#good_indices = np.append(good_indices, np.arange(find_index(wvln,600),find_index(wvln,705)))
#good_indices = np.append(good_indices, np.arange(find_index(wvln,790),find_index(wvln,950)))
ta=ta[good_indices,:]
wvln_filtered = wvln[good_indices]

avg_t = np.trapz(ta*delay,x = delay, axis = 1)/np.trapz(ta,x = delay, axis = 1)

avg_t_coeffs = np.polyfit(wvln_filtered, avg_t,100)
poly_avg_t = np.poly1d(avg_t_coeffs)
pavg_t = poly_avg_t(wvln)

mplot.figure("avg_t")
mplot.plot(wvln_filtered,avg_t,'b-',wvln,pavg_t,'r-')
mplot.ylim(-776,-774)
mplot.xlabel('\lambda (nm)')
mplot.pause(0.01)

mplot.figure("Chirp")
mplot.contourf(delay, wvln_filtered, ta, 20)
mplot.colorbar()
mplot.jet()
mplot.xlabel('\lambda (nm)')
mplot.ylabel('Chirp')
mplot.pause(0.001)

save_location = filedialog.asksaveasfilename(parent = root, title = "Save Parameters")
print(save_location)
np.savetxt(save_location,avg_t_coeffs)

root.mainloop()