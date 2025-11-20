# Import libraries and classes
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from tkinter import messagebox


# Function definitions

#def fit_frequency_domain(wvln, delay, signal):
#    """Fit each the frequency domain of the siganl at each delay.
#    parameters  :   amplitude, center, std...return values in wavenumbers
#    covar       :   covariance matrix"""

#    # Function definitions
#    def gauss_fit(x,*parameters):
#        """Sum of gaussians fitting model
#        """

#        # Set parameters
#        A1, mu1, sig1, A2, mu2, sig2, A3, mu3, sig3, C = parameters
#        # Define model
#        gaussian = A1 * np.exp(-(x - mu1)**2/(2 * sig1**2)) \
#        + A2 * np.exp(-(x - mu2)**2/(2 * sig2**2)) + A3 * np.exp(-(x - mu3)**2/(2 * sig3**2)) + C
#        return gaussian
#    # End of function: gauss_fit


#    # Convert wavelength axis to (linear) wavenumber axis
#    wvn = 1e7 / wvln
#    # Set bounds and initial guess of paramters;
#    # this should not be hardcoded.
#    bounds = ((-300, 1e7/465, 100, 0, 1e7/610, 100, 0, 1e7/680, 100, -np.inf),
#              (0, 1e7/455, 1000, 40, 1e7/590, 2000, 40, 1e7/670, 4000, np.inf))
#    guess = (-300, 1e7 / 461, 600, 1, 1e7 / 608, 600, 1, 1e7 / 675, 1600, 0)

#    # Loop over delay points in signal
#    covar = np.zeros((len(guess), len(guess), delay.size))
#    index_delays = np.arange(0, delay.size)
#    parameters = np.zeros((len(guess), delay.size))
#    for idelay in index_delays:
#        if np.sum(~np.isfinite(signal[:,idelay])) == 0:
#            parameters[:,idelay], covar[:,:,idelay] = curve_fit(
#                                                    gauss_fit, wvn, 
#                                                    signal[:, idelay], 
#                                                    p0 = guess, bounds = bounds, maxfev = 1000)

#    return parameters, covar
## End function: fit_frequency_domain
def fit_frequency_domain(wvln, delay, signal):
    """Fit each the frequency domain of the siganl at each delay.
    parameters  :   amplitude, center, std...return values in wavenumbers
    covar       :   covariance matrix"""

    # Function definitions
    def gauss_fit(x,*parameters):
        """Sum of gaussians fitting model
        """

        # Set parameters
        A1, mu1, sig1, A2, mu2, sig2, A3, mu3, sig3, C = parameters
        # Define model
        gaussian = A1 * np.exp(-(x - mu1)**2/(2 * sig1**2)) \
        + A2 * np.exp(-(x - mu2)**2/(2 * sig2**2)) + A3 * np.exp(-(x - mu3)**2/(2 * sig3**2)) + C
        return gaussian
    # End of function: gauss_fit


    # Convert wavelength axis to (linear) wavenumber axis
    wvn = 1e7 / wvln
    # Set bounds and initial guess of paramters;
    # this should not be hardcoded.
    bounds = ((-300, 1e7/465, 100, 0, 1e7/610, 100, 0, 1e7/680, 100, -np.inf),
              (0, 1e7/455, 1000, 40, 1e7/590, 2000, 40, 1e7/670, 4000, np.inf))
    guess = (-300, 1e7 / 461, 600, 1, 1e7 / 608, 600, 1, 1e7 / 675, 1600, 0)

    # Loop over delay points in signal
    covar = np.zeros((len(guess), len(guess), delay.size))
    index_delays = np.arange(0, delay.size)
    parameters = np.zeros((len(guess), delay.size))
    X = np.zeros((delay.size,signal[:,0].size + 1))
    for idelay in index_delays:
        if np.sum(~np.isfinite(signal[:,idelay])) == 0:
            parameters[:,idelay], covar[:,:,idelay] = curve_fit(
                                                    gauss_fit, wvn, 
                                                    signal[:, idelay], 
                                                    p0 = guess, bounds = bounds, maxfev = 1000)
        X[idelay,:] = np.append(signal[:,idelay],delay[idelay])
    y = parameters.T
    X[np.isnan(X)] = 0

    from sklearn.multioutput import MultiOutputRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)  

    regr_multi = MultiOutputRegressor(KNeighborsRegressor(n_neighbors=5))  
    regr_multi.fit(X_train, y_train)  

    y_multi = regr_multi.predict(X)
    import matplotlib.pyplot as mplot
    mplot.figure("knnA")
    mplot.plot(np.log10(delay),y_multi[:,0],"b-",np.log10(delay),
               y_multi[:,3],"r-",np.log10(delay),y_multi[:,6],"k-")
    mplot.pause(0.0001)
    mplot.figure("knnC")
    mplot.plot(np.log10(delay),y_multi[:,1],"b-",np.log10(delay),
               y_multi[:,4],"r-",np.log10(delay),y_multi[:,7],"k-")
    mplot.pause(0.0001)
    mplot.figure("knnV")
    mplot.plot(np.log10(delay),y_multi[:,2],"b-",np.log10(delay),
               y_multi[:,5],"r-",np.log10(delay),y_multi[:,8],"k-")
    mplot.pause(0.0001)
    return parameters, covar
# End function: fit_frequency_domain


def load_TA(wvln_path, delay_path, abs_path, chirp_flag):
    """Load wavelength axis, delay axis, and transient absorption matrix from given files and
    corrects direction of axis to be ascending

    wvln_axis, time_axis, ta = load_TA(wvln_path, delay_path, abs_path, chirp_flag)
    
wvln_path:      path for wavelength file
delay_path:     path for delay time file
abs_path:       path for TA data file
chirp_flag:     Boolean signaling whether data is from the chirp"""


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
# End function: Load_TA


def raw_ta_processing_messages(case, error_flag, parent):
    """Function to return messages used in application
    case        :   message number
    error_flag  :   boolean for if the message is an error"""

    if error_flag is False:
        switch = {
            0       : "We are going to be processing your raw transient absorption data.\n"
                    + "So we are going to need some information from you.\n\nAre you ready? "
                    + "Let's begin...",
            0.1     : "Just to make life easier, let's choose a directory as a starting point. "
                    + "That way you don't need to browse TOO much during our work.",
            1       : "In order to correct the 'chirp' we are going to need a parameters file."
                    + "\n\nDoes a parameters file already exist for the data you want to "
                    + "process? If you don't know, it doesn't hurt to make another one.",
            1.1     : "Great, let's find the parameters file!",
            1.11    : "I'm going to do some thinking....",
            1.2     : "Not a problem. I will walk you through the steps needed to generate a "
                    + "parameters file. We will need the delay, wavelength, and TA files for "
                    + "the blank; this is often, but not always, a water blank",
            1.201   : "We need to gather the following files:",
            1.21    : "I'm going to do some thinking....",
            1.22    : "We should save the parameters file that we generate.",
            1.3     : "OK! We have a parameters file for the chirp; a.k.a. we are ready to go."
                    + "\n\nLET'S DO THIS THING!"
                    }
        if case in switch:
            return switch[case]
        else:
            error_msg = "There is no message associated with" + str(case)
            parent.destroy()
    if error_flag is True:
        switch = {
            0       : "Something really really wrong happened here today.",
            1       : "N",
            2       : "This is not a parameters file. I don't know WHAT it is."
                    }
        if case in switch:
            return switch[case]
# End function: raw_ta_processing_messages


def subtract_baseline(signal, it0):
    """Remove the baseline of the signal by subtracting the average of the negative delay signal
   it0     :   timezero
   signal  :   The TA data
    """

    itimes = np.arange(2,it0)
    baseline = np.median(signal[:, itimes], axis = 1)
    signal = (signal.T - baseline).T
    return signal
# End function: subtract_baseline