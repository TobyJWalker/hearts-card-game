from random import choice
from Player import Player
from Card import Card

# some globals used in validation
VALID_VALS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALID_SUITS = ['D', 'H', 'C', 'S']

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

# 0 difficulty is randomly generated
# 1 difficulty will try and play the lowest cards to try and avoid taking tricks
# 2 difficulty will try and play the highest card which is lower than the highest card in the trick, or highest card if no cards mathing the lead_suit is available
# 3 difficulty is similar to 2, but will try to avoid playing queen of spades unless it knows it won't win the trick, will play ace of clubs on first round and will play hearts when its not leading suit

# make a decision based on bot difficulty and current game status
def make_choice(bot, round, lead_suit, heart_broken, first_play, trick):
    
    # first generate a list of valid plays
    valid_cards = [card for card in bot.hand if is_valid_choice(card.face, bot, round, lead_suit, first_play, heart_broken if first_play else True)]

    # remove queen of spades from valid_cards if difficulty is greater than 2 and other cards are available unless there is a higher card in trick
    if bot.difficulty >= 3:

        # decide on queen of spades
        if any(card.face == 'QS' for card in valid_cards):
            if len(valid_cards) == 1 or lead_suit != 'S':
                return 'QS' # return queen of spades if its the only available card or spades isn't the lead suit
            else:
                if any(card.value > 12 and card.suit == 'spades' and lead_suit == 'S' for card in trick):
                    return 'QS' # return queen of spades if there is a more valuable card in the trick
                else:
                    valid_cards = [card for card in valid_cards if card.face != 'QS']
        
        # choose only hearts if valid and leading suit is not hearts
        if any(card.suit == 'hearts' for card in valid_cards) and lead_suit != 'H':
            valid_cards = [card for card in valid_cards if card.suit == 'hearts']
        
        # choose ace of clubs if available on first round
        if any(card.face == 'AC' for card in valid_cards):
            return 'AC'

    # handle 0 difficulty
    if bot.difficulty == 0:
        return choice(valid_cards).face
    
    # handle 1 difficulty
    elif bot.difficulty == 1:
        valid_cards.sort(key=lambda card: card.value)
        return valid_cards[0].face
    
    # handle 2 difficulty
    elif bot.difficulty >= 2:
        valid_cards.sort(key=lambda card: card.value)

        # check if cards are matching lead_suit when not first_play
        if any(card.face[-1] not in lead_suit for card in valid_cards) and not first_play:
            return valid_cards[-1].face # return the largest valued card if no lead_suit available

        else:
            # check if anyone has played a trick
            if first_play:
                return valid_cards[0].face # return smallest card if its first play of the round
            
            else:
                # get the value of the highest valued card in trick
                max_val = max([card.value for card in trick if card.face[-1] ==  lead_suit])

                # get a list of all cards below the max value
                optimal_cards = [card.face for card in valid_cards if card.value < max_val]

                # if any optimal cards are available, return biggest, else return smallest available card
                if optimal_cards != []:
                    return optimal_cards[-1]
                else:
                    return valid_cards[0].face