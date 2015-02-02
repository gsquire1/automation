#!/usr/bin/env python3

###############################################################################
####
#### GUI for FLOW VISION
####
###############################################################################



from tkinter import *
from tkinter import ttk

root = Tk()

root.title("FLOW VISION")

ttk.Button(root, text="Test Case 1").grid()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=2, row=2, sticky=(N,W,E,S))
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(2, weight=1)

ipaddr = StringVar()


ip_entry = ttk.Entry(mainframe, width=10, textvariable = ipaddr)

ip_entry.grid(column=1, row=1, sticky=(W,E))













root.mainloop()