"""
 find_nodes.py

 The common code for siliXXX plugins for discovering nodes of a particular family.

 This module is part of the YOS/SWTools project.

 Date:
    2024

 Copyright:
    siliXcon (c) all rights reserved. Redistribution and usage of this code
    in another project without the author's agreement is not allowed.
"""

import tkinter, customtkinter, sxapi, os

def MessageBox(message):
    app = customtkinter.CTk()
    app.attributes("-topmost", 1)
    # app.eval("tk::PlaceWindow.center")
    x, y = app.winfo_pointerxy()
    app.geometry(f"+{x}+{y}")
    app.title("Find nodes")
    lib_dir = os.path.dirname(__file__)
    app.iconbitmap()
    app.iconphoto(False, tkinter.PhotoImage(file=lib_dir + "/SiliXcon.png"))
    customtkinter.CTkLabel(app, text=message).pack(padx=20, pady=20)
    customtkinter.CTkButton(app, text=f"OK", command=app.destroy).pack(padx=20, pady=20)
    app.mainloop()


def find(family, io = 3):
    try:
        nodeCount = sxapi.search(dummy=1)
        if nodeCount < 1:
            nodeCount2 = sxapi.search()
            if nodeCount2 < 1:
                MessageBox("No device was found, search error " + str(nodeCount2))
                raise ValueError()  # no other way to kill the script without exitting emgui
            nodeCount = nodeCount2

    except sxapi.error as e:
        MessageBox("SXAPI error " + str(e))
        exit()

    nodes = []
    nodenames = []

    for i in range(nodeCount):
        newNode = sxapi.node(
            i, iomode=io
        )
        if newNode.hwid().decode()[:3] == family:
            nodes.append(newNode)
            nodenames.append(
                newNode.name.decode() + " (" + newNode.address.decode() + ")"
            )

    if len(nodes) < 1:
        MessageBox("None of the available nodes is an " + family + " member !")
        raise ValueError()  # no other way to kill the script without exitting emgui

    return nodes, nodenames
