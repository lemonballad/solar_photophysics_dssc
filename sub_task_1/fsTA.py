# Import libraries
import matplotlib.pyplot as mplot
import numpy as np
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from Utility_Chirp \
    import chirp_fitter,find_index,load_TA,scorrect

# Flags, parameters, and initialization
desired_npts = 500
plot_chirp_flag = True
pump_center = 0
pump_FWHM = 0
pump_indices = np.arange(575,621)

# Delay stage position for time zero
# Corrects for the actual point of t_0 considering the position of the
# stage. Not really necessary if chirp correcting
zpt = 485.4 # Supposedly a number that gets close to t_0

# Wavelengths (nm) to view
# Just plotting stuff. Picks 3 wavelengths to plot decays
wv1 = 450
wv2 = 550
wv3 = 700

# Delay times (ps) to view
# Just plotting stuff. Picks 3 time points to plot spectra
de1 = 0.2
de2 = 1
de3 = 5

# GUI
root = tk.Tk()
root.withdraw()
filez = filedialog.askopenfilenames(parent=root,title='Choose a file')
lst = list(filez)

# Paths and filenames
# Define path and filenames for chirp data
path_chirp = 'C:\\Users\\tpcheshire\\Documents\\TiCat3_TA\\1-29-16\\water_chirp\\'
file_Abs_0 = 'av1.dat'
file_chirp_pm = 'chirpfit.dat'
file_time_chirp = 'td1.dat'
file_wvln_chirp = 'wavelength_recal.dat'

# Define path and filenames for linear TAdata
path = 'C:\\Users\\tpcheshire\\Documents\\TiCat3_TA\\1-29-16\\Ti(Cat)_3\\3ps_linear\\'
file_Abs = 'av1.dat'
file_time = 'td1.dat'
file_wvln = 'wavelength_recal.dat'


# Determine chirp parameters
pm = chirp_fitter(desired_npts, file_time_chirp, file_wvln_chirp, file_Abs_0, 
                  path_chirp, plot_chirp_flag)

# Write chirp parameters to file if file does not already exist
my_file = Path(path_chirp + file_chirp_pm)
if ~my_file.is_file():
    np.savetxt(path_chirp + file_chirp_pm, pm)

# Corrects for the actual point of t_0 considering the position of the
# stage. From chirp correction
zpt = pm[2] - pm[1]**2 / 4 / pm[0] #  Delay stage position for t_0
pm[2] = pm[2] - zpt

# TA data
# Read in data
wvln_axis, time_axis, ta, npix, nt = load_TA(path + file_wvln,
                                      path + file_time,
                                      path + file_Abs_0, False)

# BLOCK OUT PUMP FROM CONTOUR
pump_center_wvln = 391.5
pump_FWHM = 912
pump_low_index = find_index(wvln_axis, 1e7 / (1e7 / pump_center_wvln + pump_FWHM))
pump_high_index = find_index(wvln_axis, 1e7 / (1e7 / pump_center_wvln - pump_FWHM))
pump_indices = np.arange(pump_low_index, pump_high_index)

index_time = np.arange(0, nt) # Time points indices
index_pix = np.arange(0, npix) # Pixel points indices

# Change stage values to delay in ps
time_adjusted = time_axis - zpt # Turns raw time into ~delay linearly

# Adjust sign of spectrum
A2 = np.zeros((npix, nt))
ibleach = np.max(np.argmax(np.abs(ta), axis = 0))
for ipix in index_pix: # loop over pixels
    for itime in index_time: # loop over time
        A2[ipix, itime] = - -10**3 * np.sign(ta[ibleach,itime]) * ta[ipix,itime]
        #ADJUST SIGN relative to pump scatter. 1000 converts units to mOD
    # End loop over time indices
# End loop over pixels

# Correct for chirp in probe
time_out, S = scorrect(A2, wvln_axis, time_adjusted, pm)

# Pixel corresponding to chosen wavelengths
p1 = find_index(wvln_axis,wv1) # Finds pixel according to wavelength
p2 = find_index(wvln_axis,wv2) # Finds pixel according to wavelength
p3 = find_index(wvln_axis,wv3) # Finds pixel according to wavelength

# Time point corresponding to chosen delays
t1 = find_index(time_out,de1) # Finds time point according to requested delay
t2 = find_index(time_out,de2) # Finds time point according to requested delay
t3 = find_index(time_out,de3) # Finds time point according to requested delay

A4 = S
A4[pump_indices,:] = np.NaN
#A4[A4>2.8] = np.NaN
#A4[A4<-2.8] = np.NaN

# Contour of Raw TA signal
mplot.figure("Raw TA")
mplot.contourf(time_adjusted,wvln_axis,A2,20)
mplot.colorbar()
mplot.jet()
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\lambda$ (nm)')
mplot.show("Raw TA")

# Contour of processed TA signal
mplot.figure("TA")
mplot.contourf(np.abs(time_out),wvln_axis,A4,20)
mplot.colorbar()
mplot.jet()
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\lambda$ (nm)')
mplot.show("TA")

#mplot.figure("F[TA]")
#mplot.contourf(time_out,wvln_axis,A4,20)
#mplot.colorbar
#mplot.jet
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel(r'$\lambda$ (nm)')
#mplot.show("F[TA]")
#figure % Contour of TA signal
#fA4=A4(258:554,55:75);
#contourf(time_out(55:75),wvln_axis(258:554),abs(fftshift(fft(fliplr(fA4),[],1),1)),20,'edgecolor','none');ylim([420 600]);xlim([-3 0]);
#colorbar;colormap jet;
#ylabel('Wavelength (nm)');
#xlabel('Wavenumber (cm^{-1})');

#figure; 
#% Plot spectra at requested times
#subplot(2,1,1);plot(wvln_axis,S(:,t1),wvln_axis,S(:,t2),wvln_axis,S(:,t3));
#xlabel('Wavelength (nm)');
#ylabel('\DeltamOD');
#xlim([405,800]);
#% Plot decay at requested wavelengths
#subplot(2,1,2);plot(time_out,S(p1,:),time_out,S(p2,:),time_out,S(p3,:));
#xlabel('Delay (ps)');
#ylabel('\DeltamOD');










root = tk.Tk()
root.withdraw()
filez = filedialog.askopenfilenames(parent=root,title='Choose a file')
lst = list(filez)
