import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()

file_path = filedialog.askdirectory()

print(file_path)