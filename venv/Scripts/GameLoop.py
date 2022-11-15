from EntityBehaviour import *

WINDOW_DIMENSIONS = (1980, 1080)

Window = GameWindow(WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1])
CameraPosition = Vector2(0, 0)


def createVine(posX, posY, sepX, sepY, noOfChains):
    boxes = []

    for i in range(noOfChains):
        box = Entity([RigidBody(
            Vector2(posX + i * sepX, posY + i * sepY),
            Vector2(0, 0), False, 0.002, 0.001), VerletBody(
            Vector2(posX + i * sepX, posY + i * sepY),
            True if i == 0 else False)])

        box.onUpdate += lambda e=box: sqaureEntityUpdate(e)
        box.onInit += lambda e=box: sqaureEntityInitialise(e)

        Window.entityHost.addEntity(box)
        if i > 0:
            Window.entityHost.systems["VerletBody"].bindPoints(boxes[i - 1], box, math.sqrt(sepX * sepX + sepY * sepY))
        boxes.append(box)


def createTerrain(posX, posY, width, height):
    terrain = Entity([RigidBody(Vector2(posX, posY), Vector2(0, 0), False), Body2D(Vector2(width, height))])
    terrain.onUpdate += lambda e=terrain: sqaureEntityUpdate(e)
    terrain.onInit += lambda e=terrain: sqaureEntityInitialise(e)
    Window.entityHost.addEntity(terrain)


player = Entity([RigidBody(Vector2(10, 10), Vector2(0, 0), drag=0.998), Body2D(Vector2(10, 10))])
player.onUpdate += lambda e=player: sqaureEntityUpdate(e)
player.onUpdate += lambda e=player: playerMovement(e)
player.onInit += lambda e=player: sqaureEntityInitialise(e)
player.onUpdate += lambda e=player: playerInit(e)

Window.entityHost.addEntity(player)

createTerrain(0, 100, 100, 300)
createTerrain(0, 400, 800, 100)
createTerrain(700, 100, 100, 300)

createVine(500, 50, 20, 20, 6)
createVine(300, 50, 40, 30, 6)

Window.win.bind('<Key>', on_event)
Window.win.bind("<KeyRelease>", on_release)

Window.update()
Window.win.mainloop()
