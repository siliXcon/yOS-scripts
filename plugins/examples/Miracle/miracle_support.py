import sys, sxapi, tkinter as tk, tkinter.ttk as ttk

sxapi.search()
kontroler = sxapi.node(0)
rpm = kontroler.variable("/driver/motor/rpmf")
iref = kontroler.variable("/driver/iref")


def set_Tk_var():
    global rpm_gui
    rpm_gui = tk.DoubleVar()
    global iref_gui
    iref_gui = tk.DoubleVar()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    update_tick()


def doPressed():
    kontroler.executeSimple("beep", "50")


def rePressed():
    kontroler.executeSimple("beep", "52")


def miPressed():
    kontroler.executeSimple("beep", "54")


def runPressed():
    kontroler.executeSimple("run", "0.5")


def stopPressed():
    kontroler.executeSimple("stop")


def update_tick():
    rpm_gui.set(rpm.get())
    iref.set(iref_gui.get())
    root.after(33, update_tick)


def destroy_window():
    global top_level
    top_level.destroy()
    top_level = None
