# Import libraries and classes
import tkinter as tk

class main_frame(tk.Tk):
    """Create and maintain main frame text label"""
    def __init__(self, parent, main_frame_text):
        """Initialize main frame label
        
        parent      :   the window in which self is realized. In this case, a child window"""
        self.main_frame = tk.Frame(parent)
        self.main_frame.grid(row = 1, column = 1, rowspan = 2, columnspan = 2)
        self.main_frame_label = tk.Label(self.main_frame, height = 5, text = main_frame_text,
                                         width = 100)
        self.main_frame_label.pack()
    # End function: __init__
# End class: main_frame
