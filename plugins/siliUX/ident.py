import sxapi
import tkinter
import math
import customtkinter
import codetostr


#for message box
from messagebox import MessageBox
from queue import Queue
from ctk_tooltip import *

# customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

################################################################################

def advSwitch():
    if checkbox_adv.get():
        accelBox.configure(state="normal")
        currentBox.configure(state="normal")
        durationBox.configure(state="normal")
        checkbox_nlin.configure(state="normal")
        checkbox_scope.configure(state="normal")
        checkbox_rscope.configure(state="normal")
        spinupButton.configure(state="normal")
        identsatButton.configure(state="normal")
        identsalButton.configure(state="normal")
        #currentBox.insert(0,"iref/4")
        accelBox.insert(0,"100")
        durationBox.insert(0,"8000")
    else:
        accelBox.delete(0, 100)
        durationBox.delete(0, 100)
        currentBox.delete(0, 100)
        accelBox.configure(state="disabled")
        currentBox.configure(state="disabled")
        durationBox.configure(state="disabled")
        checkbox_nlin.configure(state="disabled")
        checkbox_scope.configure(state="disabled")
        checkbox_rscope.configure(state="disabled")
        spinupButton.configure(state="disabled")
        identsatButton.configure(state="disabled")
        identsalButton.configure(state="disabled")

def enableButtons(enabled):
    if enabled:
        checkbox_adv.configure(state="normal")
        identlinButton.configure(state="normal")
        identrunButton.configure(state="normal")
        if checkbox_adv.get():
            accelBox.configure(state="normal")
            currentBox.configure(state="normal")
            durationBox.configure(state="normal")
            checkbox_nlin.configure(state="normal")
            checkbox_scope.configure(state="normal")
            checkbox_rscope.configure(state="normal")
            spinupButton.configure(state="normal")
            identsatButton.configure(state="normal")
            identsalButton.configure(state="normal")
    else:
        checkbox_adv.configure(state="disabled")
        identlinButton.configure(state="disabled")
        identrunButton.configure(state="disabled")
        accelBox.configure(state="disabled")
        currentBox.configure(state="disabled")
        durationBox.configure(state="disabled")
        checkbox_nlin.configure(state="disabled")
        checkbox_scope.configure(state="disabled")
        checkbox_rscope.configure(state="disabled")
        spinupButton.configure(state="disabled")
        identsatButton.configure(state="disabled")
        identsalButton.configure(state="disabled")


def describe_error(error):
    if error == -101:
        MessageBox(app, title="Automatic identification", message="ERROR: The driver is not initialized.\nPlease init with sensor of your chocice first (e.g. using 'init as:' in siliTune).")
    elif error == -102:
        MessageBox(app, title="Automatic identification", message="ERROR: The drive is active.\nPlease ensure that motor command is deactivated first (e.g. through 'stop' command).")
    elif error == -103:
        MessageBox(app, title="Automatic identification", message="ERROR: A limiter is active.\nPlease ensure that limiter thresholds are deactivated or wide enough for the identification.")
    elif error == -105:
        MessageBox(app, title="Automatic identification", message="ERROR: The motor is not ready.\nPlease ensure that the motor is properly connected, free from load and standing still.")
    elif error == -110:
        MessageBox(app, title="Automatic identification", message="ERROR: R_t (coil resistance) is not set.\nPlease set it manually or run the 'identlin' to measure first.")
    elif error <= -10 and error >= -100:
        MessageBox(app, title="Automatic identification", message="ERROR: Current control / inductance measurement error in stage " + str(-error) + "\nPlease adjust the PID settings / current reference.")

def on_key_press(event):
    # Put the character into the queue
    char_queue.put(event.char)

def update_cb(state, res, stdout_data):
    if state > 0:
        retlabel.configure(text="Running !", fg_color="yellow")
    elif state < 0:
        retlabel.configure(text="Timed out !", fg_color="red")
        enableButtons(1)
    elif res < 0:
        retlabel.configure(text="Resulted with error " + str(res), fg_color="red")
        enableButtons(1)
        describe_error(res)
    else:
        retlabel.configure(text="Succeeded ("  + str(res) + ")" , fg_color="green")
        enableButtons(1)

    if isinstance(stdout_data, str):
        outputBox.insert("end", stdout_data)

    elif not char_queue.empty():
        char_list = []
        while not char_queue.empty():
            char_list.append(char_queue.get())
        return ''.join(char_list)

    return None

def identrun_cb(state, res, stdout_data):
    if res == -1:
         MessageBox(app, title="Automatic identification", message="ERROR: Flux linkage could not be found.\nPlease ensure that the rotor can freely move and optionally, adjust the acceleration and current.")
    if res == 1:
         MessageBox(app, title="Automatic identification", message="WARNING: Sensor was not identified !")

    return update_cb(state, res, stdout_data)



def identlin():
    if checkbox_nlin.get():
        retval = my_node.execute("identlin", "-n", update=update_cb)
    else:
        retval = my_node.execute("identlin", update=update_cb)

    if retval < 0:
        retlabel.configure(text="Could not start identlin, error " + str(retval), fg_color="red")
    else:
        retlabel.configure(text="Started", fg_color=("gray78", "gray23"))
        outputBox.delete("0.0", "end")
        enableButtons(0)

def spinup():

    if currentBox.get() == "":
        retval = my_node.execute("spinup", accelBox.get(), durationBox.get(), update=update_cb, timeout=10000)
    else:
        retval = my_node.execute("spinup", accelBox.get(), durationBox.get(), currentBox.get(), update=update_cb, timeout=10000)

    if retval < 0:
        retlabel.configure(text="Could not start spinup, error " + str(retval), fg_color="red")
    else:
        retlabel.configure(text="Started", fg_color=("gray78", "gray23"))
        outputBox.delete("0.0", "end")
        enableButtons(0)

def identrun():
    if checkbox_scope.get():
        my_node.open("{scope}")

    checkbox_scope.deselect()

    # TODO simplify with argument list !!
    if checkbox_rscope.get():
        if checkbox_adv.get():
            if currentBox.get() == "":
                retval = my_node.execute("identrun", "-w", accelBox.get(), durationBox.get(), update=identrun_cb, timeout=10000)
            else:
                retval = my_node.execute("identrun", "-w", accelBox.get(), durationBox.get(), currentBox.get(), update=identrun_cb, timeout=10000)
        else:
            retval = my_node.execute("identrun", "-w", update=identrun_cb, timeout=10000)
    else:
        if checkbox_adv.get():
            if currentBox.get() == "":
                retval = my_node.execute("identrun", "-w", "-k", accelBox.get(), durationBox.get(), update=identrun_cb, timeout=10000)
            else:
                retval = my_node.execute("identrun", "-w", "-k", accelBox.get(), durationBox.get(), currentBox.get(), update=identrun_cb, timeout=10000)
        else:
            retval = my_node.execute("identrun", "-w", "-k", update=identrun_cb, timeout=10000)


    if retval < 0:
        retlabel.configure(text="Could not start identrun, error " + str(retval), fg_color="red")
    else:
        retlabel.configure(text="Started", fg_color=("gray78", "gray23"))
        outputBox.delete("0.0", "end")
        enableButtons(0)

def identsat():
    if checkbox_scope.get():
        my_node.open("{scope}")

    checkbox_scope.deselect()
    retval = my_node.execute("identsat", "-w", update=update_cb, timeout=10000)

    if retval < 0:
        retlabel.configure(text="Could not start identsat, error " + str(retval), fg_color="red")
    else:
        retlabel.configure(text="Started", fg_color=("gray78", "gray23"))
        outputBox.delete("0.0", "end")
        enableButtons(0)

def identsal():
    if checkbox_scope.get():
        my_node.open("{scope}")

    checkbox_scope.deselect()

    retval = my_node.execute("identsal", "-w", update=update_cb, timeout=10000)

    if retval < 0:
        retlabel.configure(text="Could not start identsal, error " + str(retval), fg_color="red")
    else:
        retlabel.configure(text="Started", fg_color=("gray78", "gray23"))
        outputBox.delete("0.0", "end")
        enableButtons(0)

#to receive asynchronous callbacks from sxapi
def poll_events():
    sxapi.poll()
    app.after(100, poll_events)

def AutomaticIdentification(n):
    global my_node, app, char_queue, retlabel, outputBox, checkbox_adv, accelBox, currentBox, durationBox, checkbox_nlin, checkbox_scope, checkbox_rscope, identlinButton, identrunButton, identsatButton, identsalButton, spinupButton

    my_node = n

    app = customtkinter.CTk()
    #app.attributes("-topmost", 1)
    #app.eval("tk::PlaceWindow . center")
    x, y = app.winfo_pointerxy()
    app.geometry(f"{640}x{600}+{x}+{y}")
    app.title("Automatic motor identification")
    app.iconbitmap("siliUX/SiliXcon.ico")
    #customtkinter.CTkLabel(app, text="ahoj").pack(padx=20, pady=20)
    app.grid_rowconfigure((0), weight=1)
    app.grid_columnconfigure((0,1,2,3), weight=1)


    outputBox = customtkinter.CTkTextbox(app) #, state="disabled")
    outputBox.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
    outputBox.bind("<Key>", on_key_press)
    char_queue = Queue()

    outputBox.insert("0.0", "The system offers a few procedures for measuring motor parameters. You can start them from below.\n\n"
                            "HINTS:\n"
                            " - Typically, a successful 'identlin' followed by 'identrun' is recommended for the minimal setup.\n"
                            " - The resulting values will be stored as corresponding parameters (in /motor and /rest folders).\n"
                            " - The controller must be powered with sufficient current and within the operating voltage range.\n"
                            " - The sensor learning during 'identrun' is a convergent procedure. Repeat multiple times if needed.\n"
                            " - No limiters/warnings must be active before starting a procedure.\n"
                            "\nCAUTION:\n"
                            " - The rotor will be positioned into various angles and must be load-free for all procedures !\n"
                            " - The motor may spin, shake and make noise ! Do not use when engaged within a vehicle !\n"
                            " - Do not forget saving new values to flash before reboot !\n"
                            "\nADVANCED:\n"
                            " - In case of current instability, adjust the PID settings and/or 'iref' value.\n"
                            " - If the rotor fails to spin up with 'identrun', adjust the acceleration, current and duration values.\n"
                            " - 'identrun' of a back-driven motor can be done by setting acceleration to zero.\n"
                            " - 'identrun', 'identsat' and 'identsal' sends recorded data to SCOPE tool for visualisation.\n"
                            " - 'identsat' and 'identsal' are for reference only and do not store any values.\n")


    identlinButton = customtkinter.CTkButton(app, text=f"1. IdentLin ...", command=identlin,  border_width=2)
    identlinButton.grid(row=2, column=0, padx=10, pady=10)
    CTkToolTip(identlinButton, message="Measure the motor inductance (Lq, Ld) and resistance (Rt).\nOptionally, derating parameters (Da, Dc) can be evaulated too.")

    identrunButton = customtkinter.CTkButton(app, text=f"2. IdentRun ...", command=identrun,  border_width=2)
    identrunButton.grid(row=2, column=1, padx=10, pady=10)
    CTkToolTip(identrunButton, message="Measure the motor KV (psi) and, mapping parameters of the selected shaft sensor.\nFor some types of sensors, identrun must be performed multiple times.")


    checkbox_adv = customtkinter.CTkSwitch(app, text="Advanced", command=advSwitch)
    checkbox_adv.grid(row=2, column=2, padx=10, pady=10)

    adv_frame = customtkinter.CTkFrame(app, fg_color="transparent", border_width=2)
    adv_frame.grid(row=5, column=0, columnspan=4,padx=(10, 10), pady=(10, 10), sticky="sew")
    adv_frame.grid_columnconfigure((1,2,3,4,5,6,7,8,9,10), weight=1)

    identsatButton = customtkinter.CTkButton(adv_frame, text=f"IdentSat ...",  command=identsat, state="disabled")
    identsatButton.grid(row=0, column=10, padx=10, pady=5)
    CTkToolTip(identsatButton, message="Measure and display the motor magnetic saturation (dependency of the inductances to the stator current).")

    identsalButton = customtkinter.CTkButton(adv_frame, text=f"IdentSal ...",  command=identsal, state="disabled")
    identsalButton.grid(row=1, column=10, padx=10, pady=2)
    CTkToolTip(identsalButton, message="Measure and display the motor saliency (dependency of the inductances to the rotor electrical angle).")

    spinupButton = customtkinter.CTkButton(adv_frame, text=f"Try spin-up ...", command=spinup, width=100,  state="disabled")
    spinupButton.grid(row=2, column=10, padx=10, pady=5, sticky="ew")
    CTkToolTip(spinupButton, message="Try the spin-up in dry mode (no identification)")


    checkbox_nlin = customtkinter.CTkCheckBox(adv_frame, text="Measure Da, Dc", state="disabled")
    checkbox_nlin.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    CTkToolTip(checkbox_nlin, message="Attempt to find the inductance derating parameters during identlin.")

    checkbox_scope = customtkinter.CTkCheckBox(adv_frame, text="Start scope", state="disabled")
    checkbox_scope.grid(row=1, column=1, padx=10, pady=2, sticky="w")
    checkbox_scope.select()
    CTkToolTip(checkbox_scope, message="Start an instance of the scope tool before relevant procedures.")

    checkbox_rscope = customtkinter.CTkCheckBox(adv_frame, text="Reset scope", state="disabled")
    checkbox_rscope.grid(row=2, column=1, padx=10, pady=2, sticky="w")
    checkbox_rscope.select()
    CTkToolTip(checkbox_rscope, message="Reset the scope before data plot.")


    i = 2
    j = 0
    customtkinter.CTkLabel(adv_frame, text="Spin-up acceleration :", text_color="grey").grid(row=j, column=i, sticky="e")
    accelBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    accelBox.grid(row=j, column=i+1, pady=5, padx=3, sticky="ew")
    customtkinter.CTkLabel(adv_frame, text="[rad/s/s]", text_color="grey").grid(row=j, column=i+2, sticky="w")
    CTkToolTip(accelBox, message="Override the acceleration speed in synchronous spinup during identrun.")

    i = 2
    j = 1
    customtkinter.CTkLabel(adv_frame, text="Spin-up duration :", text_color="grey").grid(row=j, column=i, sticky="e")
    durationBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    durationBox.grid(row=j, column=i+1, pady=2, padx=3, sticky="ew")
    customtkinter.CTkLabel(adv_frame, text="[ms]", text_color="grey").grid(row=j, column=i+2, sticky="w")
    CTkToolTip(durationBox, message="Define the spinup time for the synchronous spinup.")

    i = 2
    j = 2
    customtkinter.CTkLabel(adv_frame, text="Spin-up current :", text_color="grey").grid(row=j, column=i, sticky="e")
    currentBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    currentBox.grid(row=j, column=i+1, pady=5, padx=3, sticky="ew")
    customtkinter.CTkLabel(adv_frame, text="[A]", text_color="grey").grid(row=j, column=i+2, sticky="w")
    CTkToolTip(currentBox, message="Override the maximum current for the synchronous spinup (default iref/4).")

    #customtkinter.CTkLabel(adv_frame, text="Steps", text_color="grey").grid(row=j, column=i, sticky="e")
    #cyclesBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    #cyclesBox.grid(row=j, column=i+1, pady=5, padx=3, sticky="ew")
    #cyclesBox.insert("0.0","10000")
    #customtkinter.CTkLabel(adv_frame, text="[A]").grid(row=j, column=i+2, sticky="w")
    #CTkToolTip(cyclesBox, message="Override the procedure step count.")

    retlabel = customtkinter.CTkLabel(app, text="Status bar", font=customtkinter.CTkFont(weight="bold"), corner_radius=5, compound="left", fg_color=("gray78", "gray23"))
    retlabel.grid(row=6, column=0, columnspan=4, padx=(10,10), pady=5, sticky="nsew")
    CTkToolTip(retlabel, message="The result and value of the lastly issued command.")

    #start the poll loop for async events
    poll_events()

    app.mainloop()



    identsalButton = customtkinter.CTkButton(adv_frame, text=f"IdentSal ...", width=5, command=identsal, state="disabled")
    identsalButton.grid(row=1, column=10, padx=10, pady=10)
    CTkToolTip(identsalButton, message="Measure and display the motor saliency (dependency of the inductances to the rotor electrical angle).")

