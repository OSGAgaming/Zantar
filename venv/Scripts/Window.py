from tkinter import *
from Entities import *
import importlib
from typing import Type, TypeVar

import time

class Scene:
    def __init__(self, win):
        self.entityHost = EntityHost(win)
        self.cameraPosition = Vector2(0,0)
        self.onStart()

    def onStart(self):
        pass

    def update(self):
        pass


class GameWindow:
    T = TypeVar("T", bound=Scene)

    def __init__(self, width, height):
        self.updating = True
        self.refreshRate = 1
        self.win = Tk()
        self.win.geometry(str(width) + "x" + str(height))
        self.canvas = Canvas(self.win, bg="black", height=height, width=width)
        self.canvas.pack()
        self.widgets = []
        self.scene = None

    def addWidget(self, widget):
        self.widgets.append(widget)

    def nextScene(self, scene: Type[T]) -> T:
        self.canvas.delete("all")
        for widget in self.widgets:
            widget.destroy()
        self.scene = scene(self)


    def onUpdate(self):
        self.scene.entityHost.update()
        self.scene.update()
        self.win.after(self.refreshRate, self.onUpdate)

    def update(self):
        if self.updating:
            self.win.after(0, self.onUpdate)

    def start(self):
        self.updating = True

    def stop(self):
        self.updating = False
