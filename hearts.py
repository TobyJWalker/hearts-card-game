from random import randint

# create a card object to hold value and suit
class Card():

    # initialise the value and suit variables
    # face variable is used to display the card to the user e.g. 4H = 4 of hearts
    # a queen of spades will have value of 12 and face of QS
    # an ace of diamonds will have a value of 14 and face of AD
    def __init__(self, value, suit, face):
        self.value = value
        self.suit = suit
        self.face = ""

# create a player class which will hold hand information and points etc
class Player():

    # initialise some important variables
    def __init__(self):
        self.hand = []
        self.trick_hand = []
        self.points = 0
    
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
            