import math

from tkinter import *
from Entities import *
from MyMath import *
from Window import *

currentKeysPressed = []


def on_event(event):
    global currentKeysPressed
    text = event.char if event.num == '??' else event.num
    if text not in currentKeysPressed:
        currentKeysPressed.append(text)


def on_release(event):
    global currentKeysPressed
    text = event.char if event.num == '??' else event.num
    if text in currentKeysPressed:
        currentKeysPressed.remove(text)


def sqaureEntityUpdate(entity, camera):
    rb = entity.getModule("RigidBody")
    entity.getCanvas().moveto(entity.entityFields["rect"], rb.pos.x - camera.x, rb.pos.y - camera.y)


def sqaureEntityInitialise(entity):
    sizeOfBox = Vector2(2, 2)
    if entity.hasModule("Body2D"):
        sizeOfBox = entity.getModule("Body2D").bounds
    entity.entityFields["rect"] = entity.window.canvas.create_rectangle(0, 0, sizeOfBox.x, sizeOfBox.y, outline="white", fill="white")


def playerInit(entity):
    entity.entityFields["playerMovement"] = 0.001
    entity.entityFields["canJump"] = False
    entity.entityFields["JumpForce"] = 0.3
    entity.getModule("RigidBody").mass = 0.001


def playerMovement(entity):
    rb = entity.getModule("RigidBody")
    col = entity.getModule("Body2D")
    entity.entityFields["canJump"] = False

    global currentKeysPressed

    if "d" in currentKeysPressed:
        rb.vel.x += entity.entityFields["playerMovement"]
    if "a" in currentKeysPressed:
        rb.vel.x -= entity.entityFields["playerMovement"]

    if col.colliding:
        entity.entityFields["canJump"] = True

    if "w" in currentKeysPressed and entity.entityFields["canJump"]:
        rb.vel.y -= entity.entityFields["JumpForce"]

def tipIndicatorsUpdate(entity, camera):
   rb = entity.getModule("RigidBody")
   edit_circle(rb.pos.x - camera.x, rb.pos.y - camera.y, 4,entity.entityFields["circle"],entity.window.canvas)

def tipIndicatorsInit(entity):
    rb = entity.getModule("RigidBody")
    entity.entityFields["circle"] = create_circle(rb.pos.x, rb.pos.y, 4, entity.window.canvas, "yellow")


