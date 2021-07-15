import tkinter as tk
from tkinter import filedialog, messagebox

path = "./data/songs.txt"
name = "./data/song_name.txt"


def chooseFile():
    global path
    path = filedialog.askopenfilename(title="选择文件", initialdir="./data")


def chooseName():
    global name
    name = filedialog.askopenfilename(title="选择文件", initialdir="./data")


def startTrans():
    global path, name
    if not path or not name:
        messagebox.showerror(title="错误", message="未选择文件")
        return

    with open(path, "r", encoding="gbk") as file:
        dataList = file.readlines()
    for i in range(len(dataList)):
        temp = dataList[i].rstrip()
        dataList[i] = eval(temp)
    covers = dataList[0]
    songs = dataList[1]
    note_origins = []
    for i in range(2, len(dataList)):
        dataList[i].pop(0)
        note_origins.append(dataList[i])

    notes = []
    for d in note_origins:
        temp = []
        for i in range(0, len(d), 2):
            temp.append("    " + str((d[i] - 1, round(d[i + 1], 3))) + "\n")
        notes.append(temp)

    with open(name, "r", encoding="UTF-8") as file:
        nameList = file.readlines()

    songNames = eval(nameList[0])
    songLittleNames = eval(nameList[1])

    for i in range(len(covers)):
        covers[i] = "images/start/songs/" + covers[i]


    for i in range(len(songs)):
        songs[i] = "songs/foundation_pack/" + songs[i] + ".mp3"

    author = "None"
    noteDesigner = "Time_emit"

    print(songs)
    print(songNames)
    print(songLittleNames)
    print(notes)
    print(covers)

    for i in range(len(songNames)):
        path = "./notes/" + songNames[i] + ".txt"
        with open(path, "w", encoding="UTF-8") as file:
            noteTemp = ""
            for note in notes[i]:
                noteTemp = noteTemp + str(note)
            file.write(
                "name : " + songNames[i] + "\n" +
                "littleName : " + songLittleNames[i] + "\n" +
                "path : " + songs[i] + "\n" +
                "cover : " + covers[i] + "\n"
                "author : " + author + " \n" +
                "noteDesigner : " + noteDesigner + "\n" +
                noteTemp
            )

    try:
        pass
    except:
        messagebox.showerror(title="错误", message="转换失败")


window = tk.Tk()
window.geometry("500x500")

fileChoose = tk.Button(
    window,
    width=20,
    height=2,
    bg="lightGreen",
    text="选择要更新的文件",
    command=chooseFile
)
fileChoose.place(x=170, y=100)

nameChoose = tk.Button(
    window,
    width=20,
    height=2,
    bg="lightGreen",
    text="选择要更新的歌曲名称文件",
    command=chooseName
)
nameChoose.place(x=170, y=200)

start = tk.Button(
    window,
    width=20,
    height=2,
    bg="lightBlue",
    text="开始",
    command=startTrans
)
start.place(x=170, y=300)

window.mainloop()
