# "Pong" mini-project
# Sebastiano Tognacci 

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
#Initial ball position, velocity and difficulty increase
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0.0, 0.0]
ball_acc = 1.1
#Set a global default velocity for the paddle movement
paddle_default_vel = 3.0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]   
    #Set random initial value for ball velocity
    ball_vel = [random.randrange(120/60, 240/60), -random.randrange(60/60, 180/60)]
    #If direction is LEFT, invert ball_vel[0]
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    #Initial paddle position and velocity
    paddle1_pos = (HEIGHT / 2 - HALF_PAD_HEIGHT)
    paddle2_pos = (HEIGHT / 2 - HALF_PAD_HEIGHT)
    #Since paddles moves only vertically, velocity vector has one value only
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    #Initialize Player scores
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # bounce ball off vertical walls
    if ((ball_pos[1] - BALL_RADIUS) <= 0):
        ball_vel[1] = -ball_vel[1]
    elif ((ball_pos[1] + BALL_RADIUS) >= HEIGHT):
        ball_vel[1] = -ball_vel[1]
    
    # Respawn ball if collide with gutter and
    # determine whether paddle and ball collide
    # Collide on left gutter or pad:
    if ((ball_pos[0] - BALL_RADIUS) < PAD_WIDTH):
        # Collided with left pad:
        if ( (paddle1_pos < ball_pos[1]) and 
             (ball_pos[1] < paddle1_pos + PAD_HEIGHT)):
            ball_vel[0] = -ball_vel[0] * ball_acc        
        else: # Collided with gutter:
            #Increase right player score, respawn ball
            score2 += 1
            spawn_ball(RIGHT)
    # Collide on right gutter:
    elif ((ball_pos[0]+BALL_RADIUS) > WIDTH - PAD_WIDTH):
        # Collided with right pad
        if ( (paddle2_pos < ball_pos[1]) and 
             (ball_pos[1] < paddle2_pos + PAD_HEIGHT)):
            ball_vel[0] = -ball_vel[0] * ball_acc
        else: # Collided with gutter:        
            #Increase left player score, respawn ball
            score1 += 1
            spawn_ball(LEFT)    
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    # If paddle reach edge of screen, stops it (paddle 1)
    if (paddle1_pos <= 0):
        paddle1_pos = 0.0
    elif ((paddle1_pos + PAD_HEIGHT) >= HEIGHT):
        paddle1_pos = HEIGHT - PAD_HEIGHT
    # If paddle reach edge of screen, stops it (paddle 2)
    if (paddle2_pos <= 0):
        paddle2_pos = 0.0
    elif ((paddle2_pos + PAD_HEIGHT) >= HEIGHT):
        paddle2_pos = HEIGHT - PAD_HEIGHT        
        
    # draw paddles
    # Paddle 1
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos], [HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT ], PAD_WIDTH, 'White')
    # Paddle 2
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT ], PAD_WIDTH, 'White')       
    # draw scores
    score_str = str(score1) + " " + str(score2)
    canvas.draw_text(score_str.center(8), [WIDTH / 4, HEIGHT / 5], 80, 'White', 'monospace')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -paddle_default_vel
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle_default_vel
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -paddle_default_vel
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle_default_vel                 
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if (key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']):
        paddle1_vel = 0.0
    elif (key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']):
        paddle2_vel = 0.0        
  
def reset_bn_handler():
    new_game()	   

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
# Add reset button
reset_button = frame.add_button('Reset', reset_bn_handler, 150)

# start frame
new_game()
frame.start()