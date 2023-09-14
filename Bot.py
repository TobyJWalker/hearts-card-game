from random import choice
from Player import Player
from Card import Card

# some globals used in validation
VALID_VALS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALID_SUITS = ['D', 'H', 'C', 'S']

# 0 difficulty is randomly generated
# 1 difficulty will try and play the lowest cards to try and avoid taking tricks
# 2 difficulty will try and play the highest card which is lower than the highest card in the trick, or highest card if no cards mathing the lead_suit is available

# function to validate a card choice, returns True or False
def is_valid_choice(chosen, player, round, lead_suit, first_play, heart_broken=True):

    # check if choice exists
    if chosen == '':
        return False

    # choice should only be 2 or 3 characters characters
    if len(chosen) < 2 or len(chosen) > 3:
        return False
    
    # check if a valid value is entered (first character(s))
    if not any(c == chosen[:-1] for c in VALID_VALS):
        return False
    
    # check if a valid suit is entered (last character)
    if not any(c == chosen[-1] for c in VALID_SUITS):
        return False
    
    # check to see if chosen card is not in hand
    if not any(card.face == chosen for card in player.hand):
        return False
    
    # check for round 1 rules (no hearts or the queen of spades can be played)
    if round == 1 and (chosen == 'QS' or chosen[-1] == 'H'):
        return False
    
    # check to see if a card matching the lead suit is available
    if any(card.face[-1] == lead_suit for card in player.hand) and chosen[-1] not in lead_suit:
        return False
    
    # prevent playing a heart on first turn if heart_broken is specified as false
    if chosen[-1] == 'H' and first_play and not heart_broken:
        return False
    
    return True

# make a decision based on bot difficulty and current game status
def make_choice(bot, round, lead_suit, heart_broken, first_play, trick):
    
    # first generate a list of valid plays
    valid_cards = [card for card in bot.hand if is_valid_choice(card.face, bot, round, lead_suit, first_play, heart_broken if first_play else True)]

    # handle 0 difficulty
    if bot.difficulty == 0:
        return choice(valid_cards).face
    
    # handle 1 difficulty
    if bot.difficulty == 1:
        valid_cards.sort(key=lambda card: card.value)
        return valid_cards[0].face
