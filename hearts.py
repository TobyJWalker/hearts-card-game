from random import randint, shuffle

# create a card object to hold value and suit
class Card():

    # initialise the value and suit variables
    # face variable is used to display the card to the user e.g. 4H = 4 of hearts
    # a queen of spades will have value of 12 and face of QS
    # an ace of diamonds will have a value of 14 and face of AD
    def __init__(self, value, suit, face):
        self.value = value
        self.suit = suit
        self.face = face

# create a player class which will hold hand information and points etc
class Player():

    # initialise some important variables
    def __init__(self, is_bot):
        self.hand = []
        self.trick_hand = []
        self.points = 0

        # is_bot determines if prompts are printed to console or choices are generated
        self.is_bot = is_bot
    
    # count the value of the trick hand
    def calculate_trick_value(self):
        
        # running total of points
        total = 0

        # bool value to check if player "shot the moon"
        shot_the_moon = False

        # loop through trick hand
        for card in self.trick_hand:

            # if card is a hearts, add 1 point
            if card.suit == 'hearts':
                total += 1
            
            # if card is a queen of spades, add 13 points
            if card.face == 'QS':
                total += 13
            
        # check if player shot the moon (got all hearts and queen of spades)
        if total == 26:
            total = 0
            shot_the_moon = True
            
        # return the calculated values
        return total, shot_the_moon
    
    # add a card to the deck
    def add_card_to_deck(self, card):
        self.hand.append(card)

# function to create the deck
def create_deck():

    # create an empty deck
    deck = []

    # create a variable to hold a dictionary of suits and their symbol
    suits = {'hearts': 'H', 'clubs': 'C', 'spades': 'S', 'diamonds': 'D'}

    # loop through suits and add all cards to deck
    for suit in suits.keys():
        
        # loop through all values
        for i in range(2, 15):

            # check for jack, queen, king or ace first
            if i == 11:
                deck.append(Card(i, suit, f'J{suits[suit]}'))
            elif i == 12:
                deck.append(Card(i, suit, f'Q{suits[suit]}'))
            elif i == 13:
                deck.append(Card(i, suit, f'K{suits[suit]}'))
            elif i == 14:
                deck.append(Card(i, suit, f'A{suits[suit]}'))
            else:
                deck.append(Card(i, suit, f'{i}{suits[suit]}'))
    
    # return the deck
    return deck

# deal the deck between 4 players
def deal_deck(player_1, player_2, player_3, player_4, deck):
    
    # loop 13 times, one for each card value
    for i in range(13):
        
        # add a card to each players hand
        player_1.add_card_to_deck(deck[i])
        player_2.add_card_to_deck(deck[i+13])
        player_3.add_card_to_deck(deck[i+26])
        player_4.add_card_to_deck(deck[i+39])

