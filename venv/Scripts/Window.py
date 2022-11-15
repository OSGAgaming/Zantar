from tkinter import *
from Entities import *
import time


class GameWindow:
    def __init__(self, width, height):
        self.updating = True
        self.refreshRate = 1
        self.win = Tk()
        self.win.geometry(str(width) + "x" + str(height))
        self.entityHost = EntityHost(self)
        self.canvas = Canvas(self.win, bg="black", height=height, width=width)
        self.canvas.pack()

        self.lastTime = time.time()

    def onUpdate(self):
        self.entityHost.update()
        self.win.after(self.refreshRate, self.onUpdate)

    def update(self):
        if self.updating:
            self.win.after(0, self.onUpdate)

    def start(self):
        self.updating = True

    def stop(self):
        self.updating = False
