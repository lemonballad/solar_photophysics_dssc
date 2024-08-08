import numpy as np
import shutil

path = "C:\\Users\\tpcheshire\\Documents\\Kinetiscope Results\\October 2018\\"\
    + "October 24 2018\\Pump Off\\"

old_name = path + "fsTA Toy Model.rxn"

suffix_switch = {
        1   :   " fs Pump Off 10-24-2018.rxn",
        2   :   " ps Pump Off 10-24-2018.rxn",
        3   :   " ns Pump Off 10-24-2018.rxn"
        }

# Define pump-probe delay
delays = np.array([-5.0e2,-4.0e2,-3.0e2,-2.0e2,-1.0e2,0])
for imag in np.arange(1,6):
    delays = np.append(delays, np.arange(1, 10) * 10**imag)
delays = np.append(delays, 1e6)

for delay in delays:
    if delay < 1e3:
        delay_str = str(int(delay))
        new_name = path + delay_str + suffix_switch[1]
    elif delay < 1e6:
        delay_str = str(int(delay/1e3))
        new_name = path + delay_str + suffix_switch[2]
    else:
        delay_str = str(int(delay/1e6))
        new_name = path + delay_str + suffix_switch[3]
    print(new_name)
    shutil.copy2(old_name, new_name)