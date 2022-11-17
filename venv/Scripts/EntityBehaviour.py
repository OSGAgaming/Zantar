import copy
import math
import random

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
    entity.entityFields["rect"] = entity.window.canvas.create_rectangle(0, 0, sizeOfBox.x, sizeOfBox.y, outline="black",
                                                                        fill="black")


def playerInit(entity):
    entity.entityFields["playerMovement"] = 0.003
    entity.entityFields["canJump"] = False
    entity.entityFields["JumpForce"] = 1.1
    entity.entityFields["HoldingVine"] = None
    entity.entityFields["HoldCooldown"] = 0

    entity.getModule("RigidBody").mass = 0.008


def playerMovement(entity, scene):
    rb = entity.getModule("RigidBody")
    col = entity.getModule("Body2D")
    entity.entityFields["canJump"] = False
    heldVine = entity.entityFields["HoldingVine"]

    global currentKeysPressed

    if entity.entityFields["HoldCooldown"] > 0: entity.entityFields["HoldCooldown"] -= 1

    if heldVine is None:
        currentDist = -1
        closestVine = None

        for vine in scene.vines:
            vineRb = vine[1].getModule("RigidBody")
            dist = math.dist([vineRb.pos.x, vineRb.pos.y], [rb.pos.x, rb.pos.y])
            if dist < currentDist or currentDist == -1:
                currentDist = dist
                closestVine = vine[1]

        if closestVine is not None and currentDist < 35:
            if "e" in currentKeysPressed and entity.entityFields["HoldCooldown"] == 0:
                entity.entityFields["HoldingVine"] = closestVine
                entity.entityFields["HoldCooldown"] = 120

        if "d" in currentKeysPressed:
            rb.vel.x += entity.entityFields["playerMovement"]
        if "a" in currentKeysPressed:
            rb.vel.x -= entity.entityFields["playerMovement"]

        if col.colliding:
            entity.entityFields["canJump"] = True

            if random.randint(0,10) < max(abs(rb.vel.x * 2) - 0.75, 0):
                negVel = Vector2(-rb.vel.x * 0.5, -rb.vel.y * 0.5 - 0.05)

                particle = Entity([RigidBody(copy.copy(rb.pos), negVel, drag=0.998, mass=0)])

                particle.onInit += lambda e=particle: groundParticleInit(e)
                particle.onUpdate += lambda e=particle: groundParticleUpdate(e, scene)

                scene.entityHost.addEntity(particle)

        if "w" in currentKeysPressed and entity.entityFields["canJump"]:
            rb.vel.y -= entity.entityFields["JumpForce"]
    else:
        vineRb = heldVine.getModule("RigidBody")

        rb.pos.x += (vineRb.pos.x - rb.pos.x) / 6
        rb.pos.y += (vineRb.pos.y - rb.pos.y) / 6

        rb.vel.x = 0
        rb.vel.y = 0
        if "e" in currentKeysPressed and entity.entityFields["HoldCooldown"] == 0:
            entity.entityFields["HoldingVine"] = None
            entity.entityFields["HoldCooldown"] = 120
            rb.vel.x = vineRb.vel.x * 2
            rb.vel.y = vineRb.vel.y * 2


def tipIndicatorsUpdate(entity, camera, player):
    rb = entity.getModule("RigidBody")
    rbPlayer = player.getModule("RigidBody")

    dist = math.sqrt((rbPlayer.pos.x - rb.pos.x) ** 2 + (rbPlayer.pos.y - rb.pos.y) ** 2)
    radius = max(0, (100 - dist) / 25)
    edit_circle(rb.pos.x - camera.x, rb.pos.y - camera.y, radius, entity.entityFields["circle"], entity.window.canvas)


def tipIndicatorsInit(entity):
    rb = entity.getModule("RigidBody")
    entity.entityFields["circle"] = create_circle(rb.pos.x, rb.pos.y, 4, entity.window.canvas, "black")


def groundParticleUpdate(entity, scene):
    rb = entity.getModule("RigidBody")

    if entity.entityFields["timeLeft"] > 0:
        entity.entityFields["timeLeft"] -= 1
    else:
        entity.getCanvas().delete(entity.entityFields["rect"])
        scene.entityHost.entities.remove(entity)

    camera = scene.getCameraPosition()

    scale = entity.entityFields["timeLeft"] / entity.entityFields["lifeTime"]

    x =  rb.pos.x - camera.x + 15
    y =  rb.pos.y - camera.y + 15

    entity.getCanvas().coords(entity.entityFields["rect"], x, y, x + 5 * scale,y + 5 * scale)


def groundParticleInit(entity):
    entity.entityFields["rect"] = entity.window.canvas.create_rectangle(0, 0, 0, 0, outline="black", fill="black")
    entity.entityFields["lifeTime"] = 90
    entity.entityFields["timeLeft"] = entity.entityFields["lifeTime"]
