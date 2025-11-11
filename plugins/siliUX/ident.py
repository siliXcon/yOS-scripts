"""
ident.py

The automatic-identification part of the siliTune SXAPI plugin for ESCx controllers.

This module is part of the YOS/SWTools project.

Date:
   2024

Copyright:
   siliXcon (c) all rights reserved. Redistribution and usage of this code
   in another project without the author's agreement is not allowed.
"""

import sxapi, tkinter, customtkinter, math, os
from queue import Queue
from PIL import Image, ImageTk
import threading

from siliUX import codetostr
from siliUX.messagebox import *
from siliUX.ctk_tooltip import *

################################################################################

identrun_count = 1
interrupt = False


def advSwitch():
    if checkbox_adv.get():
        # Advanced mode - show individual buttons
        identlinButton.grid_remove()
        identrunButton.grid_remove()
        autoidentButton.grid_remove()
        identlinButton.grid(row=2, column=0, padx=10, pady=10)
        identrunButton.grid(row=2, column=1, padx=10, pady=10)

        accelBox.configure(state="normal")
        currentBox.configure(state="normal")
        durationBox.configure(state="normal")
        checkbox_nlin.configure(state="normal")
        checkbox_pid.configure(state="normal")
        spinupButton.configure(state="normal")
        identsatButton.configure(state="normal")
        identsalButton.configure(state="normal")
        identlinButton.configure(state="normal")
        identrunButton.configure(state="normal")
        # currentBox.insert(0,"iref/4")
        accelBox.insert(0, "200")
        durationBox.insert(0, "4000")
    else:
        # Simple mode - show automatic button only
        identlinButton.grid_remove()
        identrunButton.grid_remove()
        autoidentButton.grid_remove()
        autoidentButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        accelBox.delete(0, 100)
        durationBox.delete(0, 100)
        currentBox.delete(0, 100)
        accelBox.configure(state="disabled")
        currentBox.configure(state="disabled")
        durationBox.configure(state="disabled")
        checkbox_nlin.configure(state="disabled")
        checkbox_pid.configure(state="disabled")
        spinupButton.configure(state="disabled")
        identsatButton.configure(state="disabled")
        identsalButton.configure(state="disabled")


def enableButtons(enabled):
    if enabled:
        interruptButton.configure(state="disabled")
        checkbox_adv.configure(state="normal")
        if checkbox_adv.get():
            identlinButton.configure(state="normal")
            identrunButton.configure(state="normal")
        else:
            autoidentButton.configure(state="normal")
        if checkbox_adv.get():
            accelBox.configure(state="normal")
            currentBox.configure(state="normal")
            durationBox.configure(state="normal")
            checkbox_nlin.configure(state="normal")
            checkbox_pid.configure(state="normal")
            spinupButton.configure(state="normal")
            identsatButton.configure(state="normal")
            identsalButton.configure(state="normal")
    else:
        interruptButton.configure(state="normal")
        checkbox_adv.configure(state="disabled")
        identlinButton.configure(state="disabled")
        identrunButton.configure(state="disabled")
        autoidentButton.configure(state="disabled")
        accelBox.configure(state="disabled")
        currentBox.configure(state="disabled")
        durationBox.configure(state="disabled")
        checkbox_nlin.configure(state="disabled")
        checkbox_pid.configure(state="disabled")
        spinupButton.configure(state="disabled")
        identsatButton.configure(state="disabled")
        identsalButton.configure(state="disabled")


def describe_error(error):
    if error == -101:
        MessageBox(
            window,
            cls=2,
            title="Automatic identification",
            message="The driver is not initialized.\nPlease initialize first (e.g. using 'init as:' in siliTune).",
        )
    elif error == -102:
        MessageBox(
            window,
            cls=2,
            title="Automatic identification",
            message="The drive is active.\nPlease ensure that motor command is deactivated first (e.g. through 'stop' command).",
        )
    elif error == -103:
        MessageBox(
            window,
            cls=2,
            title="Automatic identification",
            message="A limiter is active.\nPlease ensure that limiter thresholds are deactivated or wide enough for the identification.",
        )
    elif error == -105:
        MessageBox(
            window,
            cls=2,
            title="Automatic identification",
            message="The motor is not ready.\nPlease ensure that the motor is properly connected, free from load and standing still.",
        )
    elif error == -110:
        MessageBox(
            window,
            cls=2,
            title="Automatic identification",
            message="R_t (coil resistance) is not set.\nPlease set it manually or run the 'identlin' to measure first.",
        )
    elif error <= -10 and error >= -100:
        MessageBox(
            window,
            cls=2,
            title="Automatic identification",
            message="Current control / inductance measurement error in stage "
            + str(-error)
            + "\nPlease adjust the PID / current reference.\n("
            + codetostr.error2string(my_node.variable("/driver/error").get())
            + ")",
        )


def on_key_press(event):
    # Put the character into the queue
    char_queue.put(event.char)


def update_cb(state, res, stdout_data):

    if state < 0:
        retlabel.configure(text="Timed out !", fg_color="red")
        enableButtons(1)
        return

    elif state > 0:
        retlabel.configure(text="Running !", fg_color="yellow")

    else:
        if res < 0:
            retlabel.configure(text="Resulted with error " + str(res), fg_color="red")
        elif res > 0:
            retlabel.configure(
                text="Succeeded with warning (" + str(res) + ")", fg_color="green"
            )
        else:
            retlabel.configure(text="Succeeded !", fg_color="green")

    if isinstance(stdout_data, str):
        outputBox.insert("end", stdout_data)
        outputBox.see("end")

    elif state == 0:
        enableButtons(1)
        describe_error(res)

    elif interruptButton.cget("state") == "disabled":
        interruptButton.configure(state="normal")
        return "\r\n"

    elif not char_queue.empty():
        char_list = []
        while not char_queue.empty():
            char_list.append(char_queue.get())
        return "".join(char_list)

    return None


def identrun_cb(state, res, stdout_data):
    r = update_cb(state, res, stdout_data)
    if state == 0 and not isinstance(stdout_data, str):
        if res == -1:
            MessageBox(
                window,
                cls=2,
                title="Automatic identification",
                message="Flux linkage could not be measured.\nPlease ensure that the rotor can freely move and optionally, adjust the acceleration and current.",
            )
        elif res == 1:
            try:
                # dummy pull (just to refresh the emgui values). TODO find way how to trigger pull on a directory!
                my_node.variable("/driver/motor/psi").get()
            except sxapi.error as e:
                print(e)

            MessageBox(
                window,
                cls=1,
                title="Automatic identification",
                message="Sensor was not identified !",
            )
        elif res == 0:
            try:
                # dummy pull (just to refresh the emgui values). TODO find way how to trigger pull on a directory!
                my_node.variable("/driver/motor/psi").get()
                my_node.variable("/driver/rest/hvar").get()
                my_node.variable("/driver/rest/rangle").get()
                my_node.variable("/driver/rest/roff1").get()
                my_node.variable("/driver/rest/roff2").get()
                my_node.variable("/driver/rest/rpole").get()
            except sxapi.error as e:
                print(e)

            MessageBox(
                window,
                title="Automatic identification",
                message="Identrun succeeded and values were updated.\nDo not forget to save your parameters to flash after the evaluation!",
            )

    return r


def identlin_cb(state, res, stdout_data):
    r = update_cb(state, res, stdout_data)
    if state == 0 and not isinstance(stdout_data, str):
        if res == 0:
            try:
                # dummy pull (just to refresh the emgui values). TODO find way how to trigger pull on a directory!
                my_node.variable("/driver/motor/Rt").get()
                my_node.variable("/driver/motor/Lq").get()
                my_node.variable("/driver/motor/Ld").get()
                my_node.variable("/driver/motor/Da").get()
                my_node.variable("/driver/motor/Dc").get()

                my_node.variable("/driver/pid_iq/P").get()
                my_node.variable("/driver/pid_iq/I").get()
                my_node.variable("/driver/pid_id/P").get()
                my_node.variable("/driver/pid_id/I").get()
            except sxapi.error as e:
                print(e)

            MessageBox(
                window,
                title="Automatic identification",
                message="Identlin succeeded and values were updated.\nDo not forget to save your parameters to flash after the evaluation!",
            )

    return r


def spinup_cb(state, res, stdout_data):
    # a firmware bug workaround: -11 is reported when success of 'spinup'
    if res == -11:
        res = 0
    return update_cb(state, res, stdout_data)


def identlin():
    try:
        if checkbox_nlin.get():
            if checkbox_pid.get():
                my_node.execute("identlin", "-n", update=identlin_cb)
            else:
                my_node.execute("identlin", "-nP", update=identlin_cb)
        else:
            if checkbox_pid.get():
                my_node.execute("identlin", "-N", update=identlin_cb)
            else:
                my_node.execute("identlin", "-NP", update=identlin_cb)

    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        return

    retlabel.configure(text="Identlin started", fg_color=("gray78", "gray23"))
    outputBox.delete("0.0", "end")
    enableButtons(0)


def spinup():
    try:
        if currentBox.get() == "":
            my_node.execute(
                "spinup",
                accelBox.get(),
                durationBox.get(),
                update=spinup_cb,
                timeout=10000,
            )
        else:
            my_node.execute(
                "spinup",
                accelBox.get(),
                durationBox.get(),
                currentBox.get(),
                update=spinup_cb,
                timeout=10000,
            )

    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        return

    retlabel.configure(text="Spin-up started", fg_color=("gray78", "gray23"))
    outputBox.delete("0.0", "end")
    enableButtons(0)


def interrupt_cb():
    global interrupt
    interrupt = True
    # TODO make the "interrupt" signal working (through RPC) !
    interruptButton.configure(state="disabled")


def autoident_stop_cb(state, res, stdout_data):
    """Callback for the stop command in autoident sequence"""
    if state == 0:  # Command completed
        retlabel.configure(
            text="Step 1/3: Stop completed, waiting 2s...", fg_color="yellow"
        )
        # Schedule identlin after 2 seconds
        window.after(2000, autoident_run_identlin)        
    elif state < 0:  # Timeout
        retlabel.configure(text="Stop command timed out!", fg_color="red")
        enableButtons(1)


def autoident_run_identlin():
    """Run identlin as part of autoident sequence"""
    retlabel.configure(text="Step 2/3: Running identlin...", fg_color="yellow")

    try:
        my_node.execute("identlin", update=autoident_identlin_cb)

    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        enableButtons(1)


def autoident_identlin_cb(state, res, stdout_data):
    """Callback for identlin in autoident sequence"""
    r = update_cb(state, res, stdout_data)

    if state == 0 and not isinstance(stdout_data, str):
        if res == 0:

            retlabel.configure(
                text="Step 2/3: Identlin completed, waiting 1s...", fg_color="yellow"
            )
            # Schedule identrun after 1 second
            global identrun_count
            prest = my_node.variable("/driver/prest").get()

            if prest == 3:
                identrun_count = 2
            else:
                identrun_count = 1

            global interrupt
            if interrupt:
                retlabel.configure(text=f"Interrupted by user", fg_color="red")
                enableButtons(1)
            else:
                window.after(1000, autoident_run_identrun)
        else:
            retlabel.configure(text=f"Identlin failed with error {res}", fg_color="red")
            enableButtons(1)

    return r


def autoident_run_identrun():
    """Run identrun as part of autoident sequence"""
    retlabel.configure(text="Step 3/3: Running identrun...", fg_color="yellow")

    try:
        my_node.execute("identrun", update=autoident_identrun_cb, timeout=10000)
    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        enableButtons(1)


def autoident_identrun_cb(state, res, stdout_data):
    """Callback for identrun in autoident sequence"""
    r = update_cb(state, res, stdout_data)
    global identrun_count, interrupt

    if state == 0 and not isinstance(stdout_data, str):
        if res == -1:
            MessageBox(
                window,
                cls=2,
                title="Automatic identification",
                message="Flux linkage could not be measured.\nPlease ensure that the rotor can freely move and optionally, adjust the acceleration and current.",
            )
        elif res == 1:
            try:
                # dummy pull (just to refresh the emgui values)
                my_node.variable("/driver/motor/psi").get()
                my_node.variable("/driver/rest/hvar").get()
                my_node.variable("/driver/rest/rangle").get()
                my_node.variable("/driver/rest/roff1").get()
                my_node.variable("/driver/rest/roff2").get()
                my_node.variable("/driver/rest/rpole").get()
            except sxapi.error as e:
                print(e)

            MessageBox(
                window,
                cls=1,
                title="Automatic identification",
                message="Sensor was not identified !",
            )
        elif res == 0:
            identrun_count -= 1
            if identrun_count > 0:
                retlabel.configure(
                    text=f"Step 3/3: Identrun completed with success, repeating ({identrun_count} runs left)...",
                    fg_color="yellow",
                )
                # Schedule next identrun after 1 second

                if interrupt:
                    retlabel.configure(text=f"Interrupted by user", fg_color="red")
                    enableButtons(1)
                else:
                    window.after(1000, autoident_run_identrun)
                    return r
            else:
                interrupt = False

            try:
                # dummy pull (just to refresh the emgui values)
                my_node.variable("/driver/motor/Rt").get()
                my_node.variable("/driver/motor/Lq").get()
                my_node.variable("/driver/motor/Ld").get()
                my_node.variable("/driver/motor/Da").get()
                my_node.variable("/driver/motor/Dc").get()
                my_node.variable("/driver/pid_iq/P").get()
                my_node.variable("/driver/pid_iq/I").get()
                my_node.variable("/driver/pid_id/P").get()
                my_node.variable("/driver/pid_id/I").get()
            except sxapi.error as e:
                print(e)

            if not interrupt:
                MessageBox(
                    window,
                    title="Automatic identification",
                    message="Automatic identification completed successfully!\nIdentlin and Identrun values were updated.\nDo not forget to save your parameters to flash after the evaluation!",
                )

    return r


def autoident():
    """Start automatic identification sequence: stop -> identlin -> identrun"""
    retlabel.configure(text="Step 1/3: Stopping motor...", fg_color="yellow")
    outputBox.delete("0.0", "end")
    enableButtons(0)
    global interrupt
    interrupt = False

    try:
        # Start the sequence by executing stop command
        my_node.execute("stop", update=autoident_stop_cb)
    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        enableButtons(1)


def identrun():
    # NOTE: older versions of auxiliary module (in the _ESC) did not recognize the options (e.g. -'-q")
    # Instead, it is interpret them as a positional argument and parsed out as number,
    # causing sometimes the procedure to halt since zero is parsed out from the string.
    # That's why we don't send any arguments here, unless 'advanced' is checked.
    # Newer version of _ESC should ignore unknown options, extending the compatibility for future improvements.

    try:
        if checkbox_adv.get():
            my_node.open("{scope}")
            if currentBox.get() == "":
                my_node.execute(
                    "identrun",
                    "-w",  # TODO - this causes HANG when not supported by the fw !
                    accelBox.get(),
                    durationBox.get(),
                    update=identrun_cb,
                    timeout=10000,
                )
            else:
                my_node.execute(
                    "identrun",
                    "-w",  # TODO - this causes HANG when not supported by the fw !
                    accelBox.get(),
                    durationBox.get(),
                    currentBox.get(),
                    update=identrun_cb,
                    timeout=10000,
                )
        else:
            my_node.execute(
                "identrun",
                # "-q",  #TODO - this causes HANG when not supported by the fw !
                update=identrun_cb,
                timeout=10000,
            )

    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        return

    retlabel.configure(text="Identrun started", fg_color=("gray78", "gray23"))
    outputBox.delete("0.0", "end")
    enableButtons(0)


def identsat():
    try:
        if checkbox_adv.get():
            my_node.open("{scope}")
            my_node.execute("identsat", "-w", update=update_cb, timeout=10000)
        else:
            my_node.execute(
                "identsat",
                # "-q",  #TODO - this causes HANG when not supported by the fw !
                update=update_cb,
                timeout=10000,
            )

    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        return

    retlabel.configure(text="Identsat started", fg_color=("gray78", "gray23"))
    outputBox.delete("0.0", "end")
    enableButtons(0)


def identsal():
    try:
        if checkbox_adv.get():
            my_node.open("{scope}")
            my_node.execute("identsal", "-w", update=update_cb, timeout=10000)
        else:
            my_node.execute(
                "identsal",
                # "-q",  #TODO - this causes HANG when not supported by the fw !
                update=update_cb,
                timeout=10000,
            )

    except sxapi.error as e:
        retlabel.configure(text=str(e), fg_color="red")
        return

    retlabel.configure(text="Identsal started", fg_color=("gray78", "gray23"))
    outputBox.delete("0.0", "end")
    enableButtons(0)


# to receive asynchronous callbacks from sxapi
def poll_events():
    sxapi.poll()
    window.after(100, poll_events)


def AutomaticIdentification(n, parent):
    global my_node, window, char_queue, retlabel, outputBox, checkbox_adv, accelBox, currentBox, durationBox, checkbox_nlin, checkbox_pid, identlinButton, identrunButton, identsatButton, identsalButton, spinupButton, interruptButton, autoidentButton

    my_node = n
    window = customtkinter.CTkToplevel()

    window.attributes("-topmost", 1)
    # window.eval("tk::PlaceWindow . center")
    x, y = window.winfo_pointerxy()
    window.geometry(f"{640}x{600}+{x}+{y}")
    window.title("Automatic motor identification")
    lib_dir = os.path.dirname(__file__) + "/"
    window.iconbitmap(lib_dir + "SiliXcon.ico")

    icon = Image.open(
        lib_dir + "flux.png"
    )  # Make sure you have a PNG version of your icon
    photo = ImageTk.PhotoImage(icon)
    window.iconphoto(False, photo)

    window.grid_rowconfigure((0), weight=1)
    window.grid_columnconfigure((0, 1, 2), weight=1)
    window.focus()

    outputBox = customtkinter.CTkTextbox(window)  # , state="disabled")
    outputBox.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
    outputBox.bind("<Key>", on_key_press)
    char_queue = Queue()

    outputBox.insert(
        "0.0",
        "The system offers a few procedures for measuring motor parameters. You can start them from below.\n\n"
        "HINTS:\n"
        " - For SON/COS sensor run identrun at least 3 times for convergence.\n"
        " - Typically, a successful 'identlin' followed by 'identrun' is recommended for the minimal setup.\n"
        " - The resulting values will be stored as corresponding parameters (in /driver, /motor, and /rest folders).\n"
        " - The controller must be powered with sufficient current and within the operating voltage range.\n"
        " - The sensor mapping during 'identrun' is a convergent procedure. Repeat multiple times if needed.\n"
        " - No limiters/warnings must be active before starting a procedure and the driver must be in freewheel mode.\n"
        "\nCAUTION:\n"
        " - The rotor will be positioned into various angles and must be load-free for all procedures !\n"
        " - The motor may spin, shake and make noise ! Do not use when engaged within a vehicle !\n"
        " - Do not forget saving new values to flash before reboot !\n"
        "\nADVANCED:\n"
        " - In case of current instability, adjust the PID settings and/or 'iref' value.\n"
        " - When motor is to be operated close to magnetic saturation, measure Da and Dc derating coefficients.\n"
        " - If the rotor fails to spin up with 'identrun', adjust the acceleration, current and duration values.\n"
        " - 'identrun' of a back-driven motor can be performed by setting acceleration to zero.\n"
        " - 'identrun', 'identsat' and 'identsal' use SCOPE tool for visualization (in advanced mode).\n"
        " - 'identsat' and 'identsal' results produce visualization only and do not identify/store any values.\n",
    )

    identlinButton = customtkinter.CTkButton(
        window, text=f"1. IdentLin ...", command=identlin, border_width=2
    )
    identlinButton.grid(row=2, column=0, padx=10, pady=10)
    CTkToolTip(
        identlinButton,
        message="Measure the motor inductance (Lq, Ld) and resistance (Rt).\nOptionally, derating parameters (Da, Dc) can be evaulated too.",
    )

    identrunButton = customtkinter.CTkButton(
        window, text=f"2. IdentRun ...", command=identrun, border_width=2
    )
    identrunButton.grid(row=2, column=1, padx=10, pady=10)
    CTkToolTip(
        identrunButton,
        message="Measure the motor KV (psi) and, mapping parameters of the selected shaft sensor.\nFor some types of sensors, identrun must be performed multiple times.",
    )

    autoidentButton = customtkinter.CTkButton(
        window, text=f"Automatic Identification", command=autoident, border_width=2
    )
    # Initially hidden, will be shown when advanced mode is off
    CTkToolTip(
        autoidentButton,
        message="Automatically run identlin followed by identrun for complete motor identification.",
    )

    interruptButton = customtkinter.CTkButton(
        window,
        text=f"Interrupt !",
        command=interrupt_cb,
        fg_color="darkred",
        state="disabled",
    )
    interruptButton.grid(row=2, column=2, padx=10, pady=10)
    CTkToolTip(
        interruptButton,
        message="Attempt to terminate the proceudure.",
    )

    adv_frame = customtkinter.CTkFrame(window, fg_color="transparent", border_width=2)
    adv_frame.grid(
        row=5, column=0, columnspan=4, padx=(10, 10), pady=(10, 10), sticky="sew"
    )
    adv_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

    identsatButton = customtkinter.CTkButton(
        adv_frame, text=f"IdentSat ...", command=identsat, state="disabled"
    )
    identsatButton.grid(row=0, column=10, padx=10, pady=5)
    CTkToolTip(
        identsatButton,
        message="Measure and display the motor magnetic saturation (dependency of the inductances to the stator current).",
    )

    identsalButton = customtkinter.CTkButton(
        adv_frame, text=f"IdentSal ...", command=identsal, state="disabled"
    )
    identsalButton.grid(row=1, column=10, padx=10, pady=2)
    CTkToolTip(
        identsalButton,
        message="Measure and display the motor saliency (dependency of the inductances to the rotor electrical angle).",
    )

    spinupButton = customtkinter.CTkButton(
        adv_frame, text=f"Try spin-up ...", command=spinup, width=100, state="disabled"
    )
    spinupButton.grid(row=2, column=10, padx=10, pady=5, sticky="ew")
    CTkToolTip(spinupButton, message="Try the spin-up in dry mode (no identification)")

    checkbox_adv = customtkinter.CTkSwitch(
        adv_frame, text="Advanced", command=advSwitch
    )
    checkbox_adv.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    checkbox_nlin = customtkinter.CTkCheckBox(
        adv_frame, text="Find deratings", state="disabled"
    )
    checkbox_nlin.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    checkbox_nlin.select()
    CTkToolTip(
        checkbox_nlin,
        message="Attempt to find the inductance derating parameters during identlin.",
    )

    checkbox_pid = customtkinter.CTkCheckBox(
        adv_frame, text="Find PID gains", state="disabled"
    )
    checkbox_pid.grid(row=2, column=1, padx=10, pady=2, sticky="w")
    checkbox_pid.select()
    CTkToolTip(
        checkbox_pid,
        message="Attempt to preset the PID parameters during identlin (if supported by the firmware).",
    )

    i = 2
    j = 0
    customtkinter.CTkLabel(
        adv_frame, text="Spin-up acceleration :", text_color="grey"
    ).grid(row=j, column=i, sticky="e")
    accelBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    accelBox.grid(row=j, column=i + 1, pady=5, padx=3, sticky="ew")
    customtkinter.CTkLabel(adv_frame, text="[rad/s/s]", text_color="grey").grid(
        row=j, column=i + 2, sticky="w"
    )
    CTkToolTip(
        accelBox,
        message="Define the acceleration for synchronous spin-up during identrun.",
    )

    i = 2
    j = 1
    customtkinter.CTkLabel(
        adv_frame, text="Spin-up duration :", text_color="grey"
    ).grid(row=j, column=i, sticky="e")
    durationBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    durationBox.grid(row=j, column=i + 1, pady=2, padx=3, sticky="ew")
    customtkinter.CTkLabel(adv_frame, text="[ms]", text_color="grey").grid(
        row=j, column=i + 2, sticky="w"
    )
    CTkToolTip(
        durationBox,
        message="Define the time of the synchronous spin-up during identrun.",
    )

    i = 2
    j = 2
    customtkinter.CTkLabel(adv_frame, text="Spin-up current :", text_color="grey").grid(
        row=j, column=i, sticky="e"
    )
    currentBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    currentBox.grid(row=j, column=i + 1, pady=5, padx=3, sticky="ew")
    customtkinter.CTkLabel(adv_frame, text="[A]", text_color="grey").grid(
        row=j, column=i + 2, sticky="w"
    )
    CTkToolTip(
        currentBox,
        message="Define the drive current for the synchronous spin-up (default is iref/4).",
    )

    # customtkinter.CTkLabel(adv_frame, text="Steps", text_color="grey").grid(row=j, column=i, sticky="e")
    # cyclesBox = customtkinter.CTkEntry(adv_frame, width=40, state="disabled")
    # cyclesBox.grid(row=j, column=i+1, pady=5, padx=3, sticky="ew")
    # cyclesBox.insert("0.0","10000")
    # customtkinter.CTkLabel(adv_frame, text="[A]").grid(row=j, column=i+2, sticky="w")
    # CTkToolTip(cyclesBox, message="Override the procedure step count.")

    retlabel = customtkinter.CTkLabel(
        window,
        text="Status bar",
        font=customtkinter.CTkFont(weight="bold"),
        corner_radius=5,
        compound="left",
        fg_color=("gray78", "gray23"),
    )
    retlabel.grid(row=6, column=0, columnspan=4, padx=(10, 10), pady=5, sticky="nsew")
    CTkToolTip(retlabel, message="The result and value of the lastly issued command.")

    # Initially show automatic button (advanced mode is off by default)
    identlinButton.grid_remove()
    identrunButton.grid_remove()
    autoidentButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # start the poll loop for async events
    poll_events()

    window.mainloop()
