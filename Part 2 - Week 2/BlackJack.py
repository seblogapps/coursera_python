# "Blackjack" mini-project
# Sebastiano Tognacci

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# define starting position for player and dealer hands
DEALER_HAND_POS = (50, 200)
PLAYER_HAND_POS = (50, 400)

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define global game variables
deck = []
player_hand = []
dealer_hand = []

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        # initialize empty list 'cards' of Card objects
        self.cards = []

    def __str__(self):
        # helper function to print out hand content
        cards_str = "Hand contains"
        for i in range(len(self.cards)):
            cards_str += ' '+str(self.cards[i])
        return cards_str

    def add_card(self, card):
        # add the given 'card' to the end of the cards list
        self.cards.append(card)       

    def get_value(self):
        # init values for hand calculation:
        hand_value = 0
        card_value = 0
        any_aces = False
        # traverse cards list once
        for i in range(len(self.cards)):          
            # get value of card at index position [i]
            card_value = VALUES.get(self.cards[i].get_rank())
            # add value of the current card to the hand value
            hand_value += card_value
            # if an ace is in the hand, set flag
            if card_value == 1:
                any_aces = True
        # if no aces in the hand, return the hand_value
        if (not any_aces):
            return hand_value
        # if at least one ace in the hand:
        else:
            # if value of the hand + 10 doesn't bust, return hand_value + 10
            if hand_value + 10 <= 21:
                return hand_value + 10
            # if adding 10 we bust, return only hand_value
            else:
                return hand_value           
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        # print all the cards in the hand, spaced by 10 pixel
        # use pos to set position on the canvas
        for i in range(len(self.cards)):
            self.cards[i].draw(canvas,pos)
            pos[0] += 10 + CARD_SIZE[0]                              
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object (nested loop on suits and ranks)
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))                           

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)
        
    def deal_card(self):
        # return the last card from the deck
        return self.deck.pop()
    
    def __str__(self):
        # helper method to print the deck content
        deck_str = "Deck contains"
        for i in range(len(self.deck)):
            deck_str += ' '+str(self.deck[i])
        return deck_str

#define event handlers for buttons
# handler when deal is pressed
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    # if it's a new game, set outcome with instructions
    if not in_play:
        outcome = 'Hit or Stand?'             
    # if game is running, player lose, subtract score
    else:
        outcome = 'Retired - Hit or Stand?'
        score -= 10
    # create deck and shuffle it
    deck = Deck()         
    deck.shuffle()       
    # create player's hand
    player_hand = Hand()
    dealer_hand = Hand()
    # deals first two cards to player's
    i = 1
    while i <= 2:
        card1 = deck.deal_card()
        player_hand.add_card(card1)
        card2 = deck.deal_card()
        dealer_hand.add_card(card2)
        i += 1
        # set flag to start the game
        in_play = True


#handler when hit is pressed       
def hit():
    global in_play, score, outcome
    # if the hand is in play, hit the player (add a card to the player hand)
    if in_play:
        player_hand.add_card(deck.deal_card())
        # if player hand value > 21 player busted
        if player_hand.get_value() > 21:
            in_play = False
            score -= 10
            outcome = 'You Busted! - New Deal?'
            
def stand():
    global in_play, score, outcome   
    # hit dealer only if game is still in play
    if in_play:
        # hit another card to dealer until hand value is at least 17
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())          
        # compare to see if dealer busted:
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer busted - You won! - New Deal?'                       
            score += 10
        # if dealer not busted see if player value > dealer value
        elif player_hand.get_value() > dealer_hand.get_value():
            outcome = 'Player win! - New Deal?'          
            score += 10
        # means that dealer >= player value, so dealer win
        else:
            outcome = 'Dealer win - New Deal?'
            score -= 10
    # set in_play to false to end current game
    in_play = False

# draw handler    
def draw(canvas):
    global in_play, outcome, score   
    # draw welcome text, current score and dealer and player texts
    canvas.draw_text('Blackjack', (180, 80), 60, 'Blue')
    canvas.draw_text(('Score:  '+str(score)), (180, 140), 40, 'Cyan')
    canvas.draw_text('Dealer', (DEALER_HAND_POS[0], DEALER_HAND_POS[1] - 15), 40, 'White')
    canvas.draw_text('Player', (PLAYER_HAND_POS[0], PLAYER_HAND_POS[1] - 15), 40, 'White')
    # draw the dealer and the player hands (use positions defined as global constants)
    dealer_hand.draw(canvas, list(DEALER_HAND_POS))
    player_hand.draw(canvas, list(PLAYER_HAND_POS))   
    # draw text for outcome of current game
    canvas.draw_text(outcome, (PLAYER_HAND_POS[0], 560), 30, 'Cyan')
    # if game is running
    if in_play:              
        # hide first dealer card (hole)
        card_back_pos = DEALER_HAND_POS
        card_back_loc = (CARD_BACK_CENTER[0],CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_back_loc, CARD_SIZE, [card_back_pos[0] + CARD_CENTER[0], card_back_pos[1] + CARD_CENTER[1]], CARD_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()