import math

from MyMath import *


class EntityHost:
    def __init__(self, window):
        self.entities = []
        self.window = window
        self.onInit()

        self.systems = {}
        self.appendSystem("VerletBody", VerletSystem())
        self.appendSystem("Body2D", CollisionSystem())

    def queryEntity(self, entity):
        for module in entity.modules.keys():
            if module in self.systems.keys():
                self.systems[module].appendEntity(entity)

    def appendSystem(self, name, system):
        system.parent = self
        self.systems[name] = system

    def update(self):
        for entity in self.entities:
            entity.update()

        for key in self.systems:
            self.systems[key].update()

    def addEntity(self, entity):
        entity.window = self.window
        entity.onInit(entity)
        self.entities.append(entity)

        self.queryEntity(entity)

    def onInit(self):
        pass


class EntityModifier:
    def __init__(self):
        self.entity = None

    def onInit(self):
        pass

    def onUpdate(self, entity):
        pass


class EntitySystem:
    def __init__(self):
        self.entities = []
        self.parent = None

    def onInit(self):
        pass

    def update(self):
        pass

    def appendEntity(self, entity):
        self.entities.append(entity)


class VerletSystem(EntitySystem):
    def __init__(self):
        self.constraints = []
        self.lines = {}
        EntitySystem.__init__(self)

    def appendEntity(self, entity):
        self.entities.append(entity)

    def updatePoints(self):
        for entity in self.entities:
            vb = entity.getModule("VerletBody")
            if not vb.isStatic:
                rb = entity.getModule("RigidBody")

                rb.vel.x = (rb.pos.x - vb.oldPos.x)
                rb.vel.y = (rb.pos.y - vb.oldPos.y)

                vb.oldPos.x = rb.pos.x
                vb.oldPos.y = rb.pos.y

                rb.pos.x += rb.vel.x
                rb.pos.y += rb.vel.y

                rb.pos.y += rb.mass

    def bindPoints(self, p1, p2, length):
        self.constraints.append(Constraint((p1, p2), length))

        p1rb = p1.getModule("RigidBody")
        p2rb = p2.getModule("RigidBody")

        self.lines[(p1, p2)] = self.parent.window.canvas.create_line(p1rb.pos.x, p1rb.pos.y, p2rb.pos.x, p2rb.pos.y,
                                                                     fill="white")

    def updateConstraints(self):
        for constraint in self.constraints:

            p1 = constraint.points[0]
            p2 = constraint.points[1]

            p1rb = p1.getModule("RigidBody")
            p1vb = p1.getModule("VerletBody")

            p2rb = p2.getModule("RigidBody")
            p2vb = p2.getModule("VerletBody")

            dx = p2rb.pos.x - p1rb.pos.x
            dy = p2rb.pos.y - p1rb.pos.y

            currentLength = math.sqrt(dx * dx + dy * dy)
            deltaLength = currentLength - constraint.length
            perc = deltaLength / currentLength * 0.5

            offsetX = perc * dx
            offsetY = perc * dy

            if not p1vb.isStatic:
                p1rb.pos.x += offsetX
                p1rb.pos.y += offsetY

            if not p2vb.isStatic:
                p2rb.pos.x -= offsetX
                p2rb.pos.y -= offsetY

            win = self.parent.window
            cPos = win.scene.cameraPosition

            win.canvas.coords(self.lines[(p1, p2)], p1rb.pos.x - cPos.x, p1rb.pos.y - cPos.y, p2rb.pos.x - cPos.x, p2rb.pos.y - cPos.y)

    def update(self):
        self.updatePoints()
        self.updateConstraints()


class CollisionSystem(EntitySystem):
    def __init__(self):
        EntitySystem.__init__(self)

    def broadPhase(self):
        for bodies in self.entities:
            bodies.getModule("Body2D").colliding = False

        for body1 in self.entities:
            for body2 in self.entities:
                if body1 != body2 and rectIntersecting(body1, body2):
                    AABBresolution(body1, body2)

    def update(self):
        self.broadPhase()
        pass


class RigidBody(EntityModifier):
    def __init__(self, pos=Vector2(0, 0), vel=Vector2(0, 0), ifSimulated=True, mass=0.001, drag=1):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.drag = drag
        self.ifSimulated = ifSimulated
        EntityModifier.__init__(self)

    def onUpdate(self, entity):
        if self.ifSimulated:
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y
            self.vel.y += self.mass

            self.vel.x *= self.drag
            self.vel.y *= self.drag
        pass


class VerletBody(EntityModifier):
    def __init__(self, oldPos, isStatic=False, hasGravity=True):
        self.oldPos = oldPos
        self.isStatic = isStatic
        self.hasGravity = hasGravity
        EntityModifier.__init__(self)


class Body2D(EntityModifier):
    def __init__(self, bounds):
        self.bounds = bounds
        self.colliding = False
        EntityModifier.__init__(self)

    def width(self):
        return self.bounds.x

    def height(self):
        return self.bounds.y

    def right(self, entity):
        return entity.getModule("RigidBody").pos.x + self.bounds.x

    def bottom(self, entity):
        return entity.getModule("RigidBody").pos.y + self.bounds.y


class Constraint:
    def __init__(self, points, length):
        self.points = points
        self.length = length


class Entity:
    def __init__(self, modules):
        self.window = None

        self.entityFields = {}
        self.modules = {}

        self.onUpdate = Event()
        self.onInit = Event()

        for module in modules:
            self.modules[module.__class__.__name__] = module

    def getCanvas(self):
        return self.window.canvas

    def getModule(self, moduleName):
        return self.modules[moduleName]

    def hasModule(self, moduleName):
        return moduleName in self.modules

    def update(self):
        for key in self.modules:
            self.modules[key].onUpdate(self)

        self.onUpdate(self)
