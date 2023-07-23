from random import choice, randint, shuffle
from classes import *
import time


def check_trick(list_of_cards):
    flush = check_flush(list_of_cards)
    straight = check_straight(list_of_cards)
    if flush[0] and straight[0]:
        return f"Straight Flush, {straight[1][0]} high", 10, straight[1]
    quads = check_quads(list_of_cards)
    if quads[0]:
        return f"Quad {quads[1][0]}s", 9, quads[1:]
    full_house = check_full_house(list_of_cards)
    if full_house[0]:
        return f"Full House, {full_house[1][0]}s over {full_house[1][1]}s", 8, full_house[1:]
    elif flush[0]:
        return f"Flush, {flush[1][0]} high", 7, flush[1:]
    elif straight[0]:
        return f"Straight, {straight[1][0]} high", 6, straight[1:]
    three_of_a_kind = check_three(list_of_cards)
    if three_of_a_kind[0]:
        return f"Three of a kind, {three_of_a_kind[1][0]}s", 5, three_of_a_kind[1:]
    two_pair = check_two_pair(list_of_cards)
    if two_pair[0]:
        return f"Two pair, {two_pair[1][0]}s and {two_pair[1][1]}s", 4, two_pair[1:]
    pair = check_pair(list_of_cards)
    if pair[0]:
        return f"A pair of {pair[1][0]}s", 3, pair[1:]
    else:
        high_card = check_high_card(list_of_cards)
        return f"High card {high_card[0]}", 2, high_card


def compare(hero, villain):
    my_hand = check_trick(hero)
    your_hand = check_trick(villain)
    if my_hand[1] > your_hand[1]:
        return 1
    elif my_hand[1] < your_hand[1]:
        return 0
    else:
        for i in range(2, len(my_hand)):
            tie_break_hero = my_hand[i]
            tie_break_villain = your_hand[i]
            for j in range(len(my_hand[i])):
                if tie_break_hero[j] > tie_break_villain[j]:
                    return 1
                elif tie_break_hero[j] < tie_break_villain[j]:
                    return 0
    return 0.5


def check_flush(list_of_cards):
    flush = True
    first_card = list_of_cards[0]
    for card in list_of_cards:
        if card.suit != first_card.suit:
            flush = False
    card_values = [card.value for card in list_of_cards]
    card_values.sort(reverse=True)
    return flush, card_values


def check_straight(list_of_cards):
    straight = True
    card_values = [card.value for card in list_of_cards]
    card_values.sort()
    if card_values[4] - card_values[3] == 9:
        card_values[4] = 1
        card_values.sort()
    for i in range(4):
        if card_values[i+1] - card_values[i] != 1:
            straight = False
    high_card = card_values[4]
    return straight, (high_card,)


def check_pair(list_of_cards):
    card_values = [card.value for card in list_of_cards]
    card_values.sort(reverse=True)
    paired_cards = []
    for i in range(4):
        if card_values[i+1] == card_values[i]:
            paired_cards.append(card_values[i])
    if len(paired_cards) == 1:
        pair = paired_cards[0]
        card_values.remove(pair)
        card_values.remove(pair)
        return True, (pair,), card_values
    return False, []


def check_three(list_of_cards):
    card_values = [card.value for card in list_of_cards]
    card_values.sort(reverse=True)
    paired_cards = []
    for i in range(4):
        if card_values[i + 1] == card_values[i]:
            paired_cards.append(card_values[i])
    if len(paired_cards) == 2:
        triple = paired_cards[0]
        match = paired_cards[1]
        if triple == match:
            card_values.remove(triple)
            card_values.remove(triple)
            card_values.remove(triple)
            return True, (triple,), card_values
    return False, []


def check_two_pair(list_of_cards):
    card_values = [card.value for card in list_of_cards]
    card_values.sort(reverse=True)
    paired_cards = []
    for i in range(4):
        if card_values[i + 1] == card_values[i]:
            paired_cards.append(card_values[i])
    if len(paired_cards) == 2:
        first = paired_cards[0]
        second = paired_cards[1]
        if first != second:
            card_values.remove(first)
            card_values.remove(first)
            card_values.remove(second)
            card_values.remove(second)
            paired_cards.sort(reverse=True)
            return True, paired_cards, card_values
    return False, []


def check_quads(list_of_cards):
    card_values = [card.value for card in list_of_cards]
    card_values.sort(reverse=True)
    paired_cards = []
    for i in range(4):
        if card_values[i + 1] == card_values[i]:
            paired_cards.append(card_values[i])
    if len(paired_cards) == 3:
        if paired_cards[0] == paired_cards[1] == paired_cards[2]:
            card_values.remove(paired_cards[0])
            card_values.remove(paired_cards[0])
            card_values.remove(paired_cards[0])
            card_values.remove(paired_cards[0])
            return True, (paired_cards[0],), card_values
    return False, []


def check_full_house(list_of_cards):
    card_values = [card.value for card in list_of_cards]
    card_values.sort(reverse=True)
    paired_cards = []
    for i in range(4):
        if card_values[i + 1] == card_values[i]:
            paired_cards.append(card_values[i])
    if len(paired_cards) == 3:
        if not (paired_cards[0] == paired_cards[1] == paired_cards[2]):
            paired_cards.sort()
            if paired_cards[0] == paired_cards[1]:
                over, under = paired_cards[0], paired_cards[2]
            elif paired_cards[2] == paired_cards[1]:
                over, under = paired_cards[2], paired_cards[0]
            else:
                over, under = paired_cards[0], paired_cards[1]
            card_values.remove(over)
            card_values.remove(over)
            card_values.remove(under)
            return True, (over, under)
    return False, []


def check_high_card(list_of_cards):
    card_values = [card.value for card in list_of_cards]
    card_values.sort(reverse=True)
    return card_values


def choose_five(list_of_cards):
    possibilities = tuple(combinations(list_of_cards, 5))
    best = possibilities[0]
    for trick in possibilities:
        comparison = compare(trick, best)
        if comparison == 1:
            best = trick
    return best


def check_equity_vs_range(my_hand, pack, possible_hands, house_cards=()):
    hand = my_hand.tuple
    wins = 0
    total = 0
    iterations = 100
    if len(house_cards) == 3:
        remaining = 2
    elif len(house_cards) == 4:
        remaining = 1
    elif len(house_cards) == 5:
        remaining = 0
        # iterations = 1
    else:
        remaining = 5
    leftover = [card for card in pack.cards if pack.cards[card]]
    houses = set(combinations(leftover, remaining))
    for nowt in range(iterations):
        if len(houses) == 0:
            break
        house = houses.pop()
        for card in house:
            pack.deal_card(card)
        possible_hands.refresh()
        villain_hands = [hand for hand in possible_hands.hands if possible_hands.hands[hand]]
        for villain_hole in villain_hands:
            hero = hand + house + house_cards
            villain = villain_hole.tuple + house + house_cards
            hero_final = choose_five(hero)
            villain_final = choose_five(villain)
            result = compare(hero_final, villain_final)
            wins += result
            total += 1
        for card in house:
            pack.add_cards(card)
        # houses.remove(house)
        # print(wins * 100 / total)
    possible_hands.refresh()
    return wins * 100 / total


def check_equity_vs_range_generator(my_hand, pack, possible_hands, house_cards=()):
    # wins_by = {}
    # loses_to = {}
    hand = my_hand.tuple
    wins = 0
    total = 0
    load = 0
    # iterations = 999999
    if len(house_cards) == 3:
        remaining = 2
    elif len(house_cards) == 4:
        remaining = 1
    elif len(house_cards) == 5:
        remaining = 0
        # iterations = 1
    else:
        remaining = 5
    leftover = [card for card in pack.cards if pack.cards[card]]
    houses = set(combinations(leftover, remaining))
    set_size = len(houses)
    for nowt in range(set_size):
        # if len(houses) == 0:
        #     break
        house = houses.pop()
        load += 1
        # print(load/set_size)
        for card in house:
            pack.deal_card(card)
        possible_hands.refresh()
        villain_hands = [hand for hand in possible_hands.hands if possible_hands.hands[hand]]
        for villain_hole in villain_hands:
            hero = hand + house + house_cards
            villain = villain_hole.tuple + house + house_cards
            hero_final = choose_five(hero)
            villain_final = choose_five(villain)
            result = compare(hero_final, villain_final)
            # if result[0] == 1:
            #     if wins_by.get(result[1]):
            #         wins_by[result[1]] += 1
            #     else:
            #         wins_by[result[1]] = 1
            # elif result[0] == 0:
            #     if loses_to.get(result[1]):
            #         loses_to[result[1]] += 1
            #     else:
            #         loses_to[result[1]] = 1
            wins += result
            total += 1
            # for card in house:
            #     print(card.id)
            # print(f"{result} / {wins} / {total}")
        for card in house:
            pack.add_cards(card)
        # houses.remove(house)
        yield wins * 100 / total
    possible_hands.refresh()
# make this a separate function
#     first_max = 0
#     second_max = 0
#     top_winner = None
#     second_winner = None
#     for key, value in wins_by.items():
#         if value > first_max:
#             second_winner = top_winner
#             second_max = first_max
#             first_max = value
#             top_winner = key
#         elif value > second_max:
#             second_winner = key
#             second_max = value
#     print(f"{top_winner}: {wins_by[top_winner]/total}")
#     print(f"{second_winner}: {wins_by[second_winner] / total}")
#     first_max = 0
#     second_max = 0
#     top_loser = None
#     second_loser = None
#     for key, value in loses_to.items():
#         if value > first_max:
#             second_loser = top_loser
#             second_max = first_max
#             first_max = value
#             top_loser = key
#         elif value > second_max:
#             second_loser = key
#             second_max = value
#     print(f"{top_loser}: {loses_to[top_loser] / total}")
#     print(f"{second_loser}: {loses_to[second_loser] / total}")
#     print(wins_by)
#     print(loses_to)
    return


def check_equity_vs_ranges(my_hand, pack, possible_hands, house_cards=()):
    hand = my_hand.tuple
    wins = 0
    total = 0
    iterations = 50
    opponents = len(possible_hands)
    iterations = 100
    if len(house_cards) == 3:
        remaining = 2
    elif len(house_cards) == 4:
        remaining = 1
    elif len(house_cards) == 5:
        remaining = 0
        # iterations = 1
    else:
        remaining = 5
    leftover = [card for card in pack.cards if pack.cards[card]]
    houses = set(combinations(pack.cards, remaining))
    for nowt in range(iterations):
        if len(houses) == 0:
            break
        house = houses.pop()
        for card in house:
            pack.deal_card(card)
        villain_keys = []
        for villain in possible_hands:
            villain.refresh()
            new_list = [hand for hand in villain.hands if villain.hands[hand]]
            villain_keys.append(new_list)
        villain_hands = []
        for i in range(iterations):
            villain_hands = set()
            for j in range(len(possible_hands)):
                possible_hands[j].refresh(pack)
                authentic = False
                while not authentic:
                    villain_hand = choice(villain_keys[j])
                    authentic = pack.possible_hands[villain_hand]
                villain_hands.add(villain_hand.tuple)
                for card in villain_hand.tuple:
                    pack.deal_card(card)
                    # print(f"deal: {card.id}")
            hero = hand + house + house_cards
            hero_final = choose_five(hero)
            sharing = 0
            loss = False
            for villain_hole in villain_hands:
                villain = villain_hole + house + house_cards
                villain_final = choose_five(villain)
                result = compare(hero_final, villain_final)
                if result == 0:
                    loss = True
                    break
                elif result == 1/2:
                    sharing += 1
            if not loss:
                wins += (opponents + 1 - sharing)/(opponents + 1)
                # for villain_hole in villain_hands:
                #     for card in villain_hole:
                #         print(card.id)
                # print((opponents - sharing)/opponents)
            total += 1
            for antagonist in villain_hands:
                for card in antagonist:
                    pack.add_cards(card)
                    # print(f"add: {card.id}")
        for card in house:
            pack.add_cards(card)
            # print(f"add: {card.id}")
        # print(wins * 100 / total)
    return wins * 100 / total


def ask_revision(selection):
    """WIP"""
    ranks_rev = []
    two_ranks_rev = []
    one_suit_rev = []
    two_suits_rev = []
    if input("revise range:") == "yes":
        while True:
            response = input("ranks:")
            if response == "":
                break
            ranks_rev.append(response.upper())
        while True:
            response = input("two ranks:")
            if response == "":
                break
            two_ranks_rev.append(response.upper())
        while True:
            response = input("one_suit:")
            if response == "":
                break
            one_suit_rev.append(short_suits[response.upper()])
        while True:
            response = input("two_suits:")
            if response == "":
                break
            two_suits_rev.append(short_suits[response.upper()])
        if ranks_rev or two_ranks_rev or one_suit_rev or two_suits_rev:
            print(two_ranks_rev)
            selection.revise(ranks=ranks_rev, two_ranks=two_ranks_rev, one_suit=one_suit_rev, two_suits=two_suits_rev)
            return True
    return False

# -----------WIP-------------------------------------------------#


def ask_bet(hand, pack, selection, house):
    """WIP"""
    old_possibilities = [hand for hand in selection.hands if selection.hands[hand]]
    dummy_set = {card for card in selection.removed_hands}
    old_names = list(selection.hand_names)
    again = input("shove?")
    while again == "yes":
        pot = int(input("pot:"))
        stake = int(input("stake:"))
        for card in house:
            print(card.id)
        print("What does villain call with?")
        ask_revision(selection)
        new_possibilities = [hand for hand in selection.hands if selection.hands[hand]]
        fold = 1 - (len(new_possibilities) / len(old_possibilities))
        equity = check_equity_vs_range(hand, pack, selection, house)
        ev = find_ev(pot, stake, equity, fold)
        print(f"Expected Value: {ev}")
        print(selection.hand_names)
        print(old_names)
        print(fold)
        selection.removed_hands = dummy_set
        selection.refresh(pack)
        again = input("again?")
    return


def required_fold_percentage(pot, stake):
    folds = {}
    for i in range(0, 10):
        equity = i/10
        folds[str(equity)] = (stake - equity * (pot + 2 * stake)) / (pot + stake - equity * (pot + 2 * stake))
        print(f"{equity} vs. calling hands: Proportion of Villain range that must fold: "
              f"{(stake - equity * (pot + 2 * stake)) / (pot + stake - equity * (pot + 2 * stake))}")
    return folds


def fold_required(pot, stake, equity):
    equity /= 100
    if not stake:
        return
    folds = (stake - equity * (pot + 2 * stake)) / (pot + stake - equity * (pot + 2 * stake))
    if not (0 <= folds <= 1):
        return "any"
    else:
        return f"required fold percentage: {folds}"


def find_ev(pot, stake, equity, fold):
    equity /= 100
    # print(pot)
    # print(equity)
    # print(stake)
    # print(fold)
    ev = fold * pot + (1 - fold) * (equity * (pot + stake) - (1 - equity) * stake)
    return ev


def call_calculator():
    pass


def find_optimum_bet(equity, fold):
    max_ev = 0
    bet_expect = {}
    best_bet = ""
    for bet in range(0, 200):
        ev = find_ev(100, bet, equity, fold)
        bet_expect[f"{bet}%"] = ev
        if ev > max_ev:
            best_bet = f"{bet}%"
            max_ev = ev
    return best_bet, max_ev, bet_expect


def check_equity_vs_range_generator_test(my_hand, pack, possible_hands, house_cards=()):
    hand = my_hand.tuple
    wins = 0
    total = 0
    villain_wins = 0
    iterations = 999999
    if len(house_cards) == 3:
        remaining = 2
    elif len(house_cards) == 4:
        remaining = 1
    elif len(house_cards) == 5:
        remaining = 0
        # iterations = 1
    else:
        remaining = 5
    leftover = [card for card in pack.cards if pack.cards[card]]
    houses = set(combinations(leftover, remaining))
    set_size = len(houses)
    for nowt in range(iterations):
        if len(houses) == 0:
            break
        house = houses.pop()
        for card in house:
            pack.deal_card(card)
        possible_hands.refresh()
        villain_hands = [hand for hand in possible_hands.hands if possible_hands.hands[hand]]
        for villain_hole in villain_hands:
            for card in villain_hole:
                pack.deal_card(card)
            hero = hand + house + house_cards
            villain = villain_hole.tuple + house + house_cards
            hero_final = choose_five(hero)
            villain_final = choose_five(villain)
            result = compare(hero_final, villain_final)
            wins += result[0]
            total += 1
            for card in house:
                print(card.id)
            print(f"{result} / {wins} / {total}")
            ######################
            villain = hand + house + house_cards
            hero = villain_hole.tuple + house + house_cards
            hero_final = choose_five(hero)
            villain_final = choose_five(villain)
            result = compare(hero_final, villain_final)
            villain_wins += result[0]
            # total += 1
            # for card in house:
            #     print(card.id)
            print(f"{result} / {villain_wins} / {total}")
            ################################################
        for card in house:
            pack.add_cards(card)
        # houses.remove(house)
        yield wins * 100 / total, total/set_size
    possible_hands.refresh()
# make this a separate function
#     first_max = 0
#     second_max = 0
#     top_winner = None
#     second_winner = None
#     for key, value in wins_by.items():
#         if value > first_max:
#             second_winner = top_winner
#             second_max = first_max
#             first_max = value
#             top_winner = key
#         elif value > second_max:
#             second_winner = key
#             second_max = value
#     print(f"{top_winner}: {wins_by[top_winner]/total}")
#     print(f"{second_winner}: {wins_by[second_winner] / total}")
#     first_max = 0
#     second_max = 0
#     top_loser = None
#     second_loser = None
#     for key, value in loses_to.items():
#         if value > first_max:
#             second_loser = top_loser
#             second_max = first_max
#             first_max = value
#             top_loser = key
#         elif value > second_max:
#             second_loser = key
#             second_max = value
#     print(f"{top_loser}: {loses_to[top_loser] / total}")
#     print(f"{second_loser}: {loses_to[second_loser] / total}")
#     print(wins_by)
#     print(loses_to)
    return