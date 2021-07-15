import os
import tkinter as tk
import tkinter.messagebox
var = os.system("python eightDirection.py")
window = tk.Tk()
window.withdraw()
tkinter.messagebox.showerror("错误报告", str(var))
