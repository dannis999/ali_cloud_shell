'tkinter 相关'

import tkinter
from tkinter.constants import *
from tkinter import ttk

class gui(tkinter.Tk):
    def __init__(self,*a,**k):
        super().__init__(*a,**k)

    def mainloop(self):
        super().mainloop()

if __name__=='__main__':
    gui().mainloop()
