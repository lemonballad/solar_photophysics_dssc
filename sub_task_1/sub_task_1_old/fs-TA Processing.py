# Import libraries
import matplotlib
import matplotlib.pyplot as mplot
import numpy as np
import Utility_fsTA as fsTA


# Define file path and name to be read
filepath_filename='C:\\Users\\tpcheshire\\Desktop\\TestTA\\log1.dat'
A0 = np.loadtxt(filepath_filename)
filepath_filename='C:\\Users\\tpcheshire\\Desktop\\TestTA\\td1.dat'
Time = np.loadtxt(filepath_filename)
filepath_filename='C:\\Users\\tpcheshire\\Desktop\\TestTA\\wvlnCCS200.dat'
wvln2 = np.loadtxt(filepath_filename)

# ADJUSTABLE PARAMETERS 
a,b = A0.shape
npts = Time.size # npts = # of time points to process
npix = wvln2.size # npix = # of pixels in CCD array
nscans = np.int(a / npix) # nscans = # of scans
islc1 = 490 # islc# = wavelength to take slice through 2D plot
islc2 = 651
islc3 = 876

# Change time values to delay relative to time zero in picoseconds.

pix = np.arange(0, npix)
scan = np.arange(0, nscans)
t = np.arange(0, npts)
delay = Time[t] + 774.9 #   % ***NOT GENERAL***

# ADJUST SIGN OF SPECTRUM
A1 = np.empty_like(A0)
for iscan in scan:
    for ipts in t:
        rows = np.arange(iscan * npix, (iscan + 1) * npix)
        A1[rows,ipts] = -np.sign(A0[1400 + iscan * npix, ipts])*A0[rows,ipts]


# AVERAGE SPECTRUM
A2 = np.empty((npix,npts))
for ipix in pix:
    A2[ipix,:] = np.sum(A1[np.arange(ipix,a,npix),:],axis = 0)/nscans

# DATA NOW PROCESSED. . . BEGIN PLOTTING

# CONTOUR PLOTS******************************************
mplot.figure(0)
mplot.contourf(delay,wvln2,np.log10(A2**2),25)
mplot.title('2D Plot')
mplot.xlabel('Time (ps)')
mplot.ylabel('Wavelength (nm)')
mplot.colorbar()
mplot.set_cmap('jet')
mplot.show(0)

# FIND PIXEL FROM WAVELENGTH*********************************************
pixel1 = fsTA.find_index(wvln2,islc1)
pixel2 = fsTA.find_index(wvln2,islc2)
pixel3 = fsTA.find_index(wvln2,islc3)

# PLOT SAME SIGNAL VERSES DELAY
mplot.figure(1)
mplot.plot(delay,A2[pixel1,:],delay,A2[pixel2,:],delay,A2[pixel3,:])
mplot.legend(('Wavelength 1','Wavelength 2','Wavelength 3'))
mplot.title('PLOT SAME SIGNAL VERSES DELAY')
mplot.xlabel('Delay (ps)')
mplot.ylabel('Absolute Value Signal (nm)')
mplot.xlim(-2,5)
mplot.show(1)

# FIND TIME POINT FROM DELAY**************************************** 
tpt1=1
tpt2=250
tpt3=750
tpt4=5
tpt5=10
tpt6=30
tpt7=50
tpt8=100
tpt9=500
twr1 = fsTA.find_index(delay,tpt1)
twr2 = fsTA.find_index(delay,tpt2)
twr3 = fsTA.find_index(delay,tpt3)
twr4 = fsTA.find_index(delay,tpt4)
twr5 = fsTA.find_index(delay,tpt5)
twr6 = fsTA.find_index(delay,tpt6)
twr7 = fsTA.find_index(delay,tpt7)
twr8 = fsTA.find_index(delay,tpt8)
twr9 = fsTA.find_index(delay,tpt9)

# PLOT VERSES WAVELENGTH
mplot.figure(2)
mplot.plot(wvln2,A2[:,twr1],wvln2,A2[:,twr2],wvln2,A2[:,twr3])
mplot.legend(('Time 1','Time 2','Time 3'))
mplot.title('PLOT VERSES WAVELENGTH')
mplot.xlabel('Wavelength (nm)')
mplot.ylabel('Absolute Value Signal (nm)')
mplot.show(2)

#% WRITE FILES***************************************************
#% fid=fopen(['real_660nm_tetracene_70deg_296K.dat'], 'w' );
#% for n=1:npts
#%     fprintf(3, '%2f %12.8f \n',delay(n),imag(A1(pixel1,n)) );
#% end
#% fclose(3) ;
