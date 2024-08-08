# Import libraries and classes
from tc_windows.get_parameters import get_parameters
from tc_windows.raw_ta_intro import raw_ta_intro
import time
from tkinter import messagebox
import tkinter as tk
from utilities_raw_ta_processing import raw_ta_processing_messages

# Functions
# main function
def main():
    # Local functions

    # Instantiate root window
    case = 0
    root = tk.Tk()

    # Instantiate first window
    intro_window = raw_ta_intro(root)

    # Load parameters file if it exists, otherwise make one and save it
    if root.next is True:   parameters = get_parameters(intro_window.case, root)
    if root.next is True:
        parameters_message = raw_ta_processing_messages(1.3, False, root)
        messagebox.showinfo(message = parameters_message, title = "It's Business Time")

        print(parameters)

    #
    if root.next is True:
        1

    root.mainloop()
    # root window is closed
# End of main function


# Execute main
if __name__ == '__main__':
    main()
