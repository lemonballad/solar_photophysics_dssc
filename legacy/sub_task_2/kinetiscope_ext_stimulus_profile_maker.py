# Import libraries
import datetime
import matplotlib.pyplot as mplot
import numpy as np
import os

# Set today's date
now = datetime.datetime.now()
today = now.strftime("%B") + " " + str(now.day) + " " + str(now.year)
today_nums = str(now.month) + "-" + str(now.day) + "-" + str(now.year)
# Define file path to write
filepath_prefix = 'C:\\Users\\tpcheshire\\Documents\\Kinetiscope Profiles\\'
filepath_pu_pr = filepath_prefix + today + '\\pu-pr'
filepath_pr = filepath_prefix + today + '\\pr'
os.makedirs(filepath_pu_pr,exist_ok = True)
os.makedirs(filepath_pr,exist_ok = True)

# Dictionary to change suffix of files
suffix_switch = {
        1   :   " fs " + today_nums + ".prf",
        2   :   " ps " + today_nums + ".prf",
        3   :   " ns " + today_nums + ".prf"
        }


# Signal resolution
tolerance_1 = 0.001
tolerance_2 = 0.005

# Define pulse full width half maxima
FWHM_pr = (80e-15) ** 2
FWHM_pu = (40e-15) ** 2
# Define pulse centers
pr_center = np.sqrt(-np.log(tolerance_1)*2*FWHM_pr)
pu_center = np.sqrt(-np.log(tolerance_1)*2*FWHM_pu) + 5.0e-13

# Time parameters
dt = 0.5e-15
ti = 0
tf = 1.1e-9
true_tf = 5.0e-6

# Define probe pulse window
time_pr_pulse_window = np.arange(ti,tf,dt)
# Define pump pulse window
time_pu_pulse_window = np.arange(ti,tf,dt)

# Define pump-probe delay
delays = np.array([-5.0e2,-4.0e2,-3.0e2,-2.0e2,-1.0e2,0])
for imag in np.arange(1,6):
    delays = np.append(delays, np.arange(1, 10) * 10**imag)
delays = np.append(delays, 1e6)*1e-15

# Compute pulse intensities
probe_pulse = np.exp(-(time_pr_pulse_window - pr_center) ** 2 / 2 / FWHM_pr)
pump_pulse = np.exp(-(time_pu_pulse_window - pu_center) ** 2 / 2 / FWHM_pu)

# Trim pulses
probe_pulse[probe_pulse <= tolerance_1] = 0
pump_pulse[pump_pulse <= tolerance_1] = 0

# Loop over delay times, combine pulse sequence, write to file
for delay in [800*1e-15]:#delays:
    # Create pulse sequence
    probe_pulse = 0.1 * np.exp(-(time_pr_pulse_window - pu_center - delay) ** 2 / 2 / FWHM_pr)
    probe_pulse[probe_pulse <= tolerance_1] = 0
    pulse_comb = pump_pulse + probe_pulse
    pulse_probe = probe_pulse

    # Remove unnecessary 0s
    time_pulse_window = time_pr_pulse_window[pulse_comb >= tolerance_1]
    time_pulse_window = np.append(time_pulse_window,[tf])
    pulse = pulse_comb[pulse_comb >= tolerance_1]
    pulse = np.append(pulse,[0])
    pulse[pulse <= tolerance_2] = 0
    pulse_probe = pulse_probe[pulse_comb >= tolerance_1]
    pulse_probe = np.append(pulse_probe,[0])
    pulse_probe[pulse_probe <= tolerance_2] = 0
    
    #
    if time_pulse_window[0] != 0:
        time_pulse_window = np.insert(time_pulse_window,0,0)
        pulse = np.insert(pulse,0,1e-20)
        pulse_probe = np.insert(pulse_probe,0,1e-20)
    elif pulse[0] == 0:
        pulse[0] = 1e-20
        pulse_probe[0] = 1e-20
    
    # Add last point to data
    time_pulse_window = np.append(time_pulse_window, true_tf)
    pulse = np.append(pulse, 0)
    pulse_probe = np.append(pulse_probe, 0)

    # Combine data for writing
    data_pu_pr = np.array([time_pulse_window,pulse]).T
    data_pr = np.array([time_pulse_window,pulse_probe]).T
    #ldata = np.size(data,0)
    
    # Create output file name
    if delay < 1e-12: file_suffix = suffix_switch[1]; delay_str = str(int(delay * 1e15))
    elif delay < 1e-9: file_suffix = suffix_switch[2]; delay_str = str(int(delay * 1e12))
    elif delay < 1e-6: file_suffix = suffix_switch[3]; delay_str = str(int(delay * 1e9))

    file_pu_pr = '\\Pu-Pr Pulse Seq ' + delay_str + file_suffix
    file_pr = '\\Pr Pulse Seq ' + delay_str + file_suffix
    filepath_filename_pu_pr = filepath_pu_pr + file_pu_pr
    filepath_filename_pr = filepath_pr + file_pr
    
    # Write to file
    np.savetxt(filepath_filename_pu_pr,data_pu_pr)    
    np.savetxt(filepath_filename_pr,data_pr)    

    mplot.figure("pulse")
    mplot.plot(time_pulse_window,pulse_probe,'r-')
    mplot.plot(time_pu_pulse_window,pump_pulse,'b-')
    mplot.plot(time_pulse_window,pulse,'k--')
    mplot.xlim(0, np.abs(delay) + pu_center + 2e-13)
    mplot.title(delay_str)
    mplot.legend(("probe","pump","pulse seq"))
    mplot.pause(0.0001)
    mplot.cla()
mplot.close("pulse")
