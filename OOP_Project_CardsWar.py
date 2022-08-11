#####################################
### WELCOME TO YOUR OOP PROJECT #####
#####################################

# For this project you will be using OOP to create a card game. This card game will
# be the card game "War" for two players, you an the computer. If you don't know
# how to play "War" here are the basic rules:
#
# The deck is divided evenly, with each player receiving 26 cards, dealt one at a time,
# face down. Anyone may deal first. Each player places his stack of cards face down,
# in front of him.
#
# The Play:
#
# Each player turns up a card at the same time and the player with the higher card
# takes both cards and puts them, face down, on the bottom of his stack.
#
# If the cards are the same rank, it is War. Each player turns up three cards face
# down and one card face up. The player with the higher cards takes both piles
# (six cards). If the turned-up cards are again the same rank, each player places
# another card face down and turns another card face up. The player with the
# higher card takes all 10 cards, and so on.
#
# There are some more variations on this but we will keep it simple for now.
# Ignore "double" wars
#
# https://en.wikipedia.org/wiki/War_(card_game)

from ast import Pass
from os import popen
from random import shuffle

from pymysql import NULL

# Two useful variables for creating Cards.
SUITE = 'H D S C'.split()
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

# DECK CLASS


class Deck:
    """
    This is the Deck Class. This object will create a deck of cards to initiate
    play. You can then use this Deck list of cards to split in half and give to
    the players. It will use SUITE and RANKS to create the deck. It should also
    have a method for splitting/cutting the deck in half and Shuffling the deck.
    """

    def __init__(self, suite, ranks):
        self.cards = [[r, s] for r in ranks for s in suite]
        shuffle(self.cards)

    # SPLITING CARDS
    def splitting(self):

        first_half, second_half = [], []

        for x in range(len(self.cards)):
            first_half.append(
                self.cards[x]) if x % 2 == 0 else second_half.append(self.cards[x])

        return first_half, second_half


class Hand:
    '''
    This is the Hand class. Each player has a Hand, and can add or remove
    cards from that hand. There should be an add and remove card method here.
    '''

    def __init__(self, cards):
        self.cards = cards

    def __add__(self, card):
        self.cards.extend([card])

    def __del__(self):
        if self.cards:
            return self.cards.pop(0)
        return

    def __len__(self):
        return len(self.cards)


class Player():
    """
    This is the Player class, which takes in a name and an instance of a Hand

    class object. The Payer can then play cards and check if they still have cards.
    """

    def __init__(self, name, hand):
        self.hand = hand
        self.name = name

    def check(self):
        return self.hand.__len__()

    def play(self):
        return self.hand.__del__()

    def win(self, card):
        for i in range(len(card)):
            self.hand.__add__(card[i])

    def war(self):
        war_cards = []
        if self.hand.__len__() > 3:
            for i in range(3):
                war_cards.append(self.hand.__del__())

        elif self.hand.__len__() != 1:
            for i in range(self.hand.__len__()-1):
                war_cards.append(self.hand.__del__())

        return war_cards


######################
#### GAME PLAY #######
######################
print("Welcome to War, let's begin...")

deck = Deck(SUITE, RANKS)
cards_p1, cards_p2 = deck.splitting()
player1 = Player('player1', Hand(cards_p1))
player2 = Player('player2', Hand(cards_p2))
# print(cards_p1)
# print('\n')
# print(cards_p2)

round = 1
war = 0

# WHILE BOTH PLAYER STILL HAVE CARDS ON DECK
while player1.check() != 0 and player2.check() != 0:
    tempCard = []
    # print('p1 => {0}'.format(player1.check()))
    # print('p2 => {0}'.format(player2.check()))

    tempCard.append(player1.play())
    tempCard.append(player2.play())

    # CHECK IF WAR
    if(RANKS.index(tempCard[0][0]) == RANKS.index(tempCard[1][0])):
        war+1
        print("WAR in {0}".format(round))

        # WAR CARDS
        tempCard.extend(player1.war())
        tempCard.extend(player2.war())

        # PLAYER PLAY CARDS
        tempCard.append(player1.play())
        tempCard.append(player2.play())

        lentemp = len(tempCard)-1
        # CHECK IF RANKS CARD P1 > P2
        if(RANKS.index(tempCard[lentemp-1][0]) > RANKS.index(tempCard[lentemp][0])):
            player1.win(tempCard)
            print('\nplayer1 win')
        # RANKS CARD P2 > P1
        else:
            player2.win(tempCard)
            print('\nplayer2 win')

    # CHECK IF RANKS CARD P1 > P2
    elif(RANKS.index(tempCard[0][0]) > RANKS.index(tempCard[1][0])):
        player1.win(tempCard)
        print(tempCard[0][0]+' VS '+tempCard[1][0])

    # RANKS CARD P2 > P1
    else:
        player2.win(tempCard)
        print(tempCard[0][0]+' VS '+tempCard[1][0])

    round += 1

################# GAME ENDED #####################
print("\n================= GAME ENDED =================")
print("\nTOTAL ROUNDS => {0}".format(round))
print("\nTOTAL WAR => {0}".format(war))
print("\nTHE WINNER IS")
print("\nPlayer 1") if player2.check() == 0 else print("\nPlayer 2 ")
