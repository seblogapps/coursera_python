# "Memory Card Game" mini-project
# Sebastiano Tognacci

import simplegui
import random

# Define constants (can resize canvas if needed)
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 100
CARD_WIDTH = CANVAS_WIDTH / 16.0
CARD_HEIGHT = CANVAS_HEIGHT
FONT_SIZE = CARD_WIDTH 
LINE_WIDTH = CARD_WIDTH - 1
# Define global variables
deck1 = range(8)
deck2 = range(8)
# Concatenate the two deck of cards
deck = deck1 + deck2
# List to store the last two selected cards 
selected_card = [None] * 2
# List to store the last two selected cards indexes
selected_card_idx = [None] * 2

# helper function to initialize globals
def new_game():
    global deck, game_state, turn, exposed
    # Shuffle deck
    random.shuffle(deck)
    # Card exposed list (True/False), initialize all to face down
    exposed = [False]*len(deck)
    # Game state (0 = no card flipped,1 = one card flipped ,2 = two cards flipped)
    game_state = 0
    # Initial turn count
    turn = 0  
    
# define event handlers
def mouseclick(pos):
    global game_state, selected_cards, selected_cards_idx, turn    
    # Translate pos to index in the deck:
    pos_index = pos[0] // CARD_WIDTH
    # First click, flip one card face up
    if game_state == 0:       
        exposed[pos_index] = True
        selected_card[0] = deck[pos_index]
        selected_card_idx[0] = pos_index 
        game_state = 1
    # Second click, flip second card face up
    elif game_state == 1:
        if not exposed[pos_index]:
            exposed[pos_index] = True
            selected_card[1] = deck[pos_index]
            selected_card_idx[1] = pos_index
            game_state = 2
            turn += 1
    # Third click, check if cards paired, flip one card
    else:
        # Flip one card, 
        if not exposed[pos_index]:
            # If previously two selected cards are not paired, flip them face down
            if selected_card[0] is not selected_card[1]:   
                exposed[selected_card_idx[0]] = exposed[selected_card_idx[1]] = False           
            # Flip card, store his value and index
            exposed[pos_index] = True
            selected_card[0] = deck[pos_index]
            selected_card_idx[0] = pos_index
            game_state = 1        
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    # Update current turn text
    label.set_text('Turns = '+str(turn))
    # First position where to draw first card and first box (made with a thick line)
    card_x_pos = CARD_WIDTH // 5 #10 
    box_x_pos = CARD_WIDTH // 2 #25
    for card_index in range(len(deck)):
        #Draw card face up or face down based on exposed list
        if exposed[card_index]:
            canvas.draw_text(str(deck[card_index]), (card_x_pos,CARD_HEIGHT * 0.7), FONT_SIZE, 'White')        
        else: # Flip card down (draw green rectangle)         
            canvas.draw_line((box_x_pos, 0), (box_x_pos, CARD_HEIGHT), LINE_WIDTH, 'Green')
        # Move positions of elements 50 pixel on the right of last position
        card_x_pos+=CARD_WIDTH 
        box_x_pos+=CARD_WIDTH

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()