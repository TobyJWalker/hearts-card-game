from random import choice, shuffle

# some globals used in validation
VALID_VALS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VAL_CONVERSION = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
VALID_SUITS = ['D', 'H', 'C', 'S']

# welcome message function
def welcome():
    input('''\n\nWelcome to Hearts!
          
          Rules can be found here: https://playingcarddecks.com/blogs/how-to-play/hearts-game-rules
          
          Acknowledge each message (including this one) by pressing Enter key.
          Some prompts will require you to pick a card, don't forget to pick one!
          
          Good luck!\n\n''')

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
    def __init__(self, name, is_bot):
        self.hand = []
        self.trick_hand = []
        self.points = 0
        self.name = name

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
def deal_deck(players, deck):
    
    # loop 13 times, one for each card value
    for i in range(13):
        
        # add a card to each players hand
        players[0].add_card_to_hand(deck[i])
        players[1].add_card_to_hand(deck[i+13])
        players[2].add_card_to_hand(deck[i+26])
        players[3].add_card_to_hand(deck[i+39])

# find the index of the player with 2 of clubs (this will be lead player on game 1)
def find_2_clubs(players):
    index = 0

    # loop through players and return index once 2 of clubs is found
    for player in players:

        # check to see if any cards are the 2 of clubs
        if any(card.face == '2C' for card in player.hand):
            return index
        
        # increment index
        index += 1
    # retun none if 2 of clubs not found
    return None

# generate a list of indexes in the turn order of players, starting with the lead player
def get_turn_order(lead_index):
    # modulus 4 on lead index and adds to list, then repeats, adding 1 to index each time
    # a lead index of 2 for example:
    # 2 % 4 = 2, 3 % 4 = 3, 4 % 4 = 0, 5 % 4 = 1 therefore...
    # returned list = [2, 3, 0, 1]
    return [i % 4 for i in range(lead_index, lead_index+4)]

# function to display hand of passed in player
def display_hand(player):

    # format a string to display
    hand = [f'|{card.face}|' for card in player.hand]
    print(f"\nHere is your hand:\n{' '.join(hand)}\n")

# display the trick in a readable way
def display_trick(trick):
    # format a string to display
    trick_str = [f'|{card.face}|' for card in trick]
    input(f"\nCurrent Trick:\n{' '.join(trick_str)}\n")

# function to validate a card choice, returns True or False
# heart_broken variable is optional and only used on the first turn of each round to prevent heart being lead with too early
def is_valid_choice(chosen, player, round, lead_suit, heart_broken=True, show_output=True):

    # check if choice exists
    if chosen == '':
        return False

    # choice should only be 2 or 3 characters characters
    if len(chosen) < 2 or len(chosen) > 3:
        if show_output:
            input("\nChoice should consist of 2 or 3 characters, a value and suit letter")
        return False
    
    # check if a valid value is entered (first character(s))
    if not any(c == chosen[:-1] for c in VALID_VALS):
        if show_output:
            input(f"\n{chosen[:-1]} is not a valid value. Values are: 1, 2, 3...J, Q, K, A.")
        return False
    
    # check if a valid suit is entered (last character)
    if not any(c == chosen[-1] for c in VALID_SUITS):
        if show_output:
            input(f"\n{chosen[-1]} is not a valid suit. Suits are: D, S, C, H")
        return False
    
    # check to see if chosen card is not in hand
    if not any(card.face == chosen for card in player.hand):
        if show_output:
            input("\nYou do not have that card.")
        return False
    
    # check for round 1 rules (no hearts or the queen of spades can be played)
    if round == 1 and (chosen == 'QS' or chosen[:-1] == 'H'):
        if show_output:
            input("\nNo hearts or the queen of spades cannot be played on round 1.")
        return False
    
    # check to see if a card matching the lead suit is available
    if any(card.face[-1] == chosen[-1] for card in player.hand) and chosen[-1] not in lead_suit:
        if show_output:
            input("\nOne or more cards that follow suit are available, you must play a card which follows suit.")
        return False
    
    # prevent playing a heart if heart_broken is specified as false
    if chosen[-1] == 'H' and heart_broken:
        if show_output:
            input("\nCannot lead with a heart before hearts have been broken.")
        return False
    
    return True

# function to handle a player's turn, returns the card played
def play_turn(player, round, lead_suit, heart_broken=True):
    chosen = ''

    # check if player is real or a bot
    if not player.is_bot:
        # keep asking for a choice until valid
        while not is_valid_choice(chosen, player, round, lead_suit, heart_broken):

            # ask player to choose a card, set to upper for case insensitivity
            chosen = input("Enter a card to play: ").upper()
    
    # make a choice for the bot
    else:
        # keep generating a choice until valid
        while not is_valid_choice(chosen, player, round, lead_suit, heart_broken, False):
            chosen = choice(player.hand).face
    
    # check if heart_broken was already True or broken this turn
    if heart_broken or (chosen[-1] == 'H' and not heart_broken):
        return player.remove_card_from_hand(chosen), True
    
    # if hearts were not broken prior to this turn or during this turn
    else:
        return player.remove_card_from_hand(chosen), False

# main function
def main():

    welcome()

    # create some players and store in a list. 3 of them are bots
    players = [Player('You', False), Player('Bot 1', True), Player('Bot 2', True), Player('Bot 3', True)]

    # create a rounder counter
    round_num = 1
    
    # begin a loop until one player reaches 100 points
    while not any(player.points == 100 for player in players):

        # create a shuffled deck and deal
        deck = create_deck()
        shuffle(deck)
        deal_deck(players, deck)

        # another while loop until users deck is empty
        while len(players[0].hand) != 0:

            # create a 'trick' and heart_broken variable
            current_trick = []
            heart_broken = False

            # display user's hand
            display_hand(players[0])

            # check for game 1, and calculate lead player index if so
            if round_num == 1:
                lead_index = find_2_clubs(players)

            # calculate the order of play using lead index
            player_order = get_turn_order(lead_index)

            # loop through each player to do their turn
            for current in player_order:

                # check to see if player 1's turn and game 1
                if round_num == 1 and lead_index == current:
                    # automatically play 2 of clubs for lead player
                    print(f'\n{players[current].name} played 2 of clubs.')
                    
                    for card in players[current].hand:
                        if card.face == '2C':
                            current_trick.append(card)
                            players[current].hand.remove(card)
                    
                    # set the lead suit to clubs
                    lead_suit = 'C'
                
                # handle first turn slightly differently to others
                elif lead_index == current:
                    # play the turn, but check if heart is broken only on this first player
                    played_card, heart_broken = play_turn(players[current], round_num, 'DHCS', heart_broken)

                    # assign the lead suit and add card to trick
                    lead_suit = played_card.face[-1]
                    current_trick.append(played_card)

                    # display a message in readable, clear format using VAL_CONVERSION to translate card value to proper format
                    print(f"\n{players[current].name} played {VAL_CONVERSION[played_card.value-1]} of {played_card.suit}")
                
                # play by normal rules for every other play
                else:
                    # play the turn and add card to trick
                    played_card, heart_broken = play_turn(players[current], round_num, 'DHCS', heart_broken)
                    current_trick.append(played_card)

                    # display a message in readable, clear format using VAL_CONVERSION to translate card value to proper format
                    print(f"\n{players[current].name} played {VAL_CONVERSION[played_card.value-1]} of {played_card.suit}")
                    
                display_trick(current_trick)
            
            # calculate which card is the highest value and store the index
            highest_card_index = 0
            highest_card_value = 0

            for card in current_trick:
                if card.face[-1] == lead_suit and card.value > highest_card_value:
                    highest_card_value = card.value
                    highest_card_index = current_trick.index(card)
            
            # give the trick to the player with the highest value in the lead suit
            players[player_order[highest_card_index]].add_trick_cards(current_trick)

            # output a message to display who won the trick
            input(f"\n{players[player_order[highest_card_index]].name} won this trick.\n")

            # set the new lead_index and increment round number
            lead_index = player_order[highest_card_index]
            round_num += 1

                

main()