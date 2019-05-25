add_library('peasycam')
import copy
from itertools import combinations 

points = set()
num_points = 18       
G = 10
shrink = 20
world = 2500
speed = 50

def randomDis():
    return PVector(float(random(world) - world/2), float(random(world) - world/2), float(random(world) - world/2))
     
def randomVel():
    return PVector(float(random(speed)), float(random(speed)), float(random(speed)))

class PointMass:
    def __init__(self, mass, dis, vel):
        self.mass = mass
        self.dis = dis
        self.vel = vel
        self.acc = PVector(0.0, 0.0, 0.0)
        self.look = color(random(255), random(255), random(255))
    def set_acc(self):
        for i in points:
            if i != self:
                t = PVector(i.dis.x - self.dis.x, i.dis.y - self.dis.y, i.dis.z - self.dis.z)
                r = t.mag()
                t = t.div(r) #normal of currect force vector
                t.mult(i.mass); t.mult(G); t.div(r); t.div(r) # a = GM/x^2
                self.acc.add(t)
    def boundary_collision(self):
        if self.dis.x > world-(self.mass/shrink):
            self.dis.x = world-(self.mass/shrink)
            self.vel.x *= -1
        elif self.dis.x < (self.mass/shrink)-world:
            self.dis.x = (self.mass/shrink)-world
            self.vel.x *= -1
        elif self.dis.y > world-(self.mass/shrink):
            self.dis.y = world-(self.mass/shrink)
            self.vel.y *= -1
        elif self.dis.y < (self.mass/shrink)-world:
            self.dis.y = (self.mass/shrink)-world
            self.vel.y *= -1
        elif self.dis.z > world-(self.mass/shrink):
            self.dis.z = world-(self.mass/shrink)
            self.vel.z *= -1
        elif self.dis.z < (self.mass/shrink)-world:
            self.dis.z = (self.mass/shrink)-world
            self.vel.z *= -1
    def update(self):
        self.vel.add(self.acc)
        self.dis.add(self.vel)
        self.acc = PVector(0.0, 0.0, 0.0)
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

def combine():
    for tup in list(combinations(list(points), 2)):
        i, s = tup[0], tup[1]
        t = PVector(i.dis.x - s.dis.x, i.dis.y - s.dis.y, i.dis.z - s.dis.z)
        r = (i.mass/shrink + s.mass/shrink)/2.5
        if abs(t.x) < r and abs(t.y) < r and abs(t.y) < r:
            points.add(PointMass(i.mass + s.mass, i.dis.add(s.dis).div(2), i.vel.add(s.vel).div(2)))
            destroy(points, i)
            destroy(points, s)

def grids():
    stroke(255)
    line(world,world,world,world,world,-world)
    line(world,world,-world,world,-world,-world)
    line(world,-world,-world,world,-world,world)
    line(world,-world,world,world,world,world)
    line(-world,world,world,-world,world,-world)
    line(-world,world,-world,-world,-world,-world)
    line(-world,-world,-world,-world,-world,world)
    line(-world,-world,world,-world,world,world)
    line(-world,world,world,world,world,world)
    line(-world,world,-world,world,world,-world)
    line(-world,-world,world,world,-world,world)
    line(-world,-world,-world,world,-world,-world)

def create_chaos():
    points.add(PointMass(random(100, 500), randomDis(), randomVel()))
    while len(points) < num_points:
        new = PointMass(random(100, 500), randomDis(), randomVel())
        include = True
        for i in points:
            if i.dis.x == new.dis.x and i.dis.y == new.dis.y and i.dis.z == new.dis.z:
                include = False
        if include:
            points.add(new)

def create_orbit():
    m1, m2, x1, v = 1000.0, 1000.0, PVector(0.0,0.0,0.0), 5.0
    r = G*m1/(v*v)
    print(r)
    points.add(PointMass(m1, x1, PVector(0.0,0.0,0.0)))
    points.add(PointMass(m2, PVector(x1.x+r, x1.y, x1.z), PVector(0.0, v, 0.0)))
            
def setup():
    fullScreen(P3D)
    perspective(PI/3, float(width)/float(height), 1, 100000);  
    cam = PeasyCam(this, world/2)
    create_orbit()

def draw():
    global points
    background(0)
    lights()
    
    grids()
    #combine()
    for i in points:
        i.set_acc()
        i.draw()
        i.boundary_collision()
