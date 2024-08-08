# Import libraries and classes
from chirp import chirp
import tkinter as tk


def app_open(root,app):
    """"""
    app_window = tk.Toplevel()
    app_window.lift(root)
    app += "(app_window)"
    return eval(app)




def main(): 
    def exit_cmd():
        print(chirp_app.chirp_parameters_file)
        root.withdraw()

    root = tk.Tk()
    #chirp_app = app_open(root,"chirp")
    chirp_window = tk.Toplevel()
    chirp_window.lift(root)
    root.iconify()
    chirp_app = chirp(chirp_window)


    exit_button = tk.Button(root, command = exit_cmd, text = "Done")
    exit_button.pack()
    root.mainloop()

if __name__ == '__main__':
    main()


#import tkinter.filedialog as filedialog

## --- functions ---
#def chirp_parameters_button_browse():
#    chirp_parameters_file = filedialog.askopenfilenames(parent = chirp_window, title='Choose a file')  
#    chirp_parameters_entry.insert(20, chirp_parameters_file)


#def chirp_delay_button_browse():
#    chirp_delay_file = filedialog.askopenfilenames(parent = chirp_window, title='Choose a file')    
#    chirp_delay_entry.insert(20, chirp_delay_file)


#def chirp_wvln_button_browse():
#    chirp_wvln_file = filedialog.askopenfilenames(parent = chirp_window, title='Choose a file')    
#    chirp_wvln_entry.insert(20, chirp_wvln_file)


#def chirp_ta_button_browse():
#    chirp_ta_file = filedialog.askopenfilenames(parent = chirp_window, title='Choose a file')    
#    chirp_ta_entry.insert(20, chirp_ta_file)


#def chirp_button_cmd():

#    if chirp_button_intvar.get():
#        # Add chirp parameter widgets
#        chirp_parameters_label.pack()
#        chirp_parameters_entry.pack()
#        chirp_parameters_button.pack()
#        # Remove previous chirp delay, wvln, and TA file widgets
#        # Delay files
#        chirp_delay_label.pack_forget()
#        chirp_delay_entry.pack_forget()
#        chirp_delay_button.pack_forget()
#        # Wvln files
#        chirp_wvln_label.pack_forget()
#        chirp_wvln_entry.pack_forget()
#        chirp_wvln_button.pack_forget()
#        # TA files
#        chirp_ta_label.pack_forget()
#        chirp_ta_entry.pack_forget()
#        chirp_ta_button.pack_forget()

#        # Keep final button final
#        chirp_execute_button.pack_forget()
#        chirp_execute_button.pack()
#    else:
#        # Add previous chirp delay, wvln, and TA file widgets
#        # Remove previous chirp parameter widgets
#        chirp_parameters_label.pack_forget()
#        chirp_parameters_entry.pack_forget()
#        chirp_parameters_button.pack_forget()

#        # Delay files
#        chirp_delay_label.pack()
#        chirp_delay_entry.pack()
#        chirp_delay_button.pack()
#        # Wvln files
#        chirp_wvln_label.pack()
#        chirp_wvln_entry.pack()
#        chirp_wvln_button.pack()
#        # TA files
#        chirp_ta_label.pack()
#        chirp_ta_entry.pack()
#        chirp_ta_button.pack()
#        # Keep final button final
#        chirp_execute_button.pack_forget()
#        chirp_execute_button.pack()


#def chirp_execute_button_cmd():
#    if chirp_button_intvar.get():
#        print("Something something dark side")
#        chirp_window.withdraw()
#    else:
#        print("You want a popcycle")
#        chirp_window.withdraw()


## --- main ---

## Main window
#chirp_window = tk.Tk()

## Main message
#msg_txt = "We need to collect information to process your TA data.\n\n"
#msg_txt += "Consider if 'Chirp' parameters have already been determined,\n"
#msg_txt += "what data sets those parameters are for, and what data files you have."
#msg = tk.Label(chirp_window, height = 0, justify = 'left', text = msg_txt,
#                    width = 0, wraplength = False)
#msg.pack()

## Create check box for chirp parameters
#chirp_button_txt = "Chirp parameters have been computed"
#chirp_button_intvar = tk.IntVar()
#chirp_button = tk.Checkbutton(chirp_window, command = chirp_button_cmd,
#                              text = chirp_button_txt, variable = chirp_button_intvar)
#chirp_button.pack()

## Define chirp widgets when box is checked on
#chirp_parameters_txt = "Chirp parameters File:"
#chirp_parameters_label = tk.Label(chirp_window, text = chirp_parameters_txt)
#chirp_parameters_entry = tk.Entry(chirp_window)
#chirp_parameters_button_txt="Browse"
#chirp_parameters_button = tk.Button(chirp_window, command = chirp_parameters_button_browse,
#                                    text=chirp_parameters_button_txt)

## Define chirp widgets when box is checked off
## Delay file
#chirp_delay_txt = "Chirp delay File:"
#chirp_delay_label = tk.Label(chirp_window, text = chirp_delay_txt)
#chirp_delay_entry = tk.Entry(chirp_window)
#chirp_delay_button_txt="Browse"
#chirp_delay_button = tk.Button(chirp_window, command = chirp_delay_button_browse,
#                                    text=chirp_delay_button_txt)
## Wvln file
#chirp_wvln_txt = "Chirp wavelength File:"
#chirp_wvln_label = tk.Label(chirp_window, text = chirp_wvln_txt)
#chirp_wvln_entry = tk.Entry(chirp_window)
#chirp_wvln_button_txt="Browse"
#chirp_wvln_button = tk.Button(chirp_window, command = chirp_wvln_button_browse,
#                                    text=chirp_wvln_button_txt)
## TA file
#chirp_ta_txt = "Chirp TA File:"
#chirp_ta_label = tk.Label(chirp_window, text = chirp_ta_txt)
#chirp_ta_entry = tk.Entry(chirp_window)
#chirp_ta_button_txt="Browse"
#chirp_ta_button = tk.Button(chirp_window, command = chirp_ta_button_browse,
#                                    text=chirp_ta_button_txt)

## Initial state 
## Delay files
#chirp_delay_label.pack()
#chirp_delay_entry.pack()
#chirp_delay_button.pack()
## Wvln files
#chirp_wvln_label.pack()
#chirp_wvln_entry.pack()
#chirp_wvln_button.pack()
## TA files
#chirp_ta_label.pack()
#chirp_ta_entry.pack()
#chirp_ta_button.pack()

## Process chirp files or accept chirp parameter file
#if (chirp_button_intvar.get()):
#    chirp_execute_button_txt = "Use chirp parameters"
#else:
#    chirp_execute_button_txt = "Process chirp files"
#chirp_execute_button = tk.Button(chirp_window, command = chirp_execute_button_cmd,
#                                    text=chirp_execute_button_txt)
#chirp_execute_button.pack()

## Continue until window is closed or files are processed
#chirp_window.mainloop()



### This is the module for creating gui for getting files and directories. There of course is a lot in this module. Good documentation can be found
### here: https://wiki.python.org/moin/TkInter
##import tkinter as tk
##from tkinter import filedialog
##from tkinter import IntVar
##from tkinter import Checkbutton
##from tkinter import messagebox

### this is a widget object thing. Something about Tcl/Tk that we don't really need to understand to get it's magic
##root = tk.Tk()
##msgbox = messagebox.askyesno()
##offset = IntVar()
##checkbox = Checkbutton(root, text="offset subtraction", variable=offset)
##checkbox.pack()
### This line closes an annoying extra window that plays no role for our purposes
##filez = filedialog.askopenfilenames(parent=root,title='Choose a file')
##root.withdraw()
### Go get the file names that we want to open

### This breaks the list of filenames into an array of filenames
##lst = list(filez)
##print(lst)
##print(lst[0])

##t = np.loadtxt(lst[0])
##w = np.loadtxt(lst[1])

##print(t[0:10])
##print(w[0:10])
### BOOM!