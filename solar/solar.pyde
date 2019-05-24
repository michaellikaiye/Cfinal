add_library('peasycam')

points = []
num_points = 15        
G = .5
shrink = 5
world = 700

class PointMass:
    def __init__(self, name, x, y, z, mass = random(5, 25)):
        self.name = name
        self.dis = PVector(x, y, z)
        self.vel = PVector(0, 0, 0)
        self.acc = PVector(0, 0, 0)
        self.mass = mass
        self.look = color(random(255), random(255), random(255))
    def set_acc(self):
        for i in points:
            if i.name != self.name:
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
    def draw(self):
        self.update()
        self.make()
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

def setup():
    cam = PeasyCam(this, 1000)
    size(world, world, P3D)
    '''
    points.append(PointMass(0, random(60, world - 60), random(60, world - 60), random(60, world - 60)))
    while len(points) < num_points:
        new = PointMass(len(points), random(60, world - 60), random(60, world - 60), random(60, world - 60))
        include = True
        for i in points:
            if i.dis.x == new.dis.x and i.dis.y == new.dis.y and i.dis.z == new.dis.z:
                include = False
        if include:
            points.append(new)
    '''
    points.append(PointMass(0, 200, 200, 200, 100))
    points.append(PointMass(1, 250, 200, 200, 20))
    points[1].vel.add(PVector(0, 1, 0))
    
def draw():
    background(0)
    lights()
    for i in points:
        i.set_acc()
        i.draw()
        i.bounce()
