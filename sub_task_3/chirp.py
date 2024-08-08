import tkinter.filedialog as filedialog
import tkinter as tk


class chirp:
    """description of class"""


    # --- functions ---


    def __init__(self,name):
        def chirp_parameters_button_browse():
            chirp_parameters_file = filedialog.askopenfilenames(parent = name,
                                                                     title='Choose a file')  
            chirp_parameters_entry.delete(0, last = "end")
            chirp_parameters_entry.insert(20, chirp_parameters_file)
            chirp_get_all()
            self.chirp_parameters_file = list(chirp_parameters_file)


        def chirp_delay_button_browse():
            chirp_delay_file = filedialog.askopenfilenames(parent = name,
                                                                title='Choose a file')    
            chirp_delay_entry.delete(0, last = "end")
            chirp_delay_entry.insert(20, chirp_delay_file)
            chirp_get_all()
            self.chirp_delay_file = list(chirp_delay_file)

        def chirp_wvln_button_browse():
            chirp_wvln_file = filedialog.askopenfilenames(parent = name,
                                                               title='Choose a file')    
            chirp_wvln_entry.delete(0, last = "end")
            chirp_wvln_entry.insert(20, chirp_wvln_file)
            chirp_get_all()
            self.chirp_wvln_file = list(chirp_wvln_file)

        def chirp_ta_button_browse():
            chirp_ta_file = filedialog.askopenfilenames(parent = name,
                                                             title='Choose a file')    
            chirp_ta_entry.delete(0, last = "end")
            chirp_ta_entry.insert(20, chirp_ta_file)
            chirp_get_all()
            self.chirp_ta_file = list(chirp_ta_file)

        def chirp_button_cmd():

            if chirp_button_intvar.get():
                # Add chirp parameter widgets
                chirp_parameters_label.pack()
                chirp_parameters_entry.pack()
                chirp_parameters_button.pack()
                # Remove previous chirp delay, wvln, and TA file widgets
                # Delay files
                chirp_delay_label.pack_forget()
                chirp_delay_entry.pack_forget()
                chirp_delay_button.pack_forget()
                # Wvln files
                chirp_wvln_label.pack_forget()
                chirp_wvln_entry.pack_forget()
                chirp_wvln_button.pack_forget()
                # TA files
                chirp_ta_label.pack_forget()
                chirp_ta_entry.pack_forget()
                chirp_ta_button.pack_forget()

                # Keep final button final
                chirp_execute_button.pack_forget()
                chirp_execute_button.pack()
            else:
                # Add previous chirp delay, wvln, and TA file widgets
                # Remove previous chirp parameter widgets
                chirp_parameters_label.pack_forget()
                chirp_parameters_entry.pack_forget()
                chirp_parameters_button.pack_forget()

                # Delay files
                chirp_delay_label.pack()
                chirp_delay_entry.pack()
                chirp_delay_button.pack()
                # Wvln files
                chirp_wvln_label.pack()
                chirp_wvln_entry.pack()
                chirp_wvln_button.pack()
                # TA files
                chirp_ta_label.pack()
                chirp_ta_entry.pack()
                chirp_ta_button.pack()
                # Keep final button final
                chirp_execute_button.pack_forget()
                chirp_execute_button.pack()
            chirp_get_all()


        def chirp_execute_button_cmd():
            if chirp_button_intvar.get():
                print("Something something darkside")
                self.open = False
                name.destroy()
            else:
                print("You want a popcycle")
                self.open = False
                name.destroy


        def chirp_get_all():
            chirp_button_flag = chirp_button_intvar.get()
            if chirp_button_flag:
                chirp_parameter_file = chirp_parameters_entry.get()
                if chirp_parameter_file:
                    chirp_execute_button.config(state = "normal")
                else:
                    chirp_execute_button.config(state = "disabled")
            else:
                chirp_delay_file = chirp_delay_entry.get()
                chirp_wvln_file = chirp_wvln_entry.get()
                chirp_ta_file = chirp_ta_entry.get()
                if chirp_delay_file and chirp_wvln_file and chirp_ta_file:
                    chirp_execute_button.config(state = "normal")
                    return self.chirp_parameters_file
                else:
                    chirp_execute_button.config(state = "disabled")


        # Main __init__
        self.name = name
        self.open = True
        self.chirp_parameters_file = ""
        # Main message
        msg_txt = "We need to collect information to process your TA data.\n\n"
        msg_txt += "Consider if 'Chirp' parameters have already been determined,\n"
        msg_txt += "what data sets those parameters are for, and what data files you have."
        msg = tk.Label(name, height = 0, justify = 'left', text = msg_txt,
                           width = 0, wraplength = False)
        msg.pack()

        # Create check box for chirp parameters
        chirp_button_txt = "Chirp parameters have been computed"
        chirp_button_intvar = tk.IntVar()
        chirp_button = tk.Checkbutton(name, command = chirp_button_cmd,
                                      text = chirp_button_txt, variable = chirp_button_intvar)
        chirp_button.pack()

        # Define chirp widgets when box is checked on
        chirp_parameters_txt = "Chirp parameters File:"
        chirp_parameters_label = tk.Label(name, text = chirp_parameters_txt)
        chirp_parameters_entry = tk.Entry(name)
        chirp_parameters_button_txt="Browse"
        chirp_parameters_button = tk.Button(name, command = chirp_parameters_button_browse,
                                            text = chirp_parameters_button_txt)

        # Define chirp widgets when box is checked off
        # Delay file
        chirp_delay_txt = "Chirp delay File:"
        chirp_delay_label = tk.Label(name, text = chirp_delay_txt)
        chirp_delay_entry = tk.Entry(name)
        chirp_delay_button_txt="Browse"
        chirp_delay_button = tk.Button(name, command = chirp_delay_button_browse,
                                            text = chirp_delay_button_txt)
        # Wvln file
        chirp_wvln_txt = "Chirp wavelength File:"
        chirp_wvln_label = tk.Label(name, text = chirp_wvln_txt)
        chirp_wvln_entry = tk.Entry(name)
        chirp_wvln_button_txt="Browse"
        chirp_wvln_button = tk.Button(name, command = chirp_wvln_button_browse,
                                        text = chirp_wvln_button_txt)
        # TA file
        chirp_ta_txt = "Chirp TA File:"
        chirp_ta_label = tk.Label(name, text = chirp_ta_txt)
        chirp_ta_entry = tk.Entry(name)
        chirp_ta_button_txt="Browse"
        chirp_ta_button = tk.Button(name, command = chirp_ta_button_browse,
                                            text = chirp_ta_button_txt)

        # Initial state 
        # Delay files
        chirp_delay_label.pack()
        chirp_delay_entry.pack()
        chirp_delay_button.pack()
        # Wvln files
        chirp_wvln_label.pack()
        chirp_wvln_entry.pack()
        chirp_wvln_button.pack()
        # TA files
        chirp_ta_label.pack()
        chirp_ta_entry.pack()
        chirp_ta_button.pack()

        # Process chirp files or accept chirp parameter file
        if (chirp_button_intvar.get()):
            chirp_execute_button_txt = "Use chirp parameters"
        else:
            chirp_execute_button_txt = "Process chirp files"
        chirp_execute_button = tk.Button(name, command = chirp_execute_button_cmd,
                                         state = "disabled", text = chirp_execute_button_txt)
        chirp_execute_button.pack()

        # Continue until window is closed or files are processed

        