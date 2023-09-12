from Card import Card

# create a player class which will hold hand information and points etc
class Player():
    # initialise some important variables
    def __init__(self, name, is_bot):
        self.hand = []
        self.trick_hand = []
        self.points = 0
        self.name = name
        self.is_bot = is_bot
    
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
        self.trick_hand = []
    
    # get trick heart count
    def get_trick_heart_count(self):
        count = 0

        for card in self.trick_hand:
            if card.suit == 'hearts':
                count += 1
        
        return count