# Import libraries and classes
import tkinter as tk


class tc_button_parameters:
    """"""
    def __init__(self,name):
        """Instantiate parameters keeper for a new button"""
        self.name = name


    def set_grid_position(self,row,col):
        """"""
        self.row = row
        self.col = col


class tc_exit_button(tk.Tk, tc_button_parameters):
    """description of class"""

    def __init__(self,parent,parameters):
        """Instantiate next button"""

        def exit_button_cmd():
            """Early termination of application"""
            parent.next = False
            parent.destroy()
        # End of function exit_button_cmd

        self.exit_button_frame = tk.Frame(parent)
        self.exit_button_frame.grid(row = parameters.row, column = parameters.col)#3,0
        self.exit_button = tk.Button(self.exit_button_frame, command = exit_button_cmd,
                                     fg="black", text = parameters.name)#exit
        self.exit_button.pack()


class tc_next_button(tk.Tk, tc_button_parameters):
    """description of class"""

    def __init__(self,parent,parameters):
        """Instantiate next button"""
        def next_button_cmd():
            """"""
            parent.next = True
            parent.destroy()
        
        self.next_button_frame = tk.Frame(parent)
        self.next_button_frame.grid(row = parameters.row, column = parameters.col)#3,3
        self.next_button = tk.Button(self.next_button_frame, command = next_button_cmd,
                                     fg="black", text = parameters.name)
        self.next_button.pack()


class tc_okay_button(tk.Tk, tc_button_parameters):
    """description of class"""

    def __init__(self,parent,parameters):
        """Instantiate next button"""
        
        self.okay_button_frame = tk.Frame(parent)
        self.okay_button_frame.grid(row = parameters.row, column = parameters.col)
        self.okay_button = tk.Button(self.okay_button_frame, command = self.okay_button_cmd,
                                     fg="black", text = parameters.name)
        self.okay_button.pack()

    def okay_button_cmd(self):
        """"""
        print("Whoa that was close!")
        parent.destroy()
