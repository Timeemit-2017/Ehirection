import tkinter as tk

def showError(reason):
    error = tk.Tk()
    error.title("Error Report")
    error.geometry("500x300")
    text = tk.Label(error, text="Oops,游戏崩溃了!\n请尝试重新启动或重新下载游戏!\n具体原因如下：\n\n"+reason,
                    font = ("微软雅黑", 15),
                    fg = "red"
                    )
    text.pack()
    error.mainloop()