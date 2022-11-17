
class Event(object):
    def __init__(self):
        self.methods = []

    def __iadd__(self, method):
        self.methods.append(method)
        return self

    def __isub__(self, handler):
        self.methods.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for method in self.methods:
            method(*args, **keywargs)


class Vector2:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, vec):
        self.x += vec.x
        self.y += vec.y
        return self

    def __sub__(self, vec):
        self.x -= vec.x
        self.y -= vec.y
        return self


def rectIntersecting(r1, r2):
    pos1 = r1.getModule("RigidBody").pos
    pos2 = r2.getModule("RigidBody").pos

    bounds1 = r1.getModule("Body2D").bounds
    bounds2 = r2.getModule("Body2D").bounds

    return pos1.x < pos2.x + bounds2.x and \
           pos1.x + bounds1.x > pos2.x and \
           pos1.y < pos2.y + bounds2.y and \
           pos1.y + bounds1.y > pos2.y

def create_circle(x, y, r, canvas, color):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=color)

def edit_circle(x, y, r, circle, canvas):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvas.coords(circle, x0, y0, x1, y1)

def AABBresolution(body1, body2):
    col1 = body1.getModule("Body2D")
    col2 = body2.getModule("Body2D")

    rb1 = body1.getModule("RigidBody")
    rb2 = body2.getModule("RigidBody")

    if rb2.ifSimulated or not rb1.ifSimulated: return

    lastPosX1 = rb1.pos.x - rb1.vel.x * 9.81
    lastPosY1 = rb1.pos.y - rb1.vel.y * 9.81

    resolution = Vector2(0, 0)

    if lastPosY1 + col1.height() > rb2.pos.y and lastPosY1 < rb2.pos.y + col2.height():
        if lastPosX1 > rb2.pos.x + col2.width() / 2:
            resolution = Vector2(rb2.pos.x + col2.width() - rb1.pos.x, 0)
            rb1.vel.x = 0
            col1.colliding = True
        if lastPosX1 + col1.width() < rb2.pos.x + col2.width() / 2:
            resolution = Vector2(rb2.pos.x - (rb1.pos.x + col1.width()), 0)
            rb1.vel.x = 0
            col1.colliding = True

    if lastPosX1 < rb2.pos.x + col2.width() and lastPosX1 + col1.width() > rb2.pos.x:
        if lastPosY1 > rb2.pos.y + col2.height() / 2:
            resolution = Vector2(0, rb2.pos.y + col2.height() - rb1.pos.y)
            rb1.vel.y = 0
            col1.colliding = True
        if lastPosY1 + col1.height() < rb2.pos.y + col2.height() / 2:
            resolution = Vector2(0, rb2.pos.y - (rb1.pos.y + col1.height()))
            rb1.vel.y = 0
            col1.colliding = True

    rb1.pos += resolution