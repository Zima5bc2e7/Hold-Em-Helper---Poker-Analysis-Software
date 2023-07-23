from itertools import combinations
from data import *


class Card:
    def __init__(self, name, suit):
        name = str(name)
        self.value = values[name.upper()]
        self.suit = suit.title()
        self.name = name.upper()
        # self.id = name.upper() + " of " + suit
        self.id = name.upper() + suit_symbols[self.suit]

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __hash__(self):
        return hash((self.value, self.suit))


class Hand:
    def __init__(self, card_1, card_2):
        if card_1.value > card_2.value:
            self.card_1 = card_1
            self.card_2 = card_2
        elif card_2.value > card_1.value:
            self.card_1 = card_2
            self.card_2 = card_1
        elif suits_alpha[card_1.suit] > suits_alpha[card_1.suit]:
            self.card_1 = card_1
            self.card_2 = card_2
        else:
            self.card_1 = card_2
            self.card_2 = card_1
        if card_1.suit == card_2.suit:
            self.suited = "s"
        else:
            self.suited = ""
        self.name = self.card_1.name + self.card_2.name + self.suited
        self.tuple = (self.card_1, self.card_2)
        self.long_name = self.card_1.id + ", " + self.card_2.id
        self.set = {self.card_1, self.card_2}

    def __eq__(self, other):
        return self.card_1 == other.card_1 and self.card_2 == other.card_2

    def __hash__(self):
        return hash((self.card_1, self.card_2))


class Range:
    def __init__(self, pack, high, low):
        self.high = high / 100
        self.low = low / 100
        self.pack = pack
        self.hands = {hand: True for hand in self.pack.possible_hands
                      if self.high <= starting_hand_ranks[hand.name] <= self.low and self.pack.possible_hands[hand]}
        # self.tuples = [hand1.tuple for hand1 in self.hands]
        # self.permitted = {hand.long_name for hand in self.hands}
        self.hand_names = {hand.name for hand in self.hands}
        self.removed_hands = set()
        self.range_density = {hand_name: sum(1 if hand.name == hand_name and self.hands[hand]
                                             else 0 for hand in self.hands) for hand_name in self.hand_names}

    def refresh(self):
        # for hand in self.hands:
        #     if hand in self.hands[hand]:
        #         continue

        self.hands = {hand: True for hand in self.pack.possible_hands
                      if self.high <= starting_hand_ranks[hand.name] <= self.low and self.pack.possible_hands[hand]
                      and hand not in self.removed_hands}
        self.hand_names = {hand.name for hand in self.hands}
        self.range_density = {hand_name: sum(1 if hand.name == hand_name and self.hands[hand]
                                             else 0 for hand in self.hands) for hand_name in self.hand_names}

    def remove(self, hand):
        self.hands[hand] = False

    def revise(self, **kwargs):
        for hand in self.hands:
            if not self.hands[hand]:
                continue
            if hand.card_1.name in kwargs["ranks"] or hand.card_2.name in kwargs["ranks"]:
                self.hands[hand] = True
            elif hand.name[:2] in kwargs["two_ranks"]:
                self.hands[hand] = True
            elif hand.card_1.suit in kwargs["one_suit"] or hand.card_2.suit in kwargs["one_suit"]:
                self.hands[hand] = True
            elif hand.card_1.suit == hand.card_2.suit and hand.card_1.suit in kwargs["two_suits"]:
                self.hands[hand] = True
            else:
                self.hands[hand] = False
                self.removed_hands.add(hand)


class Pack:
    def __init__(self):
        cards = []
        for value in values:
            # print(value)
            for suit in suits:
                # print(suit)
                new_card = Card(value, suit)
                cards.append(new_card)
        self.cards = {card: True for card in cards}
        combos = tuple(combinations(self.cards, 2))
        possible_hands = {Hand(combo[0], combo[1]): True for combo in combos}
        self.possible_hands = possible_hands
        self.possible_hand_names = {hand.long_name for hand in self.possible_hands}

    def deal_card(self, card):
        self.cards[card] = False
        self.check_possible_hands()
        # print(len(self.possible_hands))
        return card

    def add_cards(self, *args):
        for card in args:
            self.cards[card] = True
        self.check_possible_hands()
        # self.possible_hand_names = {hand.long_name for hand in self.possible_hands}
        # print(len(self.possible_hands))

    def deal_specific_card(self, name, suit):
        new_card = [card for card in self.cards if card.name == name.upper() and card.suit == suit.title()]
        deal = new_card[0]
        self.cards[deal] = False
        self.check_possible_hands()
        return deal

    def check_possible_hands(self):
        for hand in self.possible_hands:
            card_1 = hand.card_1
            card_2 = hand.card_2
            if self.cards[card_1] and self.cards[card_2]:
                self.possible_hands[hand] = True
            else:
                self.possible_hands[hand] = False
        return self.possible_hands


