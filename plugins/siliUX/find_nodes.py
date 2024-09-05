import customtkinter, sxapi, os


def MessageBox(message):
    app = customtkinter.CTk()
    app.attributes("-topmost", 1)
    # app.eval("tk::PlaceWindow.center")
    x, y = app.winfo_pointerxy()
    app.geometry(f"+{x}+{y}")
    app.title("Find nodes")
    lib_dir = os.path.dirname(__file__)
    app.iconbitmap(lib_dir + "/SiliXcon.ico")
    customtkinter.CTkLabel(app, text=message).pack(padx=20, pady=20)
    customtkinter.CTkButton(app, text=f"OK", command=app.destroy).pack(padx=20, pady=20)
    app.mainloop()


def find(family):
    # Connect to the node
    try:
        nodeCount = sxapi.search(dummy=1)
        if nodeCount < 1:
            nodeCount2 = sxapi.search()
            if nodeCount2 < 1:
                MessageBox("No device was found, search error " + str(nodeCount2))
                raise ValueError()  # no other way to kill the script without exitting emgui
            nodeCount = nodeCount2

    except sxapi.error as e:
        # tkinter.messagebox.showerror("Error", "Failed to connect to the device")
        exit()

    # todo make these as function return
    nodes = []
    nodenames = []

    for i in range(nodeCount):
        newNode = sxapi.node(
            i, iomode=3
        )  # TODO explore other iomode options for better responsiveness and safety
        if newNode.hwid().decode()[:3] == family:
            nodes.append(newNode)
            nodenames.append(
                newNode.name.decode() + " (" + newNode.address.decode() + ")"
            )

    if len(nodes) < 1:
        MessageBox("None of the nodes is an " + family + " member!")
        raise ValueError()  # no other way to kill the script without exitting emgui

    return nodes, nodenames
