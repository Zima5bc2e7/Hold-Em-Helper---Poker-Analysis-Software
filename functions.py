from random import choice, random
from classes import *
import threading
from PIL import ImageTk


def threaded(function):
    """
    A decorator to run a function in a separate thread.

    Args:
        function: The function to be executed in a separate thread.

    """
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    return wrapper


def rescale(im: Image, max_width) -> Image:
    """
    Rescale an image to fit within a maximum width while preserving the aspect ratio.

    This function takes an input image and resizes it to ensure it fits within a specified
    maximum width while preserving the aspect ratio of the original image.

    Args:
        im (PIL.Image): The input image to be rescaled.
        max_width (int): The maximum width for the rescaled image.

    Returns:
        PIL.Image: The rescaled image that fits within the specified maximum width.

    Example:
        original_image = Image.open("input.jpg")
        max_width = 800
        rescaled_image = rescale(original_image, max_width)
        rescaled_image.save("output.jpg")

    Note:
        The aspect ratio of the original image is maintained when resizing.
    """
    # Calculate the rescaling ratio based on the maximum width
    ratio = max_width / im.size[0]
    # Calculate the new size with the aspect ratio preserved
    new_size = int(im.size[0] * ratio), max(int(im.size[1] * ratio), 1)
    # Resize the image to the new size
    rescaled_image = im.resize(new_size)
    return rescaled_image


def get_blank_card(max_width: int) -> ImageTk.PhotoImage:
    """
    Create a blank card image with a specified maximum width.

    This function loads an image of a card from the file '2_of_clubs.png', resizes it to fit within
    the specified maximum width while preserving its aspect ratio, and then replaces all pixel
    data with a blank gray color.

    Args:
        max_width (int): The maximum width for the blank card image.

    Returns:
        PIL.ImageTk.PhotoImage: The blank card image as a PhotoImage.

    Example:
        max_width = 100
        blank_card = get_blank_card(max_width)
    """
    # Load the card image and rescale it to the specified maximum width
    card_image = rescale(Image.open('images/cards/2_of_clubs.png'), max_width)

    # Convert the image to RGB mode
    rgb = card_image.convert('RGB')

    # Create a new dataset with blank gray pixels
    new_data = [(200, 200, 200) for _ in rgb.getdata()]

    # Update the image data with the blank pixel data
    rgb.putdata(new_data)

    # Convert the modified image to a PhotoImage
    return ImageTk.PhotoImage(rgb)


def compare(hero_hand, villain_hand) -> float:
    """
    Compare two poker hands and determine the winner.

    This function takes two poker hands and compares them to determine the winner or if it's a tie.
    The function follows typical hand ranking rules in poker.

    Args:
        hero_hand (list): The poker hand of the hero.
        villain_hand (list): The poker hand of the villain.

    Returns:
        float: 1.0 if the hero wins, 0.0 if the villain wins, or 0.5 in case of a tie.
    """
    # Evaluate the strength of each hand
    my_hand = read_them_and_weep(hero_hand)
    your_hand = read_them_and_weep(villain_hand)

    # Compare the primary hand ranks
    if my_hand[1] > your_hand[1]:
        return 1
    elif my_hand[1] < your_hand[1]:
        return 0
    else:
        # Compare in case of a tie
        for i in range(2, len(my_hand)):
            tie_break_hero = my_hand[i]
            tie_break_villain = your_hand[i]
            for j in range(len(my_hand[i])):
                if tie_break_hero[j] > tie_break_villain[j]:
                    return 1
                elif tie_break_hero[j] < tie_break_villain[j]:
                    return 0
    # It's a tie
    return 0.5


def check_flush_draw(list_of_cards):
    """
    Check for a flush draw and return the number of cards in the strongest suit.

    Args:
        list_of_cards (list): A list of Card objects to check for a flush draw.

    Returns:
        tuple: A tuple containing two elements - the number of cards in the strongest suit and a list
        of those cards sorted in descending order of their values.
    """
    n = 0   # Number of cards in the strongest suit
    best_suit_cards = []    # List of cards in the strongest suit

    # Iterate through the suits (e.g., Hearts, Spades, etc.)
    for suit in suits:
        same_suit_cards = []    # Temporary list to store cards of the same suit
        r = 0   # Counter for the number of cards in the current suit

        # Iterate through the list of cards to find cards of the current suit
        for card in list_of_cards:
            if card.suit == suit:
                r += 1  # Increment the count
                same_suit_cards.append(card)    # Add the card to the temporary list

        # Check if the current suit has more cards than the previous strongest suit
        if r > n:
            n = r   # Update the number of cards in the strongest suit
            best_suit_cards = sorted(same_suit_cards, reverse=True, key=lambda i: i.value)
    return n, best_suit_cards   # Return the number of cards in the strongest suit and the sorted cards


def check_straight_draw(list_of_cards):
    """
    Check for a straight draw and return the maximum number of consecutive values and the top card value.

    Args:
        list_of_cards (list): A list of Card objects to check for a straight draw.

    Returns:
        tuple: A tuple containing two elements - the maximum number of consecutive values in a straight draw
        and the value of the top card in that straight draw.
    """
    card_values = [card.value for card in list_of_cards]

    # If an Ace (value 14) is present, consider it as 1 for straight possibilities
    if 14 in card_values:
        card_values.append(1)

    card_values.sort()
    n = 1   # Maximum number of consecutive values in a straight draw
    r = 1   # Counter for consecutive values
    top_card = 0    # Value of the top card in the straight draw

    for i in range(len(card_values) - 1):
        if card_values[i + 1] - card_values[i] == 1:
            r += 1   # Increment the consecutive values count
            if r > n:
                n = r   # Update the maximum consecutive values
                top_card = card_values[i + 1]   # Update the value of the top card
        elif card_values[i + 1] - card_values[i] == 0:
            continue    # Ignore duplicate values
        else:
            r = 1   # Reset consecutive values count
    return n, top_card  # Return the maximum consecutive values and the value of the top card


def check_gutshot_straight_draw(list_of_cards):
    """
    Check for gutshot straight draws and return the number of draws and the maximum completing card value.

    A gutshot straight draw involves missing a single card value to complete a straight.

    Args:
        list_of_cards (list): A list of Card objects to check for gutshot straight draws.

    Returns:
        tuple: A tuple containing two elements - the number of gutshot straight draws and the maximum
        card value that would complete the draw.
    """
    card_values = [card.value for card in list_of_cards]

    # If an Ace (value 14) is present, consider it as 1 for straight possibilities
    if 14 in card_values:
        card_values.append(1)

    n = 0   # Number of gutshot straight draws
    max_value = None    # Maximum completing card value
    for i in range(2, 15):
        with_extra = card_values + [i]
        with_extra.sort()
        r = 1   # Consecutive values count
        m = 1   # Maximum consecutive values count

        for j in range(len(with_extra) - 1):
            if with_extra[j + 1] - with_extra[j] == 1:
                r += 1  # Increment the consecutive values count
                if r > m:
                    m = r   # Update the maximum consecutive values
                    max_value = with_extra[j + 1]   # Update the value of the top card
            elif with_extra[j + 1] - with_extra[j] == 0:
                continue    # Ignore duplicate values
            else:
                r = 1   # Reset consecutive values count
        if m >= 5:
            n += 1
    return n, max_value   # Return the number of gutshot straight draws and the maximum completing card value


def check_multiples(list_of_cards):
    """
    Check for multiples (cards with the same value) in a list of cards and return relevant information.

    This function identifies multiples (cards with the same value) and returns the number of multiples,
    the card value with the most multiples, and a list of cards that don't belong to the multiples.

    Args:
        list_of_cards (list): A list of Card objects to check for multiples.

    Returns:
        tuple: A tuple containing three elements - the number of multiples, the card value with the most multiples,
        and a list of cards that are not part of the multiples.
    """
    card_values = [card.value for card in list_of_cards]

    # Sort the card values for easier analysis
    card_values.sort()

    value = 0    # Card value with the most multiples
    n = 1   # Number of multiples
    r = 1   # Consecutive values count
    for i in range(len(card_values) - 1):
        if card_values[i] == card_values[i + 1]:
            r += 1  # Increment the consecutive values count
            if r > n or (r == n and card_values[i] > value):
                n = r   # Update the number of multiples
                value = card_values[i]  # Update the card value with the most multiples
        else:
            r = 1   # Reset the consecutive values count

    # Create a list of cards that don't belong to the multiples
    leftover_cards = [card for card in list_of_cards if card.value != value]
    return n, value, leftover_cards


def high_cards(list_of_cards):
    """
    Determine the highest card values from a list of cards.

    This function takes a list of cards and identifies the highest card values.
    It returns a tuple of the top five card values sorted in descending order.

    Args:
        list_of_cards (list): A list of Card objects to evaluate.

    Returns:
        tuple: A tuple containing the top five card values in descending order.
    """
    card_values = [card.value for card in list_of_cards]

    # Sort the card values in descending order
    card_values.sort(reverse=True)

    # Select the top five card values
    top_five = tuple(card_values[:5])
    return top_five


def read_them_and_weep(list_of_cards):
    """
    Evaluate a list of cards and determine the best poker hand.

    This function takes a list of cards and evaluates them to determine the best possible poker hand.
    It returns the name of the hand, its rank, and relevant card values to represent its strength.

    Args:
        list_of_cards (list): A list of Card objects to evaluate.

    Returns:
        tuple: A tuple containing the hand name, rank, and relevant card values.
    """

    # Check for a flush draw and the highest suit cards
    flush = check_flush_draw(list_of_cards)

    # Check for a straight draw and its top card
    straight = check_straight_draw(list_of_cards)

    # Determine the hand based on evaluation
    if flush[0] >= 5:
        # Check for a straight within the flush
        straight_flush = check_straight_draw(flush[1])
        if straight_flush[0] >= 5:
            return f"Straight Flush, {straight_flush[1]} high", 10, (straight[1], )
        else:
            flush_five = high_cards(flush[1])
            return f"Flush, {flush_five[0]} high", 7, flush_five
            # impossible to have a flush and quads or full house in 7 cards

    # Check for multiples (four of a kind, full house, three of a kind, two pair, or a pair)
    multiples = check_multiples(list_of_cards)
    leftover = check_multiples(multiples[2])

    if multiples[0] == 4:
        kicker = high_cards(multiples[2])[0]
        return f"Quad {multiples[1]}s", 9, (multiples[1], ), (kicker, )
    elif multiples[0] == 3 and leftover[0] >= 2:
        return f"Full House, {multiples[1]}s over {leftover[1]}s", 8, (multiples[1], leftover[1])

    if straight[0] >= 5:
        return f"Straight, {straight[1]} high", 6, (straight[1], )

    if multiples[0] == 3:
        kickers = high_cards(multiples[2])[:2]
        return f"Three of a kind, {multiples[1]}s", 5, (multiples[1], ), tuple(kickers)

    if multiples[0] == 2:
        if leftover[0] == 2:
            remainder = high_cards(leftover[2])
            if remainder:
                kicker = high_cards(leftover[2])[0]
            else:
                kicker = 0
            return f"Two pair, {multiples[1]}s and {leftover[1]}s", 4, (multiples[1], leftover[1], kicker)
        else:
            kickers = high_cards(leftover[2])[:3]
            return f"A pair of {multiples[1]}s", 3, (multiples[1], ), tuple(kickers)
    else:
        high_card = high_cards(list_of_cards)
        return f"High card {high_card[0]}", 2, tuple(high_card)


def check_house_possibility(house_cards, deck):
    """
    Check the possibility of forming a poker house with given house cards and a deck.

    This function checks if it is possible to form a poker full house (a set of three cards and a pair)
    with the provided house cards while considering the availability of cards in the deck.

    Args:
        house_cards (list): A list of Card objects representing the house cards to check.
        deck (Deck): The deck of cards to verify card availability from.

    Returns:
        bool: True if forming a full house is possible, False otherwise.
    """
    possible = True
    for card in house_cards:
        if not deck.cards[card]:
            possible = False
    return possible


def calculate_equity(my_hand, pack, possible_hands, house_cards=()):
    """
    Calculate equity for a poker hand against a range of possible opponent hands.

    This function calculates the equity of a poker hand against a range of possible opponent hands.
    It simulates various outcomes based on possible house cards and competing opponent hands.

    Args:
        my_hand (Hand): The poker hand of the hero.
        pack (Deck): The deck of cards used in the simulation.
        possible_hands (dict): A dictionary of possible opponent hand ranges.
        house_cards (list, optional): House cards that are already dealt.

    Yields:
        tuple: A tuple containing equity percentages and hand breakdown percentages for the hero and opponents.
    """
    # Initialize a dictionary to store hand breakdown information for the hero and opponents.
    hands_breakdown = {'hero': {n: {'made': 0, 'wins': 0} for n in range(2, 11)}}
    for i in range(len(possible_hands)):
        hands_breakdown[i] = {n: {'made': 0, 'wins': 0} for n in range(2, 11)}

    # Get the hero's hand as a tuple.
    hand = my_hand.tuple
    total = 0

    # Initialize a dictionary to store results (number of wins) for the hero and opponents.
    results = {'hero': 0}
    for count, villain_range in enumerate(possible_hands):
        results[count] = 0

    # Calculate the number of remaining cards to deal.
    remaining = 5 - len(house_cards)

    # Create a list of leftover cards from the deck.
    leftover = [card for card in pack.cards if pack.cards[card]]

    # Generate all possible combinations of house cards from the leftover cards.
    houses = list(combinations(leftover, remaining))

    randomiser = 0

    while True:
        possible = False
        villain_hands = {}
        opponents = len(possible_hands)

        # Deal opponent hands and simulate a possible house card combination.
        for n in range(opponents):
            chosen = (n + randomiser) % opponents
            villain = possible_hands[chosen]
            villain.refresh()
            new_list = [hand for hand in villain.hands if villain.hands[hand]]
            villain_hole = choice(new_list).tuple
            villain_hands[chosen] = villain_hole

            # Mark dealt cards as unavailable in the deck.
            for card in villain_hole:
                pack.deal_card(card)

        house = []

        # Randomly select a house card combination until a possible one is found.
        while not possible:
            house = choice(houses)
            possible = check_house_possibility(house, pack)

        # Combine hero's hand, house cards, and dealt house cards.
        hero_final = hand + house + house_cards
        competing = {'hero': hero_final}

        # Combine opponent hands, house cards, and dealt house cards.
        for villain in villain_hands:
            villain_final = villain_hands[villain] + house + house_cards
            competing[villain] = villain_final

        # Increment the total number of simulations.
        total += 1
        randomiser += 1

        # Determine the winner of the current simulation.
        run_out = decide_winner(competing)

        # Update results with the winner of the current simulation.
        for player in results:
            results[player] += run_out[player]
            made_hand = read_them_and_weep(competing[player])[1]

            # Update hand breakdown statistics.
            hands_breakdown[player][made_hand]['made'] += 1
            hands_breakdown[player][made_hand]['wins'] += run_out[player]

        # Calculate and yield the current equity percentages.
        share = {player: results[player] * 100 / total for player in results}
        hands_breakdown_percentages = {player: {made_hand: {'made': hands_breakdown[player][made_hand]['made'] / total,
                                                            'wins': hands_breakdown[player][made_hand]['wins'] / total}
                                                for made_hand in hands_breakdown[player]}
                                       for player in hands_breakdown}
        yield share, hands_breakdown_percentages

        # Restore dealt cards to the deck.
        for antagonist in villain_hands:
            for card in villain_hands[antagonist]:
                pack.add_cards(card)


def calculate_called_equity(my_hand, pack, possible_hands, initial_ranges, house_cards=()):
    """
    Calculate equity for a poker hand in a scenario where opponents may fold or call.

    This function calculates the equity of a poker hand in a scenario where possible opponents
    may choose to fold or call based on their initial hand ranges.

    Args:
        my_hand (Hand): The poker hand of the hero.
        pack (Deck): The deck of cards used in the simulation.
        possible_hands (list): A dictionary of possible opponent hand ranges.
        initial_ranges (list): The initial hand ranges of possible opponents.
        house_cards (list, optional): House cards that are already dealt.

    Yields:
        tuple: A tuple containing equity percentages, fold percentages, and average number of players.
    """
    hand = my_hand.tuple
    total = 0
    folds = 0
    wins = 0
    players = 0

    # Calculate the number of remaining cards to deal.
    remaining = 5 - len(house_cards)

    # Create a list of leftover cards from the deck.
    leftover = [card for card in pack.cards if pack.cards[card]]

    # Generate all possible combinations of house cards from the leftover cards.
    houses = list(combinations(leftover, remaining))
    randomiser = 0

    while True:
        possible = False
        villain_hands = {}
        opponents = len(possible_hands)

        # Iterate over possible opponents.
        for n in range(opponents):
            chosen = (n + randomiser) % opponents
            villain_initial = initial_ranges[chosen]
            villain_initial.refresh()
            villain = possible_hands[chosen]
            villain.refresh()

            # Extract the initial and current possible opponent hand lists.
            old_list = [hand for hand in villain_initial.hands if villain_initial.hands[hand]]
            new_list = [hand for hand in villain.hands if villain.hands[hand]]

            # Calculate the calling percentage based on the difference in hand lists.
            call_percentage = len(new_list) / len(old_list)

            # Generate a random number to determine if the opponent calls.
            random_number = random()
            if random_number < call_percentage:
                # The opponent calls, so choose a hand from the current list.
                villain_hole = choice(new_list).tuple
                villain_hands[chosen] = villain_hole

                # Mark the dealt cards as unavailable in the deck.
                for card in villain_hole:
                    pack.deal_card(card)

        randomiser += 1
        total += 1

        # If no opponent called, increment the fold count.
        if not villain_hands:
            folds += 1
            if total - folds:
                # Calculate and yield equity, fold percentage, and average number of players.
                output = wins / (total - folds), folds / total, players / (total - folds)
                yield output
            continue

        house = []

        # Randomly select a house card combination until a possible one is found.
        while not possible:
            house = choice(houses)
            possible = check_house_possibility(house, pack)
        hero_final = hand + house + house_cards
        competing = {'hero': hero_final}

        # Combine opponent hands, house cards, and dealt house cards.
        for villain in villain_hands:
            villain_final = villain_hands[villain] + house + house_cards
            competing[villain] = villain_final

        players += len(competing)

        # Determine the winner of the current simulation.
        run_out = decide_winner(competing)

        # Increment the wins counter for the hero.
        wins += run_out['hero']

        # Calculate and yield equity, fold percentage, and average number of players.
        output = wins / (total - folds), folds / total, players / (total - folds)
        yield output

        # Restore dealt cards to the deck.
        for antagonist in villain_hands:
            for card in villain_hands[antagonist]:
                pack.add_cards(card)


def calculate_shove_ev(my_hand, pack, possible_hands, pot, bet, initial_ranges, house_cards=()):
    """
    Calculate the expected value (EV) of shoving (going all-in) with a poker hand.

    This function calculates the expected value of shoving (going all-in) with a poker hand in a
    scenario where opponents may fold or call based on their initial hand ranges.

    Args:
        my_hand (Hand): The poker hand of the hero.
        pack (Deck): The deck of cards used in the simulation.
        possible_hands (list): A list of possible opponent hand ranges.
        pot (float): The size of the pot.
        bet (float): The size of the hero's bet.
        initial_ranges (list): The initial hand ranges of possible opponents.
        house_cards (list, optional): House cards that are already dealt.

    Yields:
        float: The expected value (EV) of shoving (going all-in) with the hero's hand.
    """
    hand = my_hand.tuple
    total = 0
    balance = 0
    wins = 0
    times_called = 0

    # Calculate the number of remaining cards to deal.
    remaining = 5 - len(house_cards)

    # Create a list of leftover cards from the deck.
    leftover = [card for card in pack.cards if pack.cards[card]]

    # Generate all possible combinations of house cards from the leftover cards.
    houses = list(combinations(leftover, remaining))
    randomiser = 0
    while True:
        possible = False
        villain_hands = {}
        opponents = len(possible_hands)

        # Iterate over possible opponents.
        for n in range(opponents):
            chosen = (n + randomiser) % opponents
            villain_initial = initial_ranges[chosen]
            villain_initial.refresh()
            villain = possible_hands[chosen]
            villain.refresh()

            # Extract the initial and current possible opponent hand lists.
            old_list = [hand for hand in villain_initial.hands if villain_initial.hands[hand]]
            new_list = [hand for hand in villain.hands if villain.hands[hand]]

            # Calculate the calling percentage based on the difference in hand lists.
            call_percentage = len(new_list) / len(old_list)

            # Generate a random number to determine if the opponent calls.
            random_number = random()
            if random_number < call_percentage:
                # The opponent calls, so choose a hand from the current list.
                villain_hole = choice(new_list).tuple
                villain_hands[chosen] = villain_hole

                # Mark the dealt cards as unavailable in the deck.
                for card in villain_hole:
                    pack.deal_card(card)
        randomiser += 1
        total += 1

        # If no opponent called, the hero collects the pot.
        if not villain_hands:
            balance += pot
            ev = balance / total
            yield ev
            continue

        house = []

        # Randomly select a house card combination until a possible one is found.
        while not possible:
            house = choice(houses)
            possible = check_house_possibility(house, pack)

        hero_final = hand + house + house_cards
        competing = {'hero': hero_final}

        # Combine opponent hands, house cards, and dealt house cards.
        for villain in villain_hands:
            villain_final = villain_hands[villain] + house + house_cards
            competing[villain] = villain_final

        run_out = decide_winner(competing)

        # Adjust the balance based on the result of the hand.
        if run_out['hero'] == 0:
            balance -= bet
        else:
            balance += (pot + (bet * len(competing))) * run_out['hero'] - bet

        ev = balance / total
        times_called += 1
        wins += run_out['hero']
        yield ev

        # Restore dealt cards to the deck.
        for antagonist in villain_hands:
            for card in villain_hands[antagonist]:
                pack.add_cards(card)


def decide_winner(players):
    """
    Determine the winner and calculate their share of the pot.

    This function compares each player's hand against all other players' hands and calculates the
    share of the pot they should receive based on their chances of winning.

    Args:
        players (dict): A dictionary containing player names as keys and their poker hands as values.

    Returns:
        dict: A dictionary containing player names as keys and their share of the pot as values.
    """
    result = {}

    # Initialize each player's result to 0.
    for player in players:
        result[player] = 0

    # Compare each player's hand with all other players.
    for player in players:
        for opponent in players:
            if player != opponent:
                duel = compare(players[player], players[opponent])

                # If the player loses to any opponent, their result is 0.
                if duel == 0:
                    result[player] = 0
                    break
                else:
                    result[player] += duel

    # Calculate the total sum of results.
    total = sum(result[player] for player in players)

    # Calculate each player's share of the pot based on their chances of winning.
    for player in players:
        result[player] /= total
    return result


def check_draws(villain_hands, house):
    """
    Check and categorize possible draws for each player's hand against the community cards.

    This function evaluates the possible draws for each player's hand in relation to the community cards,
    including straight draws, flush draws, overcards, and made hands.

    Args:
        villain_hands (HandRange): A range of possible opponent hands.
        house (list): Community cards on the board.

    Returns:
        dict: A dictionary containing draw information for each player's hand.
    """
    # Evaluate the current draws on the board
    on_board_draws = {
        'straight': check_gutshot_straight_draw(house),
        'run-of-three': False,
        'flush': check_flush_draw(house)[0],
        'made': read_them_and_weep(house)
    }

    # Check for run-of-three straight draws
    if check_straight_draw(house)[0] == 3:
        on_board_draws['run-of-three'] = check_straight_draw(house)

    # Create a dictionary to store draw information for each player's hand
    hands = [hand for hand in villain_hands.hands if villain_hands.hands[hand]]
    draw_dict = {hand: {'name': hand.long_name,
                        'overcards': False,
                        'straight': False,
                        'run-of-three': False,
                        'flush': False,
                        'made': False} for hand in hands}

    for hand in hands:
        all_cards = list(hand.tuple) + house
        made = read_them_and_weep(all_cards)

        # Evaluate the made hand
        if made[0] != on_board_draws['made'][0] and made[1] != 2:
            house_in_order = high_cards(house)

            if made[1] == 10:
                draw_dict[hand]['made'] = 'Straight Flush'
            elif made[1] == 9:
                draw_dict[hand]['made'] = 'Quads'
            elif made[1] == 8:
                draw_dict[hand]['made'] = 'Full House'
            elif made[1] == 7:
                house_flush_cards = high_cards(check_flush_draw(house)[1])
                complete_flush_cards = high_cards(check_flush_draw(all_cards)[1])

                # Determine nut flush
                if house_flush_cards[0] != 14:
                    nut = 0, 14
                elif house_flush_cards[1] != 13:
                    nut = 1, 13
                elif house_flush_cards[2] != 12:
                    nut = 2, 12
                elif len(house_flush_cards) == 3 or house_flush_cards[3] != 11:
                    nut = 3, 11
                else:
                    nut = 4, 10

                if complete_flush_cards[nut[0]] == nut[1]:
                    draw_dict[hand]['made'] = 'Nut Flush'
                else:
                    draw_dict[hand]['made'] = 'Flush'
            elif made[1] == 6:
                draw_dict[hand]['made'] = 'Straight'
            elif made[1] == 5:
                draw_dict[hand]['made'] = 'Three of a Kind'
            elif made[1] == 4:
                draw_dict[hand]['made'] = 'Two Pair'
                # pairs = made[2][0], made[2][1]
                #
                # # Evaluate pairs or two pairs
                # if check_multiples(house)[0] == 2 or on_board_draws['made'][1] == 4:
                #     if pairs[0] > house_in_order[0]:
                #         draw_dict[hand]['made'] = 'Overpair'
                #     elif pairs[1] < house_in_order[-1]:
                #         draw_dict[hand]['made'] = 'Underpair'
                #     else:
                #         draw_dict[hand]['made'] = 'Mid Two Pair'
                #         # A3 on AQQ hits this, consider condensing all to 'Two Pair'
                # else:
                #     if pairs[0] == house_in_order[0] and pairs[1] == house_in_order[1]:
                #         draw_dict[hand]['made'] = 'Top Two Pair'
                #     elif pairs[0] == house_in_order[-2] and pairs[1] == house_in_order[-1]:
                #         draw_dict[hand]['made'] = 'Bottom Two Pair'
                #     else:
                #         draw_dict[hand]['made'] = 'Mid Two Pair'
            elif made[1] == 3:
                if made[2][0] > house_in_order[0]:
                    draw_dict[hand]['made'] = 'Overpair'
                elif made[2][0] < house_in_order[-1]:
                    draw_dict[hand]['made'] = 'Underpair'
                elif made[2][0] == house_in_order[0]:
                    draw_dict[hand]['made'] = 'Top Pair'
                elif made[2][0] == house_in_order[-1]:
                    draw_dict[hand]['made'] = 'Bottom Pair'
                else:
                    draw_dict[hand]['made'] = 'Mid Pair'

        # Check for flush draws
        flush = check_flush_draw(all_cards)
        if flush[0] == 4 and on_board_draws['flush'] != 4:
            draw_dict[hand]['flush'] = 1
        elif flush[0] == 3 and on_board_draws['flush'] != 3:
            draw_dict[hand]['flush'] = 2

        # Check for straight draws
        run_check = check_straight_draw(all_cards)
        if run_check[0] < 5:
            straight_outs = check_gutshot_straight_draw(all_cards)
            legitimate_outs = straight_outs[0] - on_board_draws['straight'][0]

            # Handle potential straight draws
            if on_board_draws['straight'][0] and straight_outs[1] > on_board_draws['straight'][1]:
                legitimate_outs += 1
                # to deal with situations like ((8,9) on (3,4,5,6))
            draw_dict[hand]['straight'] = legitimate_outs

            # Check for run-of-three straight draws
            if not draw_dict[hand]['straight']:
                if run_check[0] == 3:
                    if not on_board_draws['run-of-three'] or run_check[1] > on_board_draws['run-of-three'][1]:
                        draw_dict[hand]['run-of-three'] = True

        # Check for overcards
        if made[1] == on_board_draws['made'][1] and made != on_board_draws['made']:
            hand_cards = [hand.card_1.value, hand.card_2.value]
            hand_cards.sort(reverse=True)
            house_in_order = high_cards(house)
            if house_in_order[0] < hand_cards[0]:
                if house_in_order[0] < hand_cards[1]:
                    draw_dict[hand]['overcards'] = 2
                else:
                    draw_dict[hand]['overcards'] = 1
    return draw_dict


def find_ev(pot, stake, equity, fold):
    """
    Calculate the expected value (EV) for a poker hand.

    This function calculates the expected value (EV) for a poker hand based on the given parameters.
    The EV takes into account the pot size, stake, player's equity, and the probability of folding.

    Args:
        pot (float): The current size of the pot.
        stake (float): The player's stake or bet.
        equity (float): The player's equity in percentage (0-100).
        fold (float): The probability of the player folding in percentage (0-100).

    Returns:
        float: The calculated expected value for the hand.
    """
    # Convert equity and fold percentages to decimals
    equity /= 100
    fold /= 100

    # Calculate the expected value (EV)
    ev = fold * pot + (1 - fold) * (equity * (pot + 2 * stake) - stake)
    return ev


def find_bet(equity, fold, pot, check_equity, players):
    """
    Calculate the recommended bet size and categorize it as 'over' or 'under' bet.

    This function calculates the recommended bet size based on the given parameters.
    It also categorizes the bet as 'over' or 'under' depending on the relative
    equity, fold percentage, pot size, check equity, and the number of players.

    Args:
        equity (float): The player's equity in percentage (0-100).
        fold (float): The probability of the player folding in percentage (0-100).
        pot (float): The current size of the pot.
        check_equity (float): The check equity for the player in percentage (0-100).
        players (int): The number of players in the game.

    Returns:
        tuple: A tuple containing two values - the recommendation category ('over' or 'under')
               and the recommended bet size (integer).
    """
    # Convert percentages to decimals
    equity /= 100
    fold /= 100
    check_equity /= 100

    # Calculate the recommended bet size and categorize it
    denominator = (fold - 1) * (1 - players * equity)
    if denominator != 0:
        if denominator > 0:
            over_under = 'Min Bet:'
        else:
            over_under = 'Max Bet:'
        return over_under, int((pot * (check_equity - equity + fold * (equity - 1))) / denominator)
    else:
        return 'unlikely', 0
