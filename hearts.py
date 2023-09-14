from random import shuffle
from Bot import make_choice
from Player import Player
from Card import Card
import os
import time

# some globals used in validation
VAL_CONVERSION = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
VALID_VALS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALID_SUITS = ['D', 'H', 'C', 'S']

# clear function to clear terminal
clear = lambda: os.system("clear")

# welcome message function
def welcome():
    input('''\n\nWelcome to Hearts!

Rules can be found here: https://playingcarddecks.com/blogs/how-to-play/hearts-game-rules

You will be playing against 3 other bots.

Acknowledge each message (including this one) by pressing Enter key.
Some prompts will require you to pick a card, don't forget to pick one!

Good luck!\n\n''')

# ask the user for difficulty and set each bot to the chosen difficulty level
def select_difficulty(players):
    # initialise difficulty as a negative number as 0 will be min difficulty
    difficulty = -1

    # keep asking user for a valid difficulty until one is entered
    while difficulty not in range(3):
        try:
            difficulty = int(input('''Here are available difficulty options:

0. Random
1. Basic
2. Intermediate

Enter your choice here: '''))
        except:
            print("\nDifficulty entered must be a number.\n")
    
    # loop through players and assign the chosen difficulty
    for player in players:
        player.set_difficulty(difficulty)

# function to create the deck
def create_deck():
    # create an empty deck
    deck = []

    # create a variable to hold a dictionary of suits and their symbol
    suits = {'hearts': 'H', 'clubs': 'C', 'spades': 'S', 'diamonds': 'D'}

    # loop through suits and add all cards to deck
    for suit in suits.keys():
        
        # loop through all card values and add each suit to the deck
        for i in range(2, 15):
            deck.append(Card(i, suit, f'{VALID_VALS[i-2]}{suits[suit]}'))
    return deck

# check a players hand to make sure they don't have all hearts and/or queen of spades in their hand
def validate_hands(players):
    hands_valid = True
    # loop through players and check their hands
    for player in players:
        if not any(card.suit != 'hearts' and card.face != 'QS' for card in player.hand) or len(player.hand) == 0:
            player.display_hand()
            hands_valid = False
            break
    # clear everyones hand for re-deal if any are invalid
    if not hands_valid:
        for player in players:
            player.clear_hand()

    return hands_valid

# deal the deck between 4 players
def deal_deck(players, deck):
    # include validation check
    while not validate_hands(players):
        # shuffle the deck
        shuffle(deck)

        # loop 13 times, one for each card value
        for i in range(13):
            # add a card to each players hand
            players[0].add_card_to_hand(deck[i])
            players[1].add_card_to_hand(deck[i+13])
            players[2].add_card_to_hand(deck[i+26])
            players[3].add_card_to_hand(deck[i+39])
    
    # loop through player hands and sort them by value
    for player in players:
        player.hand.sort(reverse=True, key=lambda card: (card.suit, card.value))

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

# display the trick in a readable way
def display_trick(trick, trick_players):
    print('')
    # loop through trick cards and print with the person who played that card
    for player in enumerate(trick_players):
        print(f"{player[1]}{' '*(6-len(player[1]))}: {VAL_CONVERSION[trick[player[0]].value - 2]} of {trick[player[0]].suit}")
    print('')

# function to validate a card choice, returns True or False
# heart_broken variable is optional and only used on the first turn of each round to prevent heart being lead with too early
def is_valid_choice(chosen, player, round, lead_suit, first_play, heart_broken=True, show_output=True):

    # check if a command has been entered first
    if chosen[:2] == '--':
        return chosen
    
    # check if choice exists
    if chosen == '':
        return False

    # choice should only be 2 or 3 characters characters
    if len(chosen) < 2 or len(chosen) > 3:
        if show_output:
            print("\nChoice should consist of 2 or 3 characters, a value and suit letter")
        return False
    
    # check if a valid value is entered (first character(s))
    if not any(c == chosen[:-1] for c in VALID_VALS):
        if show_output:
            print(f"\n{chosen[:-1]} is not a valid value. Values are: 1, 2, 3...J, Q, K, A.")
        return False
    
    # check if a valid suit is entered (last character)
    if not any(c == chosen[-1] for c in VALID_SUITS):
        if show_output:
            print(f"\n{chosen[-1]} is not a valid suit. Suits are: D, S, C, H")
        return False
    
    # check to see if chosen card is not in hand
    if not any(card.face == chosen for card in player.hand):
        if show_output:
            print("\nYou do not have that card.")
        return False
    
    # check for round 1 rules (no hearts or the queen of spades can be played)
    if round == 1 and (chosen == 'QS' or chosen[-1] == 'H'):
        if show_output:
            print("\nNo hearts or the queen of spades cannot be played on round 1.")
        return False
    
    # check to see if a card matching the lead suit is available
    if any(card.face[-1] == lead_suit for card in player.hand) and chosen[-1] not in lead_suit:
        if show_output:
            print("\nOne or more cards that follow suit are available, you must play a card which follows suit.")
        return False
    
    # prevent playing a heart on first turn if heart_broken is specified as false
    if chosen[-1] == 'H' and first_play and not heart_broken:
        if show_output:
            print("\nCannot lead with a heart before hearts have been broken.")
        return False
    
    return True

# function to display current game scores
def display_game_scores(players):
    clear
    input(f'''\n
---------------------------------------------------------
Here are the current game scores:

{players[0].name}: {players[0].points}
{players[1].name}: {players[1].points}
{players[2].name}: {players[2].points}
{players[3].name}: {players[3].points}

Press Enter to continue.
---------------------------------------------------------
''')
    clear

# run a specified command
def run_command(cmd, players):

    # help command
    if cmd == '--help':
        input('''
Available commands are:

--tricks      : Displays a list of players and how many tricks they have taken
--scores      : Displays a leaderboard of the current scores
--hand        : Displays your hand
--shootthemoon: Adds all hearts and queen of spades to trick hand (Debugging)

Press Enter to continue.
''')
    
    # scores command
    elif cmd == '--scores':
        display_game_scores(players)
    
    # tricks command
    elif cmd == '--tricks':
        input(f'''\n
Here's the current trick distribution:

{players[0].name}{' ' * (4 - len(players[0].name))}: {players[0].get_trick_count()})
{players[1].name}{' ' * (4 - len(players[1].name))}: {players[1].get_trick_count()})
{players[2].name}{' ' * (4 - len(players[2].name))}: {players[2].get_trick_count()})
{players[3].name}{' ' * (4 - len(players[3].name))}: {players[3].get_trick_count()})

Press Enter to continue.\n''')
    
    # hand command
    elif cmd == '--hand':
        for player in players:
            if not player.is_bot:
                player.display_hand()
    
    # shootthemoon command
    elif cmd == '--shootthemoon':
        for player in players:
            if not player.is_bot:
                for i in range(2, 15):
                    player.trick_hand.append(Card(i, 'hearts', f'{VALID_VALS[i-2]}H'))
                player.trick_hand.append(Card(12, 'spades', 'QS'))
    
    else:
        print('\nCommand not found.\n')

# function to handle a player's turn, returns the card played
def play_turn(player, players, round, lead_suit, heart_broken, first_play, trick):
    chosen = ''

    # check if player is real or a bot
    if not player.is_bot:
        # keep asking for a choice until valid
        while is_valid_choice(chosen, player, round, lead_suit, first_play, heart_broken) == False or chosen[:2] == '--':
            # handle if a command has been entered
            if chosen[:2] == '--':
                run_command(chosen.lower(), players)

            # ask player to choose a card, set to upper for case insensitivity
            chosen = input("Enter a card to play: ").upper()
    
    # make a choice for the bot
    else:
        # invoke bot AI
        chosen = make_choice(player, round, lead_suit, heart_broken, first_play, trick)
    
    # check if heart is broken
    if chosen[-1] == 'H':
        return player.remove_card_from_hand(chosen), True
    
    # return previous heart_broken value
    else:
        return player.remove_card_from_hand(chosen), heart_broken

# calculate scores at the end of each game
def calculate_game_scores(players):

    # list of players which need score checked. Someone who 'shot the moon' does not need to be checked as they won't get any points
    players_to_score = [player for player in players if not player.shot_the_moon()]
    
    # check if someone shot the moon by checking player_to_score length (only 1 person can shoot the moon)
    if len(players_to_score) == 3:
        for player in players_to_score:
            player.points += 26
    
    # do normal point calculation if no-one 'shot the moon'
    else:
        for player in players:
            # add a point for each heart in trick
            player.points += player.get_trick_heart_count()

            # add 13 if queen of spades in trick
            if player.has_queen_spades():
                player.points += 13
            
            # reset the trick hand for the next game
            player.reset_trick_hand()

# find the player with the lowest points
def get_winners(players):
    # create a list of points for each player and find the minimum score
    min_score = min([player.points for player in players])

    # loop through players and return a list of all players with min_score
    return [player for player in players if player.points == min_score]


# main game function
def main():
    welcome()
    clear()

    # create some players and store in a list. 3 of them are bots
    players = [Player('You', False), Player('Bot 1', True), Player('Bot 2', True), Player('Bot 3', True)]

    # configure difficulty of bots
    select_difficulty(players)
    clear()
    
    # begin a loop until one player reaches 100 points
    while not any(player.points >= 50 for player in players):

        # create a shuffled deck and deal until everyone's hands are valid
        deck = create_deck()
        deal_deck(players, deck)

        # set/reset heart_broken variable and round_num
        heart_broken = False
        round_num = 1

        # another while loop until users deck is empty
        while len(players[0].hand) != 0:

            # create a 'trick' deck and list of people who played that card
            current_trick = []
            trick_players = []

            # check for game 1, and calculate lead player index if so (player with 2 of clubs goes first)
            if round_num == 1:
                lead_index = find_2_clubs(players)

            # calculate the order of play using lead index
            player_order = get_turn_order(lead_index)

            # loop through each player to do their turn
            for current in player_order:
                # display users hand and if hearts have been broken
                players[0].display_hand()
                print(f"Hearts Broken: {heart_broken}")

                # check to see if player 1's turn and game 1
                if round_num == 1 and lead_index == current:
                    # automatically play 2 of clubs for lead player
                    
                    for card in players[current].hand:
                        if card.face == '2C':
                            current_trick.append(card)
                            trick_players.append(players[current].name)
                            players[current].hand.remove(card)
                    
                    # set the lead suit to clubs
                    lead_suit = 'C'
                
                # handle first turn slightly differently to others
                elif lead_index == current:
                    # play the turn, but check if heart is broken only on this first player
                    played_card, _ = play_turn(players[current], players, round_num, 'DHCS', heart_broken, True, current_trick)

                    # assign the lead suit and add card to trick
                    lead_suit = played_card.face[-1]
                    current_trick.append(played_card)
                    trick_players.append(players[current].name)

                    # display a message in readable, clear format using VAL_CONVERSION to translate card value to proper format
                    clear()
                
                # play by normal rules for every other play
                else:
                    # play the turn and add card to trick
                    played_card, heart_broken = play_turn(players[current], players, round_num, lead_suit, heart_broken, False, current_trick)
                    current_trick.append(played_card)
                    trick_players.append(players[current].name)

                    # display a message in readable, clear format using VAL_CONVERSION to translate card value to proper format
                    clear()
                    
                display_trick(current_trick, trick_players)
                time.sleep(0.5)
            
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
            input(f"\n{players[player_order[highest_card_index]].name} won this trick. (Enter to continue)\n")

            clear()

            # set the new lead_index and increment round number
            lead_index = player_order[highest_card_index]
            round_num += 1

        # calculate and display current game scores
        calculate_game_scores(players)
        display_game_scores(players)
    
    # calculate winners
    winners = get_winners(players)

    # if one winner, print win message
    if len(winners) == 1:
        input(f'\n\n{winners[0].name.upper()} WON!\n\n')
    
    # if multiple winners, print draw message
    elif len(winners) > 1:
        print("\n\nIT'S A DRAW! CONGRATULATIONS:\n")
        for player in winners:
            print(f"{player.name.upper()}")
        print("\n")



if __name__ == "__main__":
    main()