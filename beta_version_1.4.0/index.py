import os
import tkinter as tk
import tkinter.messagebox
var = os.system("python eightDirection.py")
if var != 0:
    window = tk.Tk()
    window.withdraw()
    tkinter.messagebox.showerror("错误报告", str(var))
exit()
