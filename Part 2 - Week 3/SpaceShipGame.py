# "Spaceship Game" mini-project
# Sebastiano Tognacci 

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

# constants
VELOCITY_VECTOR_REDUCTION_FACTOR = 0.1
FRICTION_CONSTANT = 0.01
MISSILE_DELTA_SPEED = 3
SHIP_RADIUS = 45
MAX_RAND_VEL = 10 # must be integer
MAX_RAND_ANG_VEL = 1 # must be integer

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        # when thrust are off, draw regular image of ship
        if not self.thrust:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        # when thrust are on, draw image of ship with flames
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # update ship position, use modular aritmethic to wrap to screen size
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update angle by angle_val value
        self.angle += self.angle_vel
        # calculate forward vector
        forward = angle_to_vector(self.angle)
        # if thrusting, add the forward vector to velocity vector
        if self.thrust:
            self.vel[0] += forward[0] * VELOCITY_VECTOR_REDUCTION_FACTOR
            self.vel[1] += forward[1] * VELOCITY_VECTOR_REDUCTION_FACTOR
        # reduce ship speed by friction constant at every update
        self.vel[0] *= (1 - FRICTION_CONSTANT)
        self.vel[1] *= (1 - FRICTION_CONSTANT)
    
    # rotate ship, param "clockwise" if True rotate ship clockwise, if False rotate anti-clockwise
    def rotate_clockwise(self,clockwise = False):
        if clockwise:          
            self.angle_vel = 0.1
        else:
            self.angle_vel = -0.1
            
    # stop ship rotation
    def rotate_stop(self):
        self.angle_vel = 0
    
    # ignite the thruster
    def thruster(self, thruster_on = False):
        self.thrust = thruster_on
        if self.thrust:       
            ship_thrust_sound.play()          
        else:
            ship_thrust_sound.rewind()
    
    # shoot missile
    def shoot(self):
        global a_missile
        # calculate current forward vector
        forward = angle_to_vector(self.angle)
        # missile position is the sum of the ship position + ship radius * forward vector
        a_missile_pos = [self.pos[0] + (SHIP_RADIUS * forward[0]),self.pos[1] + (SHIP_RADIUS * forward[1])]
        a_missile_vel = [self.vel[0] + (MISSILE_DELTA_SPEED * forward[0]), self.vel[1] + (MISSILE_DELTA_SPEED * forward[1])]       
        a_missile = Sprite(a_missile_pos, a_missile_vel, 0, 0, missile_image, missile_info, missile_sound)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # update sprite position, use modular arithmetic to wrap to screen size
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update angle by angle_val value
        self.angle += self.angle_vel

           
def draw(canvas):
    global time
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw score and lives   
    canvas.draw_text('Lives: '+str(lives), [WIDTH / 20, HEIGHT / 10], 30, 'White')
    canvas.draw_text('Score: '+str(score), [WIDTH / 1.2, HEIGHT / 10], 30, 'White')        

    # timer handler that spawns a rock    
def rock_spawner():
    # must be global to affect the rock object
    global a_rock
    a_rock_rand_pos = [WIDTH * random.random(), HEIGHT * random.random()]
    a_rock_rand_vel = [random.random() * random.randint(-MAX_RAND_VEL, MAX_RAND_VEL), random.random() * random.randint(-MAX_RAND_VEL, MAX_RAND_VEL)]   
    a_rock_rand_ang_vel = 0.1 + random.random() * random.randint(-MAX_RAND_ANG_VEL, MAX_RAND_ANG_VEL)
    a_rock = Sprite(a_rock_rand_pos, a_rock_rand_vel, 0, a_rock_rand_ang_vel, asteroid_image, asteroid_info)

# key handler
def keydown_handler(key):
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thruster(True)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate_clockwise(True)
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.rotate_clockwise(False)        

def keyup_handler(key):
    if ((key == simplegui.KEY_MAP["left"]) or (key == simplegui.KEY_MAP["right"])):
        my_ship.rotate_stop()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thruster(False)      
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
# def Ship.__init__(self, pos, vel, angle, image, info)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
# def Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, sound = None): 
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.05, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
# spaceship controls handler
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()