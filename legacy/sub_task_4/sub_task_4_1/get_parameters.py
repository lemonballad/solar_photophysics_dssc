# Import libraries and classes
from .get_ta_files import get_ta_files
import numpy as np
from tkinter import filedialog, messagebox
from utilities_chirp import chirp_fitter
from utilities_raw_ta_processing import raw_ta_processing_messages


# Functions

def get_parameters(case, parent):
    """Initiates the processes for getting chirp parameters
    case:
        1.1     :   Parameters file exists and parameters are loaded directly from it
        1.2     :   Parameters file does not exist and needs to be generated from TA files
        else    :   Someone broke my program
    parent      :   The window from which the children are spawned. In this case it is the root window.
    """

    parameters_message = raw_ta_processing_messages(case, False, parent)
    if case == 1.1:
        parameters = parameters_exist(parent)
    elif case == 1.2:
        parameters = parameters_do_not_exist(parent)
    else:
        parameters_message = raw_ta_processing_messages(case, True, parent)
        messagebox.showerror(message = parameters_message,
                             title = "ERROR! TIME TO FREAK OUT!")
        parent.destroy()
    return parameters
# End function: get_parameters


def parameters_do_not_exist(parent):
    """There is not an existing parameters file or the user does not know where it is.
    
    Delay, wavelength, and TA files are collected and processed to generate a parameters file"""
    # Inform the user of what needs to happen
    parameters_message = raw_ta_processing_messages(1.2, False, parent)
    messagebox.showinfo(message = parameters_message, title = "We got this.")
    files = get_ta_files(parent, "Collecting TA Files for Chirp Correction")
    parent.next = files.next
    if files.next:
        parameters_message = raw_ta_processing_messages(1.21, False, parent)
        messagebox.showinfo(message = parameters_message)
        parameters = chirp_fitter(500, files.delay[0], files.wvln[0], files.ta[0], True)

        parameters_message = raw_ta_processing_messages(1.22, False, parent)
        messagebox.showinfo(message = parameters_message)
        save_parameters_file = filedialog.asksaveasfilename(initialdir = parent.initial_directory,
                                                            parent = parent,
                                                            title = "Save Parameters to...")
        np.savetxt(save_parameters_file, parameters)
# End function parameters_do_not_exist


def parameters_exist(parent):
    """There is an existing parameters file."""

    # Inform the user of what needs to happen
    parameters_message = raw_ta_processing_messages(1.1, False, parent)
    messagebox.showinfo(message = parameters_message, title = "We're plugging along.")
    try:
        parameters_file_name = filedialog.askopenfilenames(initialdir = parent.initial_directory,
                                                       parent = parent,
                                                       title = "Getting Existing Parameters File")
        parameters_file = list(parameters_file_name)
        parameters = np.loadtxt(parameters_file[0])
    except ValueError:
        error_message = raw_ta_processing_messages(2, True, parent)
        messagebox.showinfo(message = error_message, title = "ERROR! TIME TO FREAK OUT!")
        parent.next = False
        parent.deiconify()
        parent.destroy()
        parameters = None
    return parameters
# End function parameters exist