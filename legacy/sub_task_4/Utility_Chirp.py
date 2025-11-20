"""
chirp_fitter
find
find_index
find_trust_bounds
load_TA
scorrect"""

def chirp_fitter(desired_npts, file_time, file_wvln, file_Abs_0, path, plot_flag):
    """This function reads in chirp data and creates the parameters need for chirp correction 
    of TA data

    pm = chirp_fitter(desired_npts, file_time, file_wvln, file_Abs_0, path, plot_flag)
       
    desired_npts:    Number of consecutive points to be reliable
    file_time:        contains the time axis of recorded chirp. Stage position file
    file_wvln:        contains the wavelength axis of recorded chirp. Spectrometer wavelength file
    file_Abs_0:       contains the absorption data of recorded chirp. Average scan file
    path:             full path of file location
    plot_flag:        flag for if the numerical chirp and analytic chirp should be plotted"""

    # Import libraries
    import matplotlib.pyplot as mplot
    import numpy as np
    from Utility_Chirp import find_trust_bounds, load_TA

    # Read in data
    wvln_axis, time_axis, Abs_0 = load_TA(path + file_wvln,
                                          path + file_time,
                                          path + file_Abs_0, True)

    # Correct for NaNs and infs
    Abs_0[np.isnan(Abs_0)] = 0  # Sets NaNs to 0
    time_mat, wvln_mat = np.meshgrid(time_axis,wvln_axis)  # Make matrices of time and wavelengths

    # NEED TO  MAKE CODE TO CORRECT FOR INF IN NEXT ITERATION!!!!!!!

    # Calculate <t>
    e_t = np.trapz(time_mat * Abs_0**2, x = time_axis, axis = 1) \
        / np.trapz(Abs_0**2, x = time_axis, axis = 1)

    # Find reliable bounds for data fitting
    index_first, index_last = find_trust_bounds(e_t, desired_npts)

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
        mplot.xlabel('\lambda (nm)')
        mplot.ylabel('Chirp')
        mplot.show("Chirp")

        # Contour of TA signal
        mplot.figure("Chirp TA")
        mplot.contourf(time_axis-zpt, wvln_axis, Abs_0, 20)
        mplot.colorbar()
        mplot.jet()
        mplot.xlabel(r'$\tau$ (ps)')
        mplot.ylabel(r'$\lambda$ (nm)')
        mplot.show("Chirp TA")
    # End if for: plotting chirp

    return pm
    # end % End function: Determin_Chirp_Parameters


# Utility functions for Determine_Chirp_Parameters

def find(condition, nmax, flag_first_last):
    """Find the nmax indices where condition is met starting from begining or end of array
       
    condition:       1D array of booleans
    flag_first_last: Search from begining or end of array
    nmax:            Max number of indices to return"""

    # Import libraries
    import numpy as np

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
    # End function find


def find_index(array,query):
    """Find the index of an array

    index = find_index(array,query):
        
    array       :The data set to be searched
    query       :The value being sought
        
        """
    
    # Import any needed libraries
    import numpy as np

    index = (np.abs(array - query)).argmin()
    return index
    # End function find_index


def find_trust_bounds(raw_data, desired_npts):
    """This function takes an 1D array of data and finds bottom and top limits
    for a region of the data that can be reliably fit.

    index_first, index_last = find_trust_bounds(raw_data, desired_npts)
    
    desired_npts:    Number of consecutive points to be reliable
    raw_data:        1D array of data"""

    # Import libraries
    import numpy as np
    from Utility_Chirp import find

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


def load_TA(wvln_path, delay_path, abs_path, chirp_flag):
    """Load wavelength axis, delay axis, and transient absorption matrix from given files and
    corrects direction of axis to be ascending

    wvln_axis, time_axis, ta = load_TA(wvln_path, delay_path, abs_path, chirp_flag)
    
wvln_path:      path for wavelength file
delay_path:     path for delay time file
abs_path:       path for TA data file
chirp_flag:     Boolean signaling whether data is from the chirp"""

    # Import libraries
    import numpy as np

    # Read in data
    time_axis = np.loadtxt(delay_path)      # Array of time data
    wvln_axis = np.loadtxt(wvln_path)       # Array of wavelength data
    ta = np.loadtxt(abs_path)               # 2d matrix of absorption data
    # NEED TO CREATE ERROR IF FILES CAN NOT BE READ

    # Check dimensions
    # Change stage values to delay in ps
    dim1, dim2 = ta.shape
    nt, = time_axis.shape
    npix, = wvln_axis.shape

    # Ensure dimensions are the same for the ta matrix and the axes
    if dim1 == nt:
        ta = ta.T
    # NEED TO CREATE ERROR IF DIMENSIONS TO MATCH AT ALL

    # First derivative of axes to determine slope of ordering
    d_time = np.diff(time_axis)
    d_wvln = np.diff(wvln_axis)
    # FOR THE FUTURE, A CHECK TO SEE IF AXES ARE LINEAR
    d2_time = np.diff(d_time)
    d2_wvln = np.diff(d_wvln)
    # Create boolean flags if axes are sorted in ascending order
    flag_time_plus = np.sum(d_time >= 0) / (nt - 1) == 1
    flag_wvln_plus = np.sum(d_time >= 0) / (nt - 1) == 1
    # Create boolean flags if axes are sorted in descending order
    flag_time_minus = np.sum(d_time <= 0) / (nt - 1) == 1
    flag_wvln_minus = np.sum(d_time <= 0) / (nt - 1) == 1

    # Reorder axis and ta time dimension, if in descending order or not sorted
    if flag_time_minus and ~flag_time_plus:
        time_axis = np.flip(time_axis)
        ta = np.fliplr(ta)
    elif ~flag_time_minus and flag_time_plus:
        1 # Nothing needs to happen if axis in ascending order
    elif flag_time_minus and flag_time_plus:
        1 # PROBABLY NEED AN ERROR IF ALL VALUES ARE EQUAL
    else:
        indices = np.argsort(time_axis)
        time_axis = time_axis[indices]
        ta = ta[:,indices]

    # Reorder axis and ta wavelength dimension, if in descending order or not sorted
    if flag_wvln_minus and ~flag_wvln_plus:
        wvln_axis = np.flip(wvln_axis)
        ta = np.flipud(ta)
    elif ~flag_wvln_minus and flag_wvln_plus:
        1 # Nothing needs to happen if axis in ascending order
    elif flag_wvln_minus and flag_wvln_plus:
        1 # PROBABLY NEED AN ERROR IF ALL VALUES ARE EQUAL
    else:
        indices = np.argsort(wvln_axis)
        wvln_axis = wvln_axis[indices]
        ta = ta[indices,:]

    if chirp_flag:
        return wvln_axis, time_axis, ta
    else:
        return wvln_axis, time_axis, ta, npix, nt
    # End function Load_TA


def scorrect(s,wvln_axis,time_axis,pm):
    """ Here's the gist, takes a square data with 1 time axis and turns it into a
parallelogramish thing with 0s where extraped data would be.
Input avg signal, wavelength and delay axes, 2nd order chirp parameters
Outputs a new log delay axis and chirp corrected signal"""

    # Import libraries
    import numpy as np
    from scipy.interpolate import griddata
    # Analytic chirp function
    t_0 = pm[0] * wvln_axis**2 + pm[1] * wvln_axis + pm[2] # form a*x^2+b*x+c = t_0
    time_shift = np.max(t_0) - np.min(t_0) # The maximum shift of an axis along a pixel
    t_low = np.min(time_axis) - time_shift # Extends lower limit for later chopping purposes. Negative value
    t_high = np.max(time_axis) + time_shift # Extends upper limit for later chopping purposes. Positive value

    nt, = time_axis.shape # Number of points on the original time axis
    nw, = wvln_axis.shape # Number of points on the original time axis
    rt = np.arange(0, nt) # Time index range
    dt = (t_high - t_low) / nt # dt...used for linear axis not log axis
    new_time_axis = np.arange(start = t_low, stop = t_high, step = dt) # The time axis being interpolated onto

    t_0_mat = np.tile(t_0[np.newaxis].T,(1,nt)) # Create matrix of duplicate t_0 arrays (wvln X time)
    time_axis_mat = np.tile(time_axis[np.newaxis],(nw,1)) # Create matrix of duplicate time arrays (wvln X time)
    delay_mat = time_axis_mat-t_0_mat # Calculate unique delay axis for each pixel (wvln X time)
    new_time_axis_mat = np.tile(new_time_axis[np.newaxis],(nw,1)) # Time matrix being interpolated onto (wvln X time)
    wvln_mat = np.tile(wvln_axis[np.newaxis].T,(1,nt)) # Create matrix of duplicate time arrays (wvln X time)

    s[~np.isfinite(s)] = np.NaN # Set infs to NaN
    good_indices = ~np.isnan(s) # Find indices that are finite

    # Fill in holes and chirp correction
    s = griddata((delay_mat[good_indices], wvln_mat[good_indices]),
                  s[good_indices], (new_time_axis_mat, wvln_mat));

    return new_time_axis, s
    # End function: scorrect


