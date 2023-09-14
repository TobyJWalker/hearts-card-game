from random import choice
from Player import Player
from Card import Card
from hearts import is_valid_choice

# 0 difficulty is randomly generated
# 1 difficulty will try and play the lowest cards to try and avoid taking tricks
# 2 difficulty will try and play the highest card which is lower than the highest card in the trick

# make a decision based on bot difficulty and current game status
def make_choice(bot, round, lead_suit, heart_broken, first_play, trick):
    
    # first generate a list of valid plays
    valid_cards = [card for card in bot.hand if is_valid_choice(card.face, bot, round, lead_suit, first_play, heart_broken, False)]

    # handle 0 difficulty
    if bot.difficulty == 0:
        return choice(valid_cards).face
    
    # handle 1 difficulty
    if bot.difficulty == 1:
        valid_cards.sort(key=lambda card: card.value)
        return valid_cards[0]