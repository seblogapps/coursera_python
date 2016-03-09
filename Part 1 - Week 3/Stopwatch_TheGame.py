# "StopWatch the game" mini-project
# Sebastiano Tognacci
 
import simplegui

# define global variables
timer_counter = 0
correct_stop = 0
total_stop = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    #Extract minutes
    A = (t // 600)
    #Extract tens of seconds
    B = (t // 100) % 6
    #Extract seconds in excess of tens of seconds
    C = (t // 10) % 10
    #Extract tenths of seconds
    D = (t % 10)
    #Format the output result
    return str(A)+":"+str(B)+str(C)+"."+str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def bh_start():
    #Just start the timer
    timer.start()

def bh_stop():
    global correct_stop, total_stop  
    #Only stop timer and verify if on exact second if the timer is running
    if (timer.is_running()):
        total_stop += 1
        if (timer_counter % 10 == 0):
            correct_stop += 1
        timer.stop()
    
def bh_reset():
    #Reset all counters and stop the timer
    global timer_counter, correct_stop, total_stop  
    timer.stop()
    timer_counter = 0
    correct_stop = 0
    total_stop = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    #Increase global variable that counts the time elapsed
    global timer_counter
    timer_counter += 1

# define draw handler
def draw_handler(canvas):  
    canvas.draw_text(format(timer_counter), (85 , 110), 42, 'White', 'monospace')
    canvas.draw_text(str(correct_stop)+"/"+str(total_stop), (250 , 30), 20, 'Green', 'monospace')
    
# create frame
frame = simplegui.create_frame('StopWatch', 300, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
button_start = frame.add_button('Start', bh_start, 100)
button_stop = frame.add_button('Stop', bh_stop, 100)
button_reset = frame.add_button('Reset', bh_reset, 100)

# start timer and frame
frame.start()