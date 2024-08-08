import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor


# Create a random dataset
rng = np.random.RandomState(1)
X = np.sort(200 * rng.rand(600, 1) - 100, axis=0)
y = np.array([np.pi * np.sin(X).ravel(), np.pi * np.cos(X).ravel()]).T
y += (0.5 - rng.rand(*y.shape))
print(y.shape,X.shape)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=400, test_size=200, random_state=4)

max_depth = 30
regr_multirf = MultiOutputRegressor(RandomForestRegressor(n_estimators=100,
                                                          max_depth=max_depth,
                                                          random_state=0))
regr_multirf.fit(X_train, y_train)

regr_rf = RandomForestRegressor(n_estimators=100, max_depth=max_depth,
                                random_state=2)
regr_rf.fit(X_train, y_train)

# Predict on new data
y_multirf = regr_multirf.predict(X_test)
y_rf = regr_rf.predict(X_test)

# Plot the results
plt.figure()
s = 50
a = 0.4
plt.scatter(y_test[:, 0], y_test[:, 1], edgecolor='k',
            c="navy", s=s, marker="s", alpha=a, label="Data")
plt.scatter(y_multirf[:, 0], y_multirf[:, 1], edgecolor='k',
            c="cornflowerblue", s=s, alpha=a,
            label="Multi RF score=%.2f" % regr_multirf.score(X_test, y_test))
plt.scatter(y_rf[:, 0], y_rf[:, 1], edgecolor='k',
            c="c", s=s, marker="^", alpha=a,
            label="RF score=%.2f" % regr_rf.score(X_test, y_test))
plt.xlim([-6, 6])
plt.ylim([-6, 6])
plt.xlabel("target 1")
plt.ylabel("target 2")
plt.title("Comparing random forests and the multi-output meta estimator")
plt.legend()
plt.show()



#import tkinter as tk
#from tkinter import filedialog,messagebox
#import numpy as np
#from tc_windows.get_ta_files import get_ta_files
#import matplotlib.pyplot as mplot
#from scipy.signal import savgol_filter
#from utilities_chirp import find_index,scorrect
#from utilities_raw_ta_processing import subtract_baseline, fit_frequency_domain

#initial_directory = "C:\\Users\\tpcheshire\\Documents\\Project_Dye Kinetics\\Moran Data\\" \
#    + "Fitted Data for ALL SAMPLES\\1\\In Solution\\Ru(bpy) Complex 1\\Chirp Corrected"

#root = tk.Tk()
#root.initial_directory = initial_directory

#ta_files = get_ta_files(root,"Get TA files")
#root.iconify()

#delay_file = ta_files.delay[0]#"initial_directory + \\td1.dat"
#wvln_file = ta_files.wvln[0]#initial_directory + "\\wvlnCCS200.dat"
#ta_file = ta_files.ta[0]#initial_directory + "\\log1.dat"

#delay = np.loadtxt(delay_file, delimiter = ",")
#wvln = np.loadtxt(wvln_file)
#ta = np.loadtxt(ta_file, delimiter = "\t")




#root.mainloop()

