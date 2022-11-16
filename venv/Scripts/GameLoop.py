from EntityBehaviour import *

WINDOW_DIMENSIONS = (1280, 720)

Window = GameWindow(WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1])
CameraPosition = Vector2(0, 0)

HomeScreen = PhotoImage(file='HomeScreen.png').zoom(2, 2)


def createVine(posX, posY, sepX, sepY, noOfChains, scene):
    boxes = []

    for i in range(noOfChains):
        box = Entity([RigidBody(
            Vector2(posX + i * sepX, posY + i * sepY),
            Vector2(0, 0), False, 0.002, 0.001), VerletBody(
            Vector2(posX + i * sepX, posY + i * sepY),
            True if i == 0 else False)])

        box.onUpdate += lambda e=box: sqaureEntityUpdate(e, scene.cameraPosition)
        box.onInit += lambda e=box: sqaureEntityInitialise(e)

        if i > 0:
            scene.entityHost.systems["VerletBody"].bindPoints(boxes[i - 1], box, math.sqrt(sepX * sepX + sepY * sepY))
            if(i == noOfChains - 1):
                box.onInit += lambda e=box: tipIndicatorsInit(e)
                box.onUpdate += lambda e=box: tipIndicatorsUpdate(e, scene.cameraPosition)

        scene.entityHost.addEntity(box)
        boxes.append(box)

    scene.vines.append((boxes[0], boxes[noOfChains - 1]))

def createTerrain(posX, posY, width, height, scene):
    terrain = Entity([RigidBody(Vector2(posX, posY), Vector2(0, 0), False), Body2D(Vector2(width, height))])
    terrain.onUpdate += lambda e=terrain: sqaureEntityUpdate(e, scene.cameraPosition)
    terrain.onInit += lambda e=terrain: sqaureEntityInitialise(e)
    scene.entityHost.addEntity(terrain)


class MainMenu(Scene):
    def onStart(self):
        button = Button(Window.canvas, font="Times 20 italic bold", text="Start",
                        command=lambda w=Window: w.nextScene(Level1))
        button.place(x=0, y=0)

        Window.canvas.create_image(0, 0, anchor=NW, image=HomeScreen)
        Window.addWidget(button)


class Level1(Scene):
    def __init__(self, win):
        self.vines = []
        Scene.__init__(self, win)

    def onStart(self):
        player = Entity([RigidBody(Vector2(10, 10), Vector2(0, 0), drag=0.998), Body2D(Vector2(10, 10))])
        player.onUpdate += lambda e=player: sqaureEntityUpdate(e, self.cameraPosition)
        player.onUpdate += lambda e=player: playerMovement(e)
        player.onInit += lambda e=player: sqaureEntityInitialise(e)
        player.onUpdate += lambda e=player: playerInit(e)

        self.entityHost.addEntity(player)

        createTerrain(0, 100, 100, 300, self)
        createTerrain(0, 400, 800, 100, self)
        createTerrain(700, 100, 100, 300, self)

        createVine(500, 50, 20, 20, 6, self)
        createVine(300, 50, 40, 30, 6, self)

        self.cameraPosition.y = 1280



    def update(self):
        self.cameraPosition.y *= 0.998


Window.nextScene(MainMenu)

Window.win.bind('<Key>', on_event)
Window.win.bind("<KeyRelease>", on_release)

Window.update()
Window.win.mainloop()
