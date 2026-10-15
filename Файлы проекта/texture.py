from tkinter import PhotoImage

_frames = {}

def load(name, file_name):
    image = PhotoImage(file=file_name)
    _frames[name] = image

def get(name):
    return _frames[name]