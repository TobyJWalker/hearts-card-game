from Card import Card
from math import floor

VAL_CONVERSION = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# create a player class which will hold hand information and points etc
class Player():
    # initialise some important variables
    def __init__(self, name, is_bot):
        self.hand = []
        self.trick_hand = []
        self.points = 0
        self.name = name
        self.is_bot = is_bot
        self.difficulty = 0
        self.tricks_won = 0
    
    # add a card to the hand
    def add_card_to_hand(self, card):
        self.hand.append(card)
    
    # function to remove a card
    def remove_card_from_hand(self, face):
        # loop through the players cards and return the chosen one whilst removing it from the hand
        for card in self.hand:
            if card.face == face:
                self.hand.remove(card)
                return card
        return None
    
    # function to add trick cards to list
    def add_trick_cards(self, trick):
        self.trick_hand += trick

    # reset the trick list
    def reset_trick_hand(self):
        self.trick_hand.clear()
    
    # get trick heart count
    def get_trick_heart_count(self):
        count = 0

        for card in self.trick_hand:
            if card.suit == 'hearts':
                count += 1
        
        return count
    
    # check if any of the trick cards is a queen of spades
    def has_queen_spades(self):
        return any(card.face == 'QS' for card in self.trick_hand)
    
    # check to see if shot to moon
    def shot_the_moon(self):
        return self.has_queen_spades() and (self.get_trick_heart_count() >= 13)
    
    # display the users hand
    def display_hand(self):
        print("\nHere is your hand:\n")

        for card in self.hand:
            print(f"{card.face}{' '*(4-len(card.face))}: {VAL_CONVERSION[card.value - 2]} of {card.suit}")
        
        print('''
Type --help for a list of commands
''')
    
    # clear the users hand
    def clear_hand(self):
        self.hand.clear()
    
    # set a bots difficulty
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty