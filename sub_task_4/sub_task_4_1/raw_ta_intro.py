from .main_frame import main_frame
from .tc_buttons import tc_button_parameters, tc_exit_button, tc_next_button
from tkinter import filedialog, messagebox 
import tkinter as tk
from utilities_raw_ta_processing import raw_ta_processing_messages

class raw_ta_intro(tk.Tk):
    """Wrapper for the introduction window to the Raw TA Processing application"""
    def __init__(self,parent):
        """Instantiation creates a window with:
            a main dialog frame
            an exit button for leaving the application
            a next button for begining the application
        
        parent      :   the window from which the child is spawned. In this case the root window."""
        # Instantiate new child
        self.child = tk.Toplevel(parent)
        # Raise child above parent
        tk.Toplevel.lift(self.child, aboveThis = parent)
        parent.iconify()

        # Instantiate main frame label
        main_frame_text = raw_ta_processing_messages(0, False, parent)
        main_frame_label = main_frame(self.child, main_frame_text)

        # Instantiate exit button
        exit_button_parameters = tc_button_parameters("EXIT")
        exit_button_parameters.set_grid_position(3,0)
        exit_button = tc_exit_button(self.child,exit_button_parameters)    

        # Instantiate next button
        next_button_parameters = tc_button_parameters("NEXT")
        next_button_parameters.set_grid_position(3,3)
        next_button = tc_next_button(self.child,next_button_parameters)
              
        # Title of current window
        self.child.title("Raw TA Proccessing")
        
        # Loop on current window until closed
        parent.wait_window(self.child)

        parent.next = self.child.next

        # What shall we do next????
        if self.child.next:
            # Get initial directory
            message_txt = raw_ta_processing_messages(0.1, False, parent)
            parent.initial_directory = filedialog.askdirectory(title = message_txt, parent = parent)

            # Ask about a parameters file
            main_frame_label_txt = raw_ta_processing_messages(1, False, parent)
            parameters_file_answer = messagebox.askyesno(icon = "question",
                                                     message = main_frame_label_txt,
                                                     parent = parent, title = "Parameters File?")

            if parameters_file_answer:
                self.case = 1.1
            else:
                self.case = 1.2
            parent.next = self.child.next
        else:
            parent.deiconify()
            parent.destroy()

    # End function: __init__
# End class: raw_ta_intro