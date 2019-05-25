add_library('peasycam')
import copy
from itertools import combinations 

points = set()
num_points = 10        
G = 3
shrink = .5
world = 700
barrier = 75

class PointMass:
    def __init__(self, mass, dis, vel):
        self.mass = mass
        self.dis = dis
        self.vel = vel
        self.acc = PVector(0, 0, 0)
        self.look = color(random(255), random(255), random(255))
    def set_acc(self):
        for i in points:
            if i != self:
                t = PVector(i.dis.x - self.dis.x, i.dis.y - self.dis.y, i.dis.z - self.dis.z)
                r = t.mag()
                t = t.div(r) #normal of currect force vector
                t.mult(i.mass); t.mult(G); t.div(r); t.div(r) # a = GM/x^2
                self.acc.add(t)
    def bounce(self):
        if self.dis.x <= 0 or self.dis.x >= world:
            if self.dis.y <= 0 or self.dis.y >= world:
                if self.dis.z <= 0 or self.dis.z >= world:
                    self.vel.mult(-1)
    def update(self):
        self.vel.add(self.acc)
        self.dis.add(self.vel)
        self.acc = PVector(0, 0, 0)
    def make(self):
        pushMatrix()
        noStroke()
        fill(self.look)
        translate(self.dis.x, self.dis.y, self.dis.z)
        sphere(self.mass/shrink)
        popMatrix()
    def draw(self):
        self.update()
        self.make()
    def equal(self, other):
        if self.dis == other.dis and self.vel == other.vel and self.acc == other.vel and self.mass == other.mass:
            return True
        return False
def destroy(points, s):
    for i in points:
        if i.mass == s.mass and i.look == s.look and i.dis == s.dis and i.vel == s.vel:
            points.remove(i)    
def randomDis():
    return PVector(random(barrier, world - barrier), random(barrier, world - barrier), random(barrier, world - barrier))
     
def randomVel():
    return PVector(random(25), random(25), random(25))
        
def setup():
    cam = PeasyCam(this, 1000)
    size(world, world, P3D)
    
    points.add(PointMass(random(5, 25), randomDis(), randomVel()))
    while len(points) < num_points:
        new = PointMass(random(5, 25), randomDis(), randomVel())
        include = True
        for i in points:
            if i.dis.x == new.dis.x and i.dis.y == new.dis.y and i.dis.z == new.dis.z:
                include = False
        if include:
            points.add(new)
    '''
    points.add(PointMass(100, PVector(200, 200, 200)))
    points.add(PointMass(20, PVector(250, 200, 200)))
    points[1].vel.add(PVector(0, 1, 0))
    '''
def draw():
    global points
    background(0)
    lights()
    for i in points:
        i.set_acc()
        i.draw()
        i.bounce()
    for tup in list(combinations(list(points), 2)):
        i, s = tup[0], tup[1]
        t = PVector(i.dis.x - s.dis.x, i.dis.y - s.dis.y, i.dis.z - s.dis.z)
        if abs(t.x) < 10 and abs(t.y) < 10 and abs(t.y) < 10:
            points.add(PointMass(i.mass + s.mass, i.dis.add(s.dis).div(2), i.vel.add(s.vel).div(2)))
            destroy(points, i)
            destroy(points, s)
