from tkinter import *
from functions import *
from data import *
import copy

FANCY_FONT = ("Courier", 20, "bold")
NORMAL_FONT = ("Courier", 12, "bold")
BUTTON_FONT = ("Liber", 12, "bold")
THEME_COLOR = '#5BC2E7'
SECONDARY_COLOR = '#5B7CE7'
TERTIARY_COLOR = '#5BE7C6'
ACOLOUR = '#E7805B'
BCOLOUR = '#E75BC2'
CCOLOUR = '#C2E75B'
DCOLOUR = '#C65BE7'
FCOLOUR = '#E7805B'
GCOLOUR = '#7CE75B'

BG_BUTTON = FCOLOUR
FG_BUTTON = GCOLOUR
ACTIVE_BG_BUTTON = BCOLOUR
ACTIVE_FG_BUTTON = TERTIARY_COLOR

BG_TILE = THEME_COLOR
TITLE_COLOUR = SECONDARY_COLOR


class CardsDisplay(Frame):
    def __init__(self, master, size):
        super().__init__(master=master, bd=5, relief=RAISED, bg=TERTIARY_COLOR)
        self.window = master
        self.card_labels = []
        self.size = size

    def add_card(self, card):
        contained = len(self.card_labels)
        if contained < self.size:
            new_label = Label(master=self, text=card.id, fg=suit_colours[card.suit], font=FANCY_FONT,
                              bg=CCOLOUR)
            self.card_labels.append(new_label)
            new_label.grid(column=contained, row=0)


class RankList(Listbox):
    """A listbox with card rank information"""
    def __init__(self, master):
        super().__init__(master=master, height=13, exportselection=False, font=NORMAL_FONT, bd=5, relief=RAISED,
                         highlightcolor=TERTIARY_COLOR, highlightbackground=SECONDARY_COLOR, fg=GCOLOUR,
                         bg=SECONDARY_COLOR)
        for index, value in enumerate(values):
            self.insert(index, value)


class SuitList(Listbox):
    """A listbox with card suit information"""
    def __init__(self, master):
        super().__init__(master=master, height=4, exportselection=False, font=NORMAL_FONT, bg=SECONDARY_COLOR,
                         fg=GCOLOUR, bd=5, relief=RAISED, highlightcolor=TERTIARY_COLOR,
                         highlightbackground=SECONDARY_COLOR)
        for index, value in enumerate(suits):
            self.insert(index, value)


class HeroHand(Frame):
    """displays the hand selected by user"""
    def __init__(self, window, selector):
        super().__init__(window, width=110, height=120, bd=5, relief=RAISED)
        self.grid_propagate(FALSE)
        self.config(background=BG_TILE)
        self.hand = None
        self.selector = selector
        self.label = Label(master=self, text="Hero Hand", font=NORMAL_FONT, bg=BG_TILE, fg=TITLE_COLOUR)
        self.label.grid(column=0, row=0)
        # self.hand_label = Label(master=self)
        # self.hand_label.grid(column=0, row=1)
        # self.hand_text = Text(master=self, bg="yellow", highlightthickness=0, state="disabled")
        # self.hand_text.grid(column=0, row=1)
        self.card_display = CardsDisplay(self, 2)
        self.card_display.config(bg=SECONDARY_COLOR)
        self.card_display.grid(column=0, row=1)
        self.cards = []
        self.card_names = []
        self.add_card_button = Button(master=self, text="Add", command=self.add_card, font=BUTTON_FONT,
                                      background=BG_BUTTON, activebackground=ACTIVE_BG_BUTTON, fg=FG_BUTTON,
                                      activeforeground=ACTIVE_FG_BUTTON
                                      )
        self.add_card_button.grid(column=0, row=2)

        # self.cancel_first_card_button = Button(text="Cancel")
        # self.cancel_first_card_button.grid(column=0, row=3)
        #
        # self.cancel_second_card_button = Button(text="Cancel")
        # self.cancel_second_card_button.grid(column=1, row=3)

    def add_card(self):
        card = self.selector.card
        if len(self.cards) < 2 and self.selector.pack.cards[card]:
            self.cards.append(card)
            self.card_names.append(card.id)
            self.selector.pack.deal_card(card)
            self.card_display.add_card(card)
            # self.hand_label.config(text=", ".join(self.card_names))
            # self.hand_text.configure(state="normal")
            # self.hand_text.insert("end", card.id, font=suit_colours[card.suit])
            if len(self.cards) == 2:
                self.hand = Hand(self.cards[0], self.cards[1])


class Selector(Frame):
    """used to select a card to add to hand or house"""
    def __init__(self, window, pack):
        super().__init__(window, width=570, height=330, bd=5, relief=RAISED)
        self.grid_propagate(False)
        self.config(background=BG_TILE)
        self.pack = pack
        self.rank = None
        self.suit = None
        self.card = None
        self.rank_select = RankList(master=self)
        self.rank_select.bind("<<ListboxSelect>>", self.choose_rank)
        self.rank_select.grid(column=0, row=0)
        self.suit_select = SuitList(master=self)
        self.suit_select.bind("<<ListboxSelect>>", self.choose_suit)
        self.suit_select.grid(column=1, row=0)

    def choose_suit(self, _):
        self.suit = self.suit_select.get(self.suit_select.curselection())
        self.select_card()
        self.rank_select.config(bg=suit_colours[self.suit])
        # self.config(bg=suit_colours[self.suit])
        self.suit_select.config(bg=suit_colours[self.suit])

    def choose_rank(self, _):
        self.rank = self.rank_select.get(self.rank_select.curselection())
        self.select_card()

    def select_card(self):
        if self.rank and self.suit:
            self.card = Card(self.rank, self. suit)


class House(Frame):
    """displays house cards chosen by user"""
    def __init__(self, window, selector):
        super().__init__(window, width=210, height=120, bd=5, relief=RAISED)
        self.grid_propagate(FALSE)
        self.window = window
        self.selector = selector
        self.cards = []
        self.card_names = []
        self.title = Label(master=self, text="House", font=NORMAL_FONT, bg=BG_TILE, justify=CENTER,
                           fg=TITLE_COLOUR)
        self.title.grid(column=0, row=0)
        # self.house_label = Label(master=self)
        # self.house_label.grid(column=0, row=1)
        self.house_text = CardsDisplay(master=self, size=5)
        self.house_text.grid(column=0, row=1)
        self.config(background=BG_TILE)
        self.add_button = Button(master=self, text="Add", command=self.add_card, font=BUTTON_FONT,
                                 background=BG_BUTTON, activebackground=ACTIVE_BG_BUTTON, fg=FG_BUTTON,
                                 activeforeground=ACTIVE_FG_BUTTON
                                 )
        self.add_button.grid(column=0, row=2, padx=80)

    def add_card(self):
        card = self.selector.card
        if len(self.cards) < 5 and self.selector.pack.cards[card]:
            self.cards.append(card)
            self.card_names.append(card.id)
            self.selector.pack.deal_card(card)
            # self.house_label.config(text=", ".join(self.card_names))
            self.house_text.add_card(card)
            self.window.refresh_ranges()


class RangeSelector(Frame):
    """sliders to choose tightness, add range button (later multiple ranges)"""
    def __init__(self, window):
        super().__init__(window, bg=BG_TILE, bd=5, relief=RAISED, width=570,
                         height=470)
        self.grid_propagate(False)
        self.top_label = Label(master=self, text="Top of Range", bg=BG_TILE, font=FANCY_FONT, fg=TITLE_COLOUR)
        self.top_label.grid(column=0, row=0)
        self.bottom_label = Label(master=self, text="Bottom of Range", bg=BG_TILE, font=FANCY_FONT, fg=TITLE_COLOUR)
        self.bottom_label.grid(column=1, row=0)
        self.top_scale = Scale(master=self, from_=0, to=99, command=self.top_used, length=400, bg=BG_TILE,
                               font=FANCY_FONT, highlightthickness=0, activebackground=FG_BUTTON,
                               troughcolor=BG_BUTTON, fg=DCOLOUR
                               )
        self.top_scale.grid(column=0, row=1, padx=100)
        self.bottom_scale = Scale(master=self, from_=1, to=100, command=self.bottom_used, length=400, bg=BG_TILE,
                                  font=FANCY_FONT, highlightthickness=0, activebackground=FG_BUTTON,
                                  troughcolor=BG_BUTTON, fg=DCOLOUR)
        self.bottom_scale.grid(column=1, row=1)
        self.bottom_scale.set(100)
        self.top = 0
        self.bottom = 100

    def top_used(self, value):
        top = int(value)
        self.top = top
        self.bottom_scale.config(from_=top+1)

    def bottom_used(self, value):
        bottom = int(value)
        self.bottom = bottom
        self.top_scale.config(to=bottom-1)


RANGE_DISPLAY_BG = SECONDARY_COLOR


class RangeDisplay(Frame):
    def __init__(self, master, villain_range):
        super().__init__(master, bg=RANGE_DISPLAY_BG, bd=5, relief=RAISED)
        # self.grid_propagate(False)
        self.range = villain_range
        self.unsuited_hands = [hand for hand in starting_hand_ranks
                               if hand in self.range.hand_names and len(hand) == 2]
        self.suited_hand_names = [hand for hand in starting_hand_ranks
                                  if hand in self.range.hand_names and len(hand) == 3]
        self.suited_hands = [hand for hand in self.range.hands
                             if self.range.hands[hand] and hand.suited == "s"]
        self.buttons = []
        # self.unsuited_label = Label(master=self, text="Unsuited")
        # self.unsuited_label.grid(column=0, row=0)
        self.clubs_label = Label(master=self, text="♣", fg="green", bg=RANGE_DISPLAY_BG, font=FANCY_FONT)
        self.clubs_label.grid(column=0, row=1)
        self.diamonds_label = Label(master=self, text="♦", fg="blue", bg=RANGE_DISPLAY_BG, font=FANCY_FONT)
        self.diamonds_label.grid(column=0, row=2)
        self.hearts_label = Label(master=self, text="♥", fg="red", bg=RANGE_DISPLAY_BG, font=FANCY_FONT)
        self.hearts_label.grid(column=0, row=3)
        self.spades_label = Label(master=self, text="♠", fg="black", bg=RANGE_DISPLAY_BG, font=FANCY_FONT)
        self.spades_label.grid(column=0, row=4)
        self.display_unsuited_hand_buttons()
        self.display_all_suits()

    def display_unsuited_hand_buttons(self):
        for index, hand in enumerate(self.unsuited_hands):
            new_button = CardButton(master=self, hand_name=hand)
            self.buttons.append(new_button)
            new_button.grid(column=index+1, row=0, sticky="S")

    def display_suited_hand_buttons(self, suit, row):
        hands = [hand for hand in self.suited_hands if hand.card_1.suit == suit]
        for index, hand in enumerate(hands):
            new_button = SuitedCardButton(master=self, hand=hand, bg=suit_colours[suit])
            self.buttons.append(new_button)
            new_button.grid(column=index+1, row=row)

    def display_all_suits(self):
        for index, suit in enumerate(suits):
            self.display_suited_hand_buttons(suit, index + 1)

    def refresh(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        self.unsuited_hands = [hand for hand in starting_hand_ranks
                               if hand in self.range.hand_names and len(hand) == 2]
        self.suited_hand_names = [hand for hand in starting_hand_ranks
                                  if hand in self.range.hand_names and len(hand) == 3]
        self.suited_hands = [hand for hand in self.range.hands
                             if self.range.hands[hand] and hand.suited == "s"]
        self.display_unsuited_hand_buttons()
        self.display_all_suits()
        # print(self.range.range_density)


class SuitedCardButton(Button):
    def __init__(self, master: RangeDisplay, hand, bg):
        super().__init__(master=master, text=hand.name[:2], command=self.remove_from_range, fg="white",
                         bg=bg, width=2, height=1, font=NORMAL_FONT)
        self.display = master
        self.hand = hand

    def remove_from_range(self):
        self.display.range.removed_hands.add(self.hand)
        # print(self.hand.long_name)
        self.display.range.refresh()
        self.display.refresh()


class CardButton(Button):
    def __init__(self, master: RangeDisplay, hand_name):
        super().__init__(master=master, text=hand_name, command=self.remove_from_range, width=2,
                         height=master.range.range_density[hand_name], bg="grey", fg="white", font=NORMAL_FONT)
        self.display = master
        self.hand_name = hand_name

    def remove_from_range(self):
        for hand in self.display.range.hands:
            if hand.name == self.hand_name:
                self.display.range.removed_hands.add(hand)
        self.display.range.refresh()
        self.display.refresh()


class RangeManager(Frame):
    """Buttons with hand names to remove from range, think about suits
    consider splitting suited and unsuited, with suited allowing removal from specific suit
    challenge: remove AK if A not Clubs"""
    def __init__(self, window, pack, selector):
        super().__init__(window, bg=BG_TILE, width=1250, height=450, bd=5, relief=RAISED)
        self.grid_propagate(False)
        self.range = None
        self.pack = pack
        self.title_pane = Frame(master=self, bg="orange")
        self.selector = selector
        self.create_range_button = Button(master=self.title_pane, text="Create Range", command=self.create_range,
                                          font=BUTTON_FONT, fg=FG_BUTTON, bg=BG_BUTTON,
                                          activeforeground=ACTIVE_FG_BUTTON, activebackground=ACTIVE_BG_BUTTON)
        self.create_range_button.grid(column=0, row=0)
        self.range_display = None
        self.refresh_range_button = Button(master=self.title_pane, text="Refresh", command=self.refresh,
                                           font=BUTTON_FONT, fg=FG_BUTTON, bg=BG_BUTTON,
                                           activebackground=ACTIVE_BG_BUTTON, activeforeground=ACTIVE_FG_BUTTON)
        self.refresh_range_button.grid(column=1, row=0)
        self.title_pane.grid(column=0, row=0, sticky="w")

    def create_range(self):
        if self.range_display:
            self.range_display.destroy()
        new_range = Range(self.pack, self.selector.top, self.selector.bottom)
        self.range = new_range
        self.range_display = RangeDisplay(master=self, villain_range=self.range)
        self.range_display.grid(column=0, row=1, columnspan=2)

    def refresh(self):
        self.range.refresh()
        self.range_display.refresh()


class EquityCalculator(Frame):
    """Calculate, Stop (temp), show equity"""
    def __init__(self, window, hero_hand, range_manager, house):
        super().__init__(window, bg=THEME_COLOR, width=250, height=120, bd=5, relief=RAISED)
        self.grid_propagate(False)
        self.hand = hero_hand
        self.range_manager = range_manager
        self.house = house
        self.equity = StringVar()
        self.label = Label(master=self, text="Equity:", bg=THEME_COLOR, font=FANCY_FONT, fg=TITLE_COLOUR)
        self.label.grid(column=0, row=0)
        self.equity_label = Label(master=self, textvariable=self.equity, font=FANCY_FONT, bg=THEME_COLOR,
                                  fg=DCOLOUR)
        self.equity_label.grid(column=1, row=0)
        self.calculate_button = Button(master=self, text="Calculate", command=self.calculate, font=BUTTON_FONT,
                                       background=BG_BUTTON, activebackground=ACTIVE_BG_BUTTON, fg=FG_BUTTON,
                                       activeforeground=ACTIVE_FG_BUTTON)
        self.calculate_button.grid(column=0, row=1)
        self.stop_button = Button(master=self, text="Stop", command=self.stop_calculating, font=BUTTON_FONT,
                                  background=BG_BUTTON, activebackground=ACTIVE_BG_BUTTON, fg=FG_BUTTON,
                                  activeforeground=ACTIVE_FG_BUTTON)
        self.stop_button.grid(column=1, row=1)
        self.calculating = False

    def calculate(self):
        self.calculating = True
        self.range_manager.range.refresh()
        pack = copy.deepcopy(self.range_manager.pack)
        my_hand = self.hand.hand
        current_house = tuple(self.house.cards)
        villain_range = copy.deepcopy(self.range_manager.range)
        villain_range.pack = pack
        for i in check_equity_vs_range_generator(my_hand, pack, villain_range, current_house):
            if not self.calculating:
                break
            self.equity.set(f"{round(i, 2)}%")
            self.update()

    def stop_calculating(self):
        self.calculating = False


class BetAnalyser(Frame):
    """create new Range (calling range), ask for pot and bet sizes and calculate eV"""
    def __init__(self, window, range_manager, hero_hand, house):
        super().__init__(window, bg=BG_TILE, bd=5, relief=RAISED, height=470, width=1250)
        self.grid_propagate(False)
        self.calling_range_display = None
        self.calling_range = None
        self.full_range = None
        self.stake = None
        self.pot = None
        self.pack = None
        self.house = house
        self.hero_hand = hero_hand
        self.range_manager = range_manager
        self.title_pane = Frame(master=self)
        self.choose_calling_range_label = Label(master=self.title_pane, text="Choose calling range:    ",
                                                font=NORMAL_FONT, bg=BG_TILE, fg=TITLE_COLOUR)
        self.ev_label = Label(master=self, bg=BG_TILE, font=FANCY_FONT, fg=DCOLOUR)
        self.calculate_button = Button(master=self, text="Calculate", command=self.calculate, font=BUTTON_FONT,
                                       fg=FG_BUTTON, bg=BG_BUTTON, activeforeground=ACTIVE_FG_BUTTON,
                                       activebackground=ACTIVE_BG_BUTTON)
        self.pot_label = Label(master=self.title_pane, text="Pot:", bg=BG_TILE, font=NORMAL_FONT, fg=TITLE_COLOUR)
        self.stake_label = Label(master=self.title_pane, text="Stake:", bg=BG_TILE, font=NORMAL_FONT, fg=TITLE_COLOUR)
        self.pot_box = Entry(master=self.title_pane, width=5)
        self.stake_box = Entry(master=self.title_pane, width=5)
        self.pot_box.insert(END, "0")
        self.stake_box.insert(END, "0")
        self.stake_box.grid_propagate(False)
        self.bet_button = Button(master=self, text="Bet", command=self.bet, font=BUTTON_FONT, fg=FG_BUTTON,
                                 bg=BG_BUTTON, activebackground=ACTIVE_BG_BUTTON, activeforeground=ACTIVE_FG_BUTTON)
        # self.pot_label.grid(column=0, row=0)
        # self.pot_box.grid(column=0, row=1, sticky="N")
        # self.stake_box.grid(column=1, row=1, sticky="N")
        self.bet_button.grid(column=0, row=2)
        # self.stake_label.grid(column=1, row=0)

    def bet(self):
        self.calling_range = copy.deepcopy(self.range_manager.range)
        self.pack = copy.deepcopy(self.range_manager.pack)
        self.calling_range_display = RangeDisplay(self, self.calling_range)
        self.calling_range_display.grid(column=0, row=1, columnspan=5, sticky="w")
        self.choose_calling_range_label.grid(column=0, row=0)
        self.calculate_button.grid(column=0, row=3, pady=10)
        self.bet_button.destroy()
        self.pot_box.grid(column=2, row=0, sticky="w")
        self.pot_label.grid(column=1, row=0, sticky="e")
        self.stake_label.grid(column=3, row=0, sticky="e")
        self.stake_box.grid(column=4, row=0, sticky="w")
        self.title_pane.grid(column=0, row=0, sticky="w", columnspan=2)

    def calculate(self):
        self.pack = copy.deepcopy(self.range_manager.pack)
        self.calling_range.pack = self.pack
        self.full_range = copy.deepcopy(self.range_manager.range)
        self.stake = float(self.stake_box.get())
        self.pot = float(self.pot_box.get())
        hand = self.hero_hand.hand
        old_size = sum(self.full_range.range_density[hand] for hand in self.full_range.range_density)
        new_size = sum(self.calling_range.range_density[hand] for hand in self.calling_range.range_density)
        house_cards = tuple(self.house.cards)
        # print(self.full_range.range_density)
        # print(old_size)
        # print(new_size)
        # print(self.calling_range.range_density)
        fold = 1 - (new_size / old_size)
        equity = check_equity_vs_range(hand, self.pack, self.calling_range, house_cards)
        ev = find_ev(self.pot, self.stake, equity, fold)
        # print(find_optimum_bet(equity, fold)[:2])
        # print(find_optimum_bet(equity, fold)[2])
        self.ev_label.config(text=f"Fold%: {round((fold*100), 2)}, Equity%: {round(equity, 2)}, eV: {round(ev, 2)}")
        self.ev_label.grid(column=1, row=3, columnspan=3)
        # print(f"Fold%: {round((fold*100), 2)}\nEquity%: {round(equity, 2)}\neV: {round(ev, 2)}")


class Trick(Frame):
    def __init__(self, window):
        super().__init__(window, bg=BCOLOUR, bd=5, relief=RIDGE)
        self.pack = Pack()
        self.window = window
        # self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.dealer = Selector(self, self.pack)
        self.hero_hand = HeroHand(self, self.dealer)
        self.house = House(self, self.dealer)
        self.range_selector = RangeSelector(self)
        self.range_manager = RangeManager(self, self.pack, self.range_selector)
        self.equity_calculator = EquityCalculator(self, self.hero_hand, self.range_manager, self.house)
        self.bet_analyser = BetAnalyser(self, self.range_manager, self.hero_hand, self.house)
        self.new_bet_button = Button(text="New Bet", command=self.new_bet, font=BUTTON_FONT, fg=FG_BUTTON,
                                     bg=BG_BUTTON, activeforeground=ACTIVE_FG_BUTTON, activebackground=ACTIVE_BG_BUTTON)
        self.hero_hand.grid(column=0, row=0)
        self.dealer.grid(column=0, row=1, columnspan=3)
        self.house.grid(column=1, row=0)
        self.range_selector.grid(column=0, row=2, columnspan=3)
        self.range_manager.grid(column=3, row=0, rowspan=2, sticky="w")
        self.equity_calculator.grid(column=2, row=0)
        self.bet_analyser.grid(column=3, row=2, sticky="w")
        self.new_bet_button.grid(column=0, row=5, columnspan=3)

    def new_bet(self):
        self.bet_analyser.destroy()
        self.bet_analyser = BetAnalyser(self, self.range_manager, self.hero_hand, self.house)
        self.bet_analyser.grid(column=3, row=2, sticky="w")

    def refresh_ranges(self):
        if self.range_manager.range:
            self.range_manager.refresh()
        if self.bet_analyser.calling_range:
            # print(self.bet_analyser.calling_range.range_density)
            self.bet_analyser.calling_range.pack = copy.deepcopy(self.range_manager.pack)
            self.bet_analyser.calling_range.refresh()
            # print(self.bet_analyser.calling_range.range_density)
            self.bet_analyser.calling_range_display.refresh()


class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.config(bg=SECONDARY_COLOR, padx=20, pady=20)
        self.title("Hold'em Helper")
        self.trick = Trick(self)
        self.restart_button = Button(text="Restart", command=self.restart, font=BUTTON_FONT, fg=FG_BUTTON, bg=BG_BUTTON,
                                     activebackground=ACTIVE_BG_BUTTON, activeforeground=ACTIVE_FG_BUTTON)
        self.restart_button.grid(column=0, row=0)
        self.trick.grid(column=0, row=1)
        self.state("zoomed")

    def restart(self):
        self.trick.destroy()
        self.trick = Trick(self)
        self.trick.grid(column=0, row=1)

