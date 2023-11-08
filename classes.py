from itertools import combinations
from data import *
from PIL import Image


class Card:
    """
    Represents a playing card with a name and suit.

    Attributes:
        name (str): The name of the card (e.g., 'A', '2', 'K', 'T').
        value (int): The numeric value associated with the card.
        suit (str): The suit of the card (e.g., 'Hearts', 'Spades').
        id (str): A unique identifier for the card based on its name and suit.
        image_path (str): The file path to the card's image.

    Methods:
        __eq__(other): Check if two cards are equal based on their value and suit.
        __hash__(): Compute a custom hash for the card based on value and suit.

    Note:
        The `values` dictionary is used to map card names to their numeric values.

    Example:
        card = Card('A', 'Hearts')
        print(card.name)  # Output: 'A'
        print(card.value)  # Output: 14
        print(card.suit)  # Output: 'Hearts'
    """
    def __init__(self, name, suit):
        # Initialize a Card with a name and suit
        self.name = str(name)
        # Get the value of the card from the 'values' dictionary
        self.value = values[name.upper()]
        self.suit = suit.title()
        self.name = name.upper()
        # Construct a unique ID for the card based on name and suit
        self.id = name.upper() + suit_symbols[self.suit]
        # Define the image path for the card
        self.image_path = f'images/cards/{self.name}_of_{self.suit.lower()}.png'
        self.raw_image = Image.open(self.image_path)

    def __eq__(self, other):
        """
        Compare this card with another card for equality based on value and suit.

        Args:
            other (Card): Another card to compare with.

        Returns:
            bool: True if the cards have the same value and suit, False otherwise.
        """
        return self.value == other.value and self.suit == other.suit

    def __hash__(self):
        """
        Compute a custom hash value for the Card object.

        Returns:
            int: A custom hash value based on the card's value and suit.
        """
        # Define a custom hash function for the Card class
        return hash((self.value, self.suit))


class Hand:
    """
    Represents a poker hand consisting of two cards.

    Attributes:
        card_1 (Card): The first card in the hand.
        card_2 (Card): The second card in the hand.
        suited (str): 's' if the two cards have the same suit, '' (empty string) otherwise.
        name (str): A short name representing the hand (e.g., 'AhKs', 'QdJh').
        tuple (tuple): A tuple containing the two cards in the hand.
        long_name (str): A long name representing the hand (e.g., 'Ace of Hearts, King of Spades').
        set (set): A set containing the two cards in the hand.

    Methods:
        __eq__(other): Check if two hands are equal based on their cards.
        __hash__(): Compute a custom hash value for the Hand object.

    Example:
        card_1 = Card('A', 'Hearts')
        card_2 = Card('K', 'Spades')
        hand = Hand(card_1, card_2)
        print(hand.name)  # Output: 'AhKs'
    """
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
        """
        Compare this hand with another hand for equality based on their cards.

        Args:
            other (Hand): Another hand to compare with.

        Returns:
            bool: True if the hands have the same cards, False otherwise.
        """
        return self.card_1 == other.card_1 and self.card_2 == other.card_2

    def __hash__(self):
        """
        Compute a custom hash value for the Hand object.

        Returns:
            int: A custom hash value based on the hand's cards.
        """
        return hash((self.card_1, self.card_2))


class Range:
    """
    Represents a poker hand range with specified high and low values.

    Attributes:
        high (float): The upper bound of the hand range as a percentage (e.g., 20%).
        low (float): The lower bound of the hand range as a percentage (e.g., 10%).
        deck (Deck): The deck of possible poker hands to create the range from.
        hands (dict): A dictionary of hands in the range.
        hand_names (set): A set of hand names in the range.
        removed_hands (set): A set of hands that have been removed from the range.
        range_density (dict): A dictionary of hand name to density mapping within the range.

    Methods:
        refresh(): Refresh the range by updating the included hands and range density.
        remove(hand): Remove a specific hand from the range.
        revise(**kwargs): Revise the range based on specified criteria (ranks, two_ranks, one_suit, two_suits).
        get_hands(): Get a list of hands in the range.

    Example:
        deck = Deck(...)
        high = 20  # 20%
        low = 10  # 10%
        hand_range = Range(deck, high, low)
        print(hand_range.get_hands())  # Output: List of hands in the specified range.
    """
    def __init__(self, deck, high, low):
        self.high = high.get() / 100    # Convert to a decimal percentage.
        self.low = low.get() / 100  # Convert to a decimal percentage.
        self.deck = deck
        self.hands = {hand: True for hand in self.deck.possible_hands
                      if self.high <= starting_hand_ranks[hand.name] <= self.low and self.deck.possible_hands[hand]}
        self.hand_names = {hand.name for hand in self.hands}
        self.removed_hands = set()
        self.range_density = {hand_name: sum(1 if hand.name == hand_name and self.hands[hand]
                                             else 0 for hand in self.hands) for hand_name in self.hand_names}

    def refresh(self):
        """
        Refresh the range by updating the included hands and range density.
        """
        self.hands = {hand: True for hand in self.deck.possible_hands
                      if self.high <= starting_hand_ranks[hand.name] <= self.low and self.deck.possible_hands[hand]
                      and hand not in self.removed_hands}
        self.hand_names = {hand.name for hand in self.hands}
        self.range_density = {hand_name: sum(1 if hand.name == hand_name and self.hands[hand]
                                             else 0 for hand in self.hands) for hand_name in self.hand_names}

    def remove(self, hand):
        """
        Remove a specific hand from the range.

        Args:
            hand (Hand): The hand to remove from the range.
        """
        self.hands[hand] = False
        self.removed_hands.add(hand)

    def get_hands(self):
        """
        Get a list of hands in the range.

        Returns:
            list: A list of hands in the range.
        """
        return [hand for hand in self.hands if self.hands[hand]]


class Deck:
    """
    Represents a standard deck of playing cards.

    Attributes:
        cards (dict): A dictionary of cards in the deck and their availability.
        possible_hands (dict): A dictionary of possible poker hands that can be formed from the deck.

    Methods:
        deal_card(card): Marks a specific card as dealt and updates possible poker hands.
        add_cards(*args): Marks multiple cards as available and updates possible poker hands.
        deal_specific_card(name, suit): Marks a specific card as dealt by name and suit, updating possible poker hands.
        check_possible_hands(): Checks and updates the availability of possible poker hands based on dealt cards.

    Example:
        deck = Deck()
        card = deck.deal_card(some_card)
        deck.add_cards(card_1, card_2, card_3)
    """
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
        """
        Marks a specific card as dealt and updates possible poker hands.

        Args:
            card (Card): The card to be marked as dealt.

        Returns:
            Card: The card that has been dealt.
        """
        self.cards[card] = False
        self.check_possible_hands()
        return card

    def add_cards(self, *args):
        """
        Marks multiple cards as available and updates possible poker hands.

        Args:
            *args (Card): One or more cards to be marked as available.
        """
        for card in args:
            self.cards[card] = True
        self.check_possible_hands()

    def deal_specific_card(self, name, suit):
        """
        Marks a specific card as dealt by name and suit, updating possible poker hands.

        Args:
            name (str): The name of the card (e.g., 'A', 'K', '2').
            suit (str): The suit of the card (e.g., 'Hearts', 'Spades').

        Returns:
            Card: The card that has been dealt.
        """
        new_card = [card for card in self.cards if card.name == name.upper() and card.suit == suit.title()]
        deal = new_card[0]
        self.cards[deal] = False
        self.check_possible_hands()
        return deal

    def check_possible_hands(self):
        """
        Checks and updates the availability of possible poker hands based on dealt cards.

        Returns:
            dict: A dictionary of possible poker hands and their availability.
        """
        for hand in self.possible_hands:
            card_1 = hand.card_1
            card_2 = hand.card_2
            if self.cards[card_1] and self.cards[card_2]:
                self.possible_hands[hand] = True
            else:
                self.possible_hands[hand] = False
        return self.possible_hands


class Manager:
    """
    Manages game data and calculations for the poker application.

    Attributes:
        game_data (dict): A dictionary containing game-related data, such as the deck, hand, house cards, and more.
        calculating (dict): A dictionary of flags to track various calculations (e.g., equity, shove).
        summary: Reference to the summary object (not explicitly defined here).
        notebook: Reference to the notebook object (not explicitly defined here).
        tabs (dict): A dictionary to store references to different tabs in the notebook.
        resize_ratio (float): The ratio used for resizing elements.
        width (int): The width of the application window.
        height (int): The height of the application window.
        small_card (int): The size of small playing cards.
        large_card (int): The size of large playing cards.
        small_pad (int): The size of small padding.
        large_pad (int): The size of large padding.
        button (int): The size of hand buttons

    Methods:
        refresh(): Refresh the summary (if available).
        stop_calculating(): Set all calculation flags to False.
    Example:
        manager = Manager(1.0)
        manager.refresh()
        manager.stop_calculating()
    """
    def __init__(self, resize_ratio):
        """
        Initialize the Manager with the given resize ratio.

        Args:
            resize_ratio (float): The ratio used for resizing elements.
        """
        # Initialize game data and calculation flags
        self.game_data = {
            'deck': Deck(),
            'hand': None,
            'house': [],
            'ranges': [],
            'equity': {},
            'hand_breakdown': {}
        }
        self.calculating = {
            'equity': False,
            'shove': False
        }

        # Store references to summary, notebook, and other properties
        self.summary = None
        self.notebook = None
        self.tabs = {}

        # Store resize ratio and dimensions
        self.resize_ratio = resize_ratio
        self.width = int(1366 * resize_ratio)
        self.height = int(768 * resize_ratio)
        self.small_card = int(62 * resize_ratio)
        self.large_card = int(70 * resize_ratio)
        self.small_pad = int(5 * resize_ratio)
        self.large_pad = int(10 * resize_ratio)
        self.button = int(3 * resize_ratio)
        self.scale_length = int(200 * resize_ratio)

    def refresh(self):
        """
        Refresh the summary (if available).
        """
        self.summary.refresh()

    def stop_calculating(self):
        """
        Set all calculation flags to False.
        """
        for calculation in self.calculating:
            self.calculating[calculation] = False
