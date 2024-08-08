from .main_frame import main_frame
from .tc_buttons import tc_button_parameters, tc_exit_button, tc_next_button
from tkinter import filedialog
from tkinter import messagebox 
import tkinter as tk
from utilities_raw_ta_processing import raw_ta_processing_messages

class collect_file(tk.Tk):
    """"""

    def __init__(self, parent, label_txt, parameters):
        """"""
        def file_button_cmd():
            self.files = list(filedialog.askopenfilenames(initialdir = parent.initial_directory,
                                                          parent = parent,title = 'Choose a file'))  
            self.file_entry.delete(0, last = "end")
            self.file_entry.insert(20, self.files)
            self.file = list(self.files)


        # Define file collection widget
        self.file_frame = tk.Frame(parent)
        self.file_frame.grid(row = parameters.row, column = parameters.col, columnspan = 2)
        self.file_label = tk.Label(self.file_frame, text = label_txt, width = 20)
        self.file_entry = tk.Entry(self.file_frame)
        self.file_button_txt = "Browse"
        self.file_button = tk.Button(self.file_frame, command = file_button_cmd,
                                     fg="black", text = "Browse")#parameters.name)#Browse
        self.file_label.pack(side = "left")
        self.file_entry.pack(side = "left")
        self.file_button.pack(side = "left")
    # End function __init__ for class collect_file
# End class collect_file


class get_ta_files(tk.Tk):
    """description of class"""
    def __init__(self, parent, window_title):
        """"""
        # Instantiate new child
        self.child = tk.Toplevel(parent)
        # Raise child above parent
        tk.Toplevel.lift(self.child, aboveThis = parent)
        self.child.initial_directory = parent.initial_directory
        parent.iconify()

        # Instantiate main frame label
        main_frame_label_text = raw_ta_processing_messages(1.201, False, parent)
        main_frame_label = main_frame(self.child,main_frame_label_text)

        # Instantiate delay file insertion zone
        delay_button_parameters = tc_button_parameters("Browse")
        delay_button_parameters.set_grid_position(3,1)
        delay_collector = collect_file(self.child,"Delay File", delay_button_parameters)

        # Instantiate delay file insertion zone
        wvln_button_parameters = tc_button_parameters("Browse")
        wvln_button_parameters.set_grid_position(4,1)
        wvln_collector = collect_file(self.child,"Wavelength File", wvln_button_parameters)

        # Instantiate delay file insertion zone
        ta_button_parameters = tc_button_parameters("Browse")
        ta_button_parameters.set_grid_position(5,1)
        ta_collector = collect_file(self.child,"TA File", ta_button_parameters)

        # Instantiate exit button
        exit_button_parameters = tc_button_parameters("EXIT")
        exit_button_parameters.set_grid_position(6,0)
        exit_button = tc_exit_button(self.child,exit_button_parameters)    

        # Instantiate next button
        next_button_parameters = tc_button_parameters("NEXT")
        next_button_parameters.set_grid_position(6,3)
        next_button = tc_next_button(self.child,next_button_parameters)
              
        # Title of current window
        self.child.title(window_title)
        
        # Loop on current window until closed
        parent.wait_window(self.child)

        # Send out the files
        self.next = self.child.next
        if self.child.next:
            self.delay = delay_collector.file
            self.wvln = wvln_collector.file
            self.ta = ta_collector.file
            self.next = self.child.next
