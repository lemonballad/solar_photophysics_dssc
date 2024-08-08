# Import libraries and classes
import matplotlib.pyplot as mplot
from mpl_toolkits import mplot3d
import numpy as np
from utilities_raw_ta_processing import load_TA, raw_ta_processing_messages

def chirp_fitter(desired_npts, file_time, file_wvln, file_Abs_0, plot_flag):
    """This function reads in chirp data and creates the parameters need for chirp correction 
    of TA data

    pm = chirp_fitter(desired_npts, file_time, file_wvln, file_Abs_0, plot_flag)
       
    desired_npts:    Number of consecutive points to be reliable
    file_time:        contains the time axis of recorded chirp. Stage position file
    file_wvln:        contains the wavelength axis of recorded chirp. Spectrometer wavelength file
    file_Abs_0:       contains the absorption data of recorded chirp. Average scan file
    plot_flag:        flag for if the numerical chirp and analytic chirp should be plotted"""

    # Read in data
    wvln_axis, time_axis, Abs_0 = load_TA(file_wvln,file_time,file_Abs_0, True)



    ## ADJUSTABLE PARAMETERS 
    a,b = Abs_0.shape
    npts, = time_axis.shape # npts = # of time points to process
    npix, = wvln_axis.shape # npix = # of pixels in CCD array
    nscans = np.int(a / npix) # nscans = # of scans

    A1 = np.zeros(Abs_0.shape)
    ibleach = np.max(np.argmax(np.abs(Abs_0), axis = 0))
    for ipix in np.arange(0, npix): # loop over pixels
        for itime in np.arange(0, npts): # loop over time
            A1[ipix, itime] = - -10**3 * np.sign(Abs_0[1400,itime]) * Abs_0[ipix,itime]
            #ADJUST SIGN relative to pump scatter. 1000 converts units to mOD
        # End loop over time indices
    # End loop over pixels


    # AVERAGE SPECTRUM
    A2 = np.zeros((npix,npts))
    for ipix in np.arange(0, npix):
        A2[ipix,:] = np.sum(A1[np.arange(ipix,a,npix),:],axis = 0)/nscans
    Abs_0 = A2

    # Correct for NaNs and infs
    Abs_0[np.isnan(Abs_0)] = 0  # Sets NaNs to 0
    Abs_0[np.isinf(Abs_0)] = 0
    time_mat, wvln_mat = np.meshgrid(time_axis,wvln_axis)  # Make matrices of time and wavelengths

    # NEED TO  MAKE CODE TO CORRECT FOR INF IN NEXT ITERATION!!!!!!!

    # Calculate <t>
    e_t = np.trapz(time_mat * Abs_0**2, x = time_axis, axis = 1) \
        / np.trapz(Abs_0**2, x = time_axis, axis = 1)
    from scipy.signal import savgol_filter
    e_t = savgol_filter(e_t, 101, 3) # window size 51, polynomial order 3
    mplot.figure(35)
    mplot.plot(wvln_axis,e_t)
    mplot.pause(0.1)

    # Find reliable bounds for data fitting
    index_first, index_last = find_index(wvln_axis, 460),find_index(wvln_axis,700)#find_trust_bounds(e_t, desired_npts)

    # Calculate parameters for chirp correction
    pm = np.polyfit(wvln_axis[index_first:index_last], e_t[index_first:index_last], 2)

    # If plot_flag is true then plot the numerical and analytic chirp
    if plot_flag:
        # Create analytic chirp data from parameters
        analytic_chirp = pm[0] * wvln_axis**2 + pm[1] * wvln_axis + pm[2]
        zpt = pm[2] - pm[1]**2 / 4 / pm[0] #  Delay stage position for t_0
        # Plot data
        mplot.figure("Chirp")
        mplot.plot(wvln_axis,e_t-zpt)#,
        mplot.plot(wvln_axis,analytic_chirp-zpt)
        mplot.legend(('Numerical','Analytic'))
        mplot.xlabel(r'$\lambda$ (nm)')
        mplot.ylabel('Chirp')
        mplot.pause(0.01)

        # Contour of TA signal
        mplot.figure("Chirp TA")
        mplot.contourf(time_axis-zpt, wvln_axis, Abs_0, 20)
        mplot.colorbar()
        mplot.jet()
        mplot.xlabel(r'$\tau$ (ps)')
        mplot.ylabel(r'$\lambda$ (nm)')
        mplot.pause(0.01)
    # End if for: plotting chirp
    return pm
# End function: chirp_fitter


def find(condition, nmax, flag_first_last):
    """Find the nmax indices where condition is met starting from begining or end of array
       
    condition:       1D array of booleans
    flag_first_last: Search from begining or end of array
    nmax:            Max number of indices to return"""

    indices = np.argwhere(condition)
    nindices = indices.size
    if nmax > nindices: nmax = nindices
    if nmax == 0: return False
    if flag_first_last == True:
        if nmax == 1:
            return indices[0][0]
        else:
            return indices[:nmax]
    else:
        if nmax == 1:
            return indices[-1][0]
        else:
            return indices[-nmax:]
# End function: find


def find_index(array,query):
    """Find the index of an array

    index = find_index(array,query):
        
    array       :The data set to be searched
    query       :The value being sought
        
        """    
    index = (np.abs(array - query)).argmin()
    return index
# End function: find_index


def find_trust_bounds(raw_data, desired_npts):
    """This function takes an 1D array of data and finds bottom and top limits
    for a region of the data that can be reliably fit.

    index_first, index_last = find_trust_bounds(raw_data, desired_npts)
    
    desired_npts:    Number of consecutive points to be reliable
    raw_data:        1D array of data"""

    # Absolute value of the 2nd derivative of the raw data array
    d_raw_data_2 = np.abs(np.diff(raw_data, n = 2))
    # The variance of the 2nd derivative: <|d2(raw_data)/dx2|^2>
    var_d_raw_data_2 = np.var(d_raw_data_2)

    # A counter for the number of consecutive reliable points
    reliable_point_count = 0

    # Loop over derivative points until good mid_search_point is found
    for ii in np.arange(0,d_raw_data_2.size):
        # Is the current point less than the variance of the derivative
        if d_raw_data_2[ii] < var_d_raw_data_2:
            # Is the next point less than the variance of the derivative
            if d_raw_data_2[ii + 1] < var_d_raw_data_2:
                # Yes, add to the count
                reliable_point_count += 1
                # Define the mid_search_point in event the desired number of consecutive points
                # will not be achieved
                mid_search_point = ii - np.int(desired_npts / 2)
            else:
                # No, reset the count
                reliable_point_count = 0
            # End if statement for: is the next point less than the variance of the derivative
        # End if statement for: is the current point less than the variance of the derivative
    
        # Define the mid_search_point if the desired number of consecutive
        # reliable points has been found and BREAK out of the loop
        if reliable_point_count == desired_npts:
            mid_search_point = ii - np.int(desired_npts / 2)
            break # Leave loop
        # End if statement for: finding the desired number of points
    # End loop to find good mid_search_point

    # Define the index for the upper limit of reliable data
    index_first = find(d_raw_data_2[1:mid_search_point]
        > var_d_raw_data_2, 1, False)
    # Define the index for the lower limit of reliable data
    index_last = mid_search_point + find(d_raw_data_2[
        mid_search_point:-1] > var_d_raw_data_2, 1, True)

    return index_first, index_last
# End function: find_trust_bounds

def scorrect(s,wvln_axis,time_axis,chirp):
    """ Here's the gist, takes a square data with 1 time axis and turns it into a
parallelogramish thing with 0s where extraped data would be.
Input avg signal, wavelength and delay axes, 2nd order chirp parameters
Outputs a new log delay axis and chirp corrected signal"""

    # Import libraries
    import numpy as np
    from scipy.interpolate import griddata
    import scipy.interpolate
    # Analytic chirp function
    t_0 = chirp
    # The maximum shift of an axis along a pixel
    time_shift = np.max(t_0) - np.min(t_0) 
    # Extends lower limit for later chopping purposes. Negative value
    t_low = np.min(time_axis) - time_shift 
    # Extends upper limit for later chopping purposes. Positive value
    t_high = np.max(time_axis) + time_shift 

    nt, = time_axis.shape # Number of points on the original time axis
    nw, = wvln_axis.shape # Number of points on the original time axis
    rt = np.arange(0, nt) # Time index range
    dt = (t_high - t_low) / nt # dt...used for linear axis not log axis
    #new_time_axis = np.arange(start = t_low, stop = t_high, step = dt) # The time axis being interpolated onto
    new_time_axis = (dt*nt+1)**(rt / nt) + t_low - np.min(t_0)-1
    # Create matrices from arrays
    time_axis_mat, t_0_mat = np.meshgrid(time_axis,t_0)
    new_time_axis_mat, wvln_mat = np.meshgrid(new_time_axis,wvln_axis)
    delay_mat = time_axis_mat-t_0_mat # Calculate unique delay axis for each pixel (wvln X time)


    # Get good_indices of signal
    good_indices = np.isfinite(s) # Find indices that are finite
    #good_indices = np.ones((nw,nt), dtype = bool)

    print(time_axis[0],np.min(t_0),new_time_axis[0],t_low)
    # Fill in holes and chirp correction
    #s = griddata((delay_mat[good_indices], wvln_mat[good_indices]),
    #              s[good_indices], (new_time_axis_mat, wvln_mat), method = "nearest");
    #s = griddata((new_time_axis_mat[good_indices]-10, wvln_mat[good_indices]),
    #              s[good_indices], (new_time_axis_mat, wvln_mat), method = "cubic");
    for it0 in np.arange(0,nw):
        sinterp = scipy.interpolate.interp1d(time_axis-t_0[it0],s[it0,:],kind = "cubic",
                                             bounds_error=False, fill_value=np.nan)
        s[it0,:] = sinterp(new_time_axis)
    return new_time_axis, s
    # End function: scorrect

