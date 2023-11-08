from buttons import *
import tkinter as tk


class RangeFilter(ttk.Frame):
    """
    Create a RangeFilter widget for filtering or displaying hands based on criteria.

    Args:
        manager: The parent GUI manager.
        villain_range: The opponent's hand range.
        range_display: The widget for displaying the hand range.
        mode (str): 'filter' for filtering, 'show' for displaying.
        *args, **kwargs: Additional arguments for the ttk.Frame constructor.
    """
    def __init__(self, manager, villain_range, range_display, mode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.manager = manager
        self.villain_range = villain_range
        self.selected_hands = set()
        self.clicked_hands = set()
        self.selected_hands_count = tk.StringVar()
        self.selected_hands_count.set('0 selected')
        self.range_display = range_display
        self.draws = {}

        # Create a label based on the mode
        label_text = 'Tick what folds' if self.mode == 'filter' else 'Tick what calls'
        ttk.Label(self, text=label_text).grid(column=0, row=0, pady=self.manager.small_pad)

        # Define the filter criteria based on game data
        if len(self.manager.game_data['house']) < 3:
            self.filter = {}
        else:
            self.draws = check_draws(self.villain_range, self.manager.game_data['house'])
            self.filter = {'Straight Flush': tk.IntVar(),
                           'Quads': tk.IntVar(),
                           'Full House': tk.IntVar(),
                           'Nut Flush': tk.IntVar(),
                           'Flush': tk.IntVar(),
                           'Straight': tk.IntVar(),
                           'Three of a Kind': tk.IntVar(),
                           'Top Two Pair': tk.IntVar(),
                           'Mid Two Pair': tk.IntVar(),
                           'Bottom Two Pair': tk.IntVar(),
                           'Overpair': tk.IntVar(),
                           'Top Pair': tk.IntVar(),
                           'Mid Pair': tk.IntVar(),
                           'Bottom Pair': tk.IntVar(),
                           'Underpair': tk.IntVar(),
                           }
            if len(self.manager.game_data['house']) < 5:
                self.filter['Flush Draw'] = tk.IntVar()
                self.filter['Double-ended straight'] = tk.IntVar()
                self.filter['Gutshot Straight Draw'] = tk.IntVar()
                self.filter['Two Overcards'] = tk.IntVar()
                self.filter['One Overcard'] = tk.IntVar()
            if len(self.manager.game_data['house']) < 4:
                self.filter['Backdoor Flush Draw'] = tk.IntVar()
                self.filter['Three in a row'] = tk.IntVar()
            self.filter['Missed'] = tk.IntVar()

        # Create check buttons for filter criteria
        for count, category in enumerate(self.filter):
            check_button = ttk.Checkbutton(self, text=category, variable=self.filter[category],
                                           command=self.check_button_pressed)
            check_button.grid(column=0, row=count + 1)

        # Create the "Filter" button
        self.filter_button = ttk.Button(self, text='Fold', command=self.filter_hands)
        self.filter_button.grid(column=0, row=len(self.filter) + 3, pady=self.manager.large_pad)

        # Display the number of hands and the count of selected hands
        self.number_of_hands = tk.StringVar()
        number_of_hands = len([hand for hand in self.villain_range.hands if self.villain_range.hands[hand]])
        self.number_of_hands.set(f'{number_of_hands} hands')
        ttk.Label(self, textvariable=self.number_of_hands).grid(column=0, row=len(self.filter) + 1,
                                                                pady=self.manager.small_pad)
        ttk.Label(self, textvariable=self.selected_hands_count).grid(column=0, row=len(self.filter) + 2,
                                                                     pady=self.manager.small_pad)

    def house_hit(self, strength, hand):
        """
        Check if the hand category 'hits' the current community cards' strength.

        Args:
            strength (str): The strength category to check.
            hand: The hand to check.

        Returns:
            bool: True if the hand hits the specified strength category, otherwise False.
        """
        if strength == 'Flush Draw':
            return self.draws[hand]['flush'] == 1
        elif strength == 'Backdoor Flush Draw':
            return self.draws[hand]['flush'] == 2
        elif strength == 'Double-ended straight':
            return self.draws[hand]['straight'] == 2
        elif strength == 'Gutshot Straight Draw':
            return self.draws[hand]['straight'] == 1
        elif strength == 'Three in a row':
            return self.draws[hand]['run-of-three']
        elif strength == 'Two Overcards':
            return self.draws[hand]['overcards'] == 2
        elif strength == 'One Overcard':
            return self.draws[hand]['overcards'] == 1
        elif strength == 'Missed':
            missed = True
            for draw in self.filter:
                if draw != 'Missed' and self.house_hit(draw, hand):
                    missed = False
            return missed
        else:
            return self.draws[hand]['made'] == strength

    def filter_hands(self):
        """
        Filter the hands based on selected criteria and update the display.

        This method filters the hands in the opponent's hand range based on the selected criteria
        and updates the range display accordingly. It also refreshes the number of remaining hands,
        stops ongoing calculations, and clears the selected hands set.

        """
        for hand in self.selected_hands:
            self.villain_range.removed_hands.add(hand)
        self.villain_range.refresh()
        self.manager.stop_calculating()

        # Update the number of remaining hands
        number_of_hands = len([hand for hand in self.villain_range.hands if self.villain_range.hands[hand]])
        self.number_of_hands.set(f'{number_of_hands} hands')
        self.selected_hands_count.set('0 selected')

        # Refresh the range display
        self.range_display.refresh()

        # Configure the buttons with highlight functionality
        for button in self.range_display.buttons:
            button.configure(command=lambda i=button: i.highlight(self))

        # Clear the selected hands set
        self.selected_hands = set()

    def check_button_pressed(self):
        """
        Handle the event when a check button is pressed.

        This method is called when a check button is pressed. It updates the set of selected hands based on the clicked
        check buttons,
        checks if they meet the specified criteria, and highlights the corresponding buttons accordingly.

        If in 'show' mode, it checks if the selected hands meet the criteria for displaying.
        If in 'filter' mode, it checks if the selected hands meet the criteria for filtering.

        The method also updates the label showing the count of selected hands.

        """
        self.selected_hands = set()
        for hand in self.clicked_hands:
            self.selected_hands.add(hand)
        n = 0
        for button in self.range_display.buttons:
            if self.mode == 'show':
                on_the_block = False
                for hand in button.hands:
                    if hand in self.clicked_hands:
                        on_the_block = True
                    for strength in self.filter:
                        if self.filter[strength].get() and self.house_hit(strength, hand):
                            on_the_block = True
                            self.selected_hands.add(hand)
                            n += 1
                            break
                    # opportunity to use a counter to show when only some hands in a button have hit requirement
            elif self.mode == 'filter':
                on_the_block = False
                for hand in button.hands:
                    hand_fold = True
                    for strength in self.filter:
                        if not self.filter[strength].get() and self.house_hit(strength, hand):
                            hand_fold = False
                    if hand_fold:
                        self.selected_hands.add(hand)
                        n += 1
                        on_the_block = True
            else:
                on_the_block = None
                print("this shouldn't happen")
            if on_the_block:
                button.configure(style='Highlighted.Hand.TButton')
            else:
                button.configure(style=button.default_style)
        self.selected_hands_count.set(f'{len(self.selected_hands)} selected')

    def refresh(self):
        """
        Refresh the draws based on the current community cards.
        """
        self.draws = check_draws(self.villain_range, self.manager.game_data['house'])


class RangeDisplay(ttk.Frame):
    """
    Create a RangeDisplay widget for displaying hands within a hand range.

    Args:
        manager: The parent GUI manager.
        villain_range: The opponent's hand range.
        *args, **kwargs: Additional arguments for the ttk.Frame constructor.
    """

    def __init__(self, manager, villain_range, *args, **kwargs):
        super().__init__(relief=tk.RAISED, style='Range.TFrame', padding=manager.small_pad, *args, **kwargs)
        self.manager = manager
        self.villain_range = villain_range
        self.unsuited_hands = [hand for hand in self.villain_range.hands
                               if self.villain_range.hands[hand] and hand.suited == '']
        self.suited_hands = [hand for hand in self.villain_range.hands
                             if self.villain_range.hands[hand] and hand.suited == "s"]
        self.buttons = []
        self.selected_hands = set()
        self.clicked_hands = set()
        self.selected_hands_count = tk.StringVar(value='0 selected')

        # Create a vertical separator
        separator = ttk.Separator(self, orient='vertical')
        separator.grid(column=32, row=0, rowspan=16, sticky='ns')

        # Create labels for different suits
        self.clubs_label = ttk.Label(master=self, text="♣", style='Clubs.TLabel')
        self.clubs_label.grid(column=0, row=4, padx=self.manager.small_pad)
        self.diamonds_label = ttk.Label(master=self, text="♦", style='Diamonds.TLabel')
        self.diamonds_label.grid(column=0, row=7, padx=self.manager.small_pad)
        self.hearts_label = ttk.Label(master=self, text="♥", style='Hearts.TLabel')
        self.hearts_label.grid(column=0, row=10, padx=self.manager.small_pad)
        self.spades_label = ttk.Label(master=self, text="♠", style='Spades.TLabel')
        self.spades_label.grid(column=0, row=13, padx=self.manager.small_pad)

        # Display unsuited hand buttons and all suits
        self.display_unsuited_hand_buttons()
        self.display_all_suits()

    def display_unsuited_hand_buttons(self):
        """
        Display buttons for unsuited hands.

        This method displays buttons for unsuited hands based on the available hands in the opponent's range.
        It creates HandButton widgets for each hand and arranges them in a grid.
        """
        hand_name_set = set(hand.name for hand in self.unsuited_hands)

        # Filter hands from starting_hand_ranks that are in the opponent's range
        hands = [hand for hand in starting_hand_ranks if hand in hand_name_set]

        for index, hand_name in enumerate(hands):
            col = index // 3
            row = index % 3

            # Create a new HandButton widget and add it to the list of buttons
            new_button = HandButton(master=self, manager=self.manager, hand_name=hand_name,
                                    villain_range=self.villain_range)
            self.buttons.append(new_button)

            # Grid placement and styling
            new_button.grid(column=col + 1, row=row, sticky="sew",
                            ipady=self.manager.button * (self.villain_range.range_density[hand_name] - 1))

    def display_suited_hand_buttons(self, suit, row):
        """
        Display buttons for suited hands of a specific suit.

        This method displays buttons for suited hands of a specific suit, arranging them in a grid.

        Args:
            suit (str): The suit to display buttons for.
            row (int): The row in the grid where the buttons should be placed.
        """
        # Filter suited hands by the specified suit and sort them by hand ranking
        hands = [hand for hand in self.suited_hands if hand.card_1.suit == suit]
        hands.sort(key=lambda hand: starting_hand_ranks[hand.name])

        for index, hand in enumerate(hands):
            col_index = index // 3
            row_index = index % 3
            style = f'{suit}.Hand.TButton'

            # Create a new SuitedHandButton widget and add it to the list of buttons
            new_button = SuitedHandButton(master=self, manager=self.manager, hand=hand, style=style,
                                          villain_range=self.villain_range)
            self.buttons.append(new_button)

            # Grid placement and styling
            new_button.grid(column=1 + col_index, row=row + row_index, sticky='nsew')

    def display_all_suits(self):
        """
        Display buttons for all four suits.

        This method displays buttons for all four suits (Clubs, Diamonds, Hearts, and Spades) by calling
        the `display_suited_hand_buttons` method for each suit.
        """
        for index, suit in enumerate(suits):
            # Calculate the row position based on the index of the suit and display suited hand buttons
            self.display_suited_hand_buttons(suit, 3 * index + 3)

    def refresh(self):
        """
        Refresh the RangeDisplay widget.

        This method clears the existing buttons, updates the list of unsuited and suited hands in the range,
        and then displays the updated buttons.
        """
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        # Update the list of unsuited and suited hands based on the villain's hand range
        self.unsuited_hands = [hand for hand in self.villain_range.hands
                               if self.villain_range.hands[hand] and hand.suited == '']
        self.suited_hands = [hand for hand in self.villain_range.hands
                             if self.villain_range.hands[hand] and hand.suited == "s"]
        # Display the updated buttons for unsuited hands and all suits
        self.display_unsuited_hand_buttons()
        self.display_all_suits()


class CallingRangeDisplay(ttk.Frame):
    """
    Create a CallingRangeDisplay widget for displaying the hands that the villain calls with.

    Args:
        manager: The parent GUI manager.
        villain_range: The opponent's hand range.
        *args, **kwargs: Additional arguments for the ttk.Frame constructor.
    """
    def __init__(self, manager, villain_range, *args, **kwargs):
        super().__init__(relief=tk.RAISED, style='Range.TFrame', padding=manager.small_pad, *args, **kwargs)
        self.manager = manager
        self.villain_range = villain_range

        # Initialize lists to store unsuited and suited hands
        self.unsuited_hands = [hand for hand in self.villain_range.hands
                               if self.villain_range.hands[hand] and hand.suited == '']
        self.suited_hands = [hand for hand in self.villain_range.hands
                             if self.villain_range.hands[hand] and hand.suited == "s"]
        self.buttons = []
        self.calling_hands = []
        self.counter = 0

        # Create a vertical separator
        separator = ttk.Separator(self, orient='vertical')
        separator.grid(column=32, row=0, rowspan=16, sticky='ns')

        # Create a frame for displaying calling hands (updated to filter)
        self.calling_hands_frame = ttk.Frame(self, style='Range.TFrame')
        self.calling_hands_frame.grid(column=33, row=0, padx=self.manager.large_pad, rowspan=15, sticky='n')

        # now defunct, to be removed
        self.villain_calls_with = ttk.Label(self.calling_hands_frame, text='Hands Villain Calls With:')
        self.villain_calls_with.grid(column=1, row=0, columnspan=10, pady=self.manager.small_pad,
                                     padx=self.manager.small_pad, sticky='n')

        # Create a RangeFilter widget for selecting calling hands
        self.filter = RangeFilter(master=self.calling_hands_frame, manager=self.manager,
                                  villain_range=self.villain_range, range_display=self, mode='show')
        self.filter.filter_button.destroy()
        self.filter.grid(column=0, row=0, rowspan=19)

        # Create a label for the initial villain range
        initial_range = ttk.Label(self, text='Initial Villain Range:')
        initial_range.grid(column=0, row=0, columnspan=33, padx=self.manager.small_pad, pady=self.manager.small_pad)

        # Create labels for different suits
        self.clubs_label = ttk.Label(master=self, text="♣", style='Clubs.TLabel')
        self.clubs_label.grid(column=0, row=5, padx=self.manager.small_pad)

        self.diamonds_label = ttk.Label(master=self, text="♦", style='Diamonds.TLabel')
        self.diamonds_label.grid(column=0, row=8, padx=self.manager.small_pad)

        self.hearts_label = ttk.Label(master=self, text="♥", style='Hearts.TLabel')
        self.hearts_label.grid(column=0, row=11, padx=self.manager.small_pad)

        self.spades_label = ttk.Label(master=self, text="♠", style='Spades.TLabel')
        self.spades_label.grid(column=0, row=14, padx=self.manager.small_pad)

        # Display hand buttons
        self.display_unsuited_hand_buttons()
        self.display_all_suits()

    def display_unsuited_hand_buttons(self):
        """
        Display buttons for unsuited starting hands.

        This method displays buttons for unsuited starting hands in the CallingRangeDisplay widget.
        It creates a button for each unsuited hand, based on the hands in the villain's range.

        """
        # Create a set of hand names for unsuited hands in the villain's range
        hand_name_set = set(hand.name for hand in self.unsuited_hands)

        # Filter starting hand names that match those in the villain's range
        hands = [hand for hand in starting_hand_ranks if hand in hand_name_set]

        for index, hand_name in enumerate(hands):
            # Calculate the column and row for button placement
            col = index // 3
            row = index % 3

            # Create a new HandButton for the unsuited hand and add it to the list of buttons
            new_button = HandButton(master=self, manager=self.manager, hand_name=hand_name,
                                    villain_range=self.villain_range)
            self.buttons.append(new_button)

            # Place the button in the appropriate grid cell
            new_button.grid(column=col + 1, row=row + 1, sticky="S",
                            ipady=self.manager.button * (self.villain_range.range_density[hand_name] - 1))

    def display_suited_hand_buttons(self, suit, row):
        """
        Display buttons for suited starting hands of a specific suit.

        This method displays buttons for suited starting hands of a specific suit in the CallingRangeDisplay widget.
        It creates a button for each suited hand that matches the specified suit.

        Args:
            suit (str): The suit of the starting hands to display ('c', 'd', 'h', or 's').
            row (int): The row in the grid where the buttons should be displayed.

        """
        # Filter suited hands that match the specified suit
        hands = [hand for hand in self.suited_hands if hand.card_1.suit == suit]

        for index, hand in enumerate(hands):
            # Calculate the column and row index for button placement
            col_index = index // 3
            row_index = index % 3

            # Define the style for the button based on the suit
            style = f'{suit}.Hand.TButton'

            # Create a new SuitedHandButton for the suited hand and add it to the list of buttons
            new_button = SuitedHandButton(master=self, manager=self.manager, hand=hand, style=style,
                                          villain_range=self.villain_range)
            self.buttons.append(new_button)

            # Place the button in the appropriate grid cell
            new_button.grid(column=1 + col_index, row=row + 1 + row_index)

    def display_all_suits(self):
        """
        Display buttons for suited starting hands of all four suits.

        This method displays buttons for suited starting hands of all four suits ('c', 'd', 'h', and 's') in the
        CallingRangeDisplay widget. It calls the display_suited_hand_buttons method for each suit to create the buttons.

        """
        for index, suit in enumerate(suits):
            # Calculate the row position for displaying suited hands of the current suit
            row_position = 3 * index + 3

            # Display buttons for suited hands of the current suit
            self.display_suited_hand_buttons(suit, row_position)

    def refresh(self):
        """
        Refresh the Calling Range Display by clearing and redrawing the buttons.

        This method refreshes the Calling Range Display widget by first destroying all existing buttons, resetting
        counters, and then redrawing the buttons based on the current villain's range, including unsuited and suited
        hands.

        """
        # Destroy all existing buttons
        for button in self.buttons:
            button.destroy()

        # Reset the counter and clear the buttons list
        self.counter = 0
        self.buttons = []

        # Update the list of unsuited and suited hands based on the current villain's range
        self.unsuited_hands = [hand for hand in self.villain_range.hands
                               if self.villain_range.hands[hand] and hand.suited == '']
        self.suited_hands = [hand for hand in self.villain_range.hands
                             if self.villain_range.hands[hand] and hand.suited == "s"]

        # Redraw the buttons for unsuited and suited hands
        self.display_unsuited_hand_buttons()
        self.display_all_suits()


class SummarySidebar(ttk.Frame):
    """
    Create a widget for displaying a summary of the current game state.

    Args:
        manager: The parent GUI manager.
        *args, **kwargs: Additional arguments for the ttk.Frame constructor.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.blank = get_blank_card(self.manager.small_card)
        self.hand_frame = ttk.Frame(self)
        self.house_frame = ttk.Frame(self)
        self.hand_frame.grid(row=0, column=0, pady=self.manager.small_pad)
        self.house_frame.grid(column=0, row=2, pady=self.manager.small_pad)
        self.equity_label = ttk.Label(self)
        self.equity_label.grid(column=0, row=1)
        self.labels = []
        self.images = []

    def refresh(self):
        """
        Refresh the summary sidebar by updating displayed player hand, community cards, and equity information.

        This method clears the existing labels and images, then updates the sidebar with the player's hand, community
        cards,
        and equity information if available. It also binds events to labels for user interaction.

        """
        # Clear existing labels and images
        for label in self.labels:
            label.destroy()
        self.labels = []
        self.images = []

        if self.manager.game_data['hand']:
            # Display player's hand
            image_1 = rescale(self.manager.game_data['hand'].card_1.raw_image, self.manager.small_card)
            image_1 = ImageTk.PhotoImage(image_1)
            self.images.append(image_1)
            image_2 = rescale(self.manager.game_data['hand'].card_2.raw_image, self.manager.small_card)
            image_2 = ImageTk.PhotoImage(image_2)
            self.images.append(image_2)
            label_1 = ttk.Label(self.hand_frame, image=image_1)
            label_2 = ttk.Label(self.hand_frame, image=image_2)
            label_1.grid(column=0, row=0, pady=1)
            label_2.grid(column=0, row=1, pady=1)
        else:
            # If no player hand available, display blank cards
            label_1 = ttk.Label(self.hand_frame, image=self.blank)
            label_1.grid(column=0, row=0, pady=1)
            label_2 = ttk.Label(self.hand_frame, image=self.blank)
            label_2.grid(column=0, row=1, pady=1)
        self.labels.append(label_1)
        self.labels.append(label_2)

        label_1.bind("<Button-1>", lambda _: self.manager.notebook.select(self.manager.tabs['add_hero_hand']))
        label_2.bind("<Button-1>", lambda _: self.manager.notebook.select(self.manager.tabs['add_hero_hand']))

        house_size = len(self.manager.game_data['house'])
        for index, card in enumerate(self.manager.game_data['house']):
            # Display community cards
            image = rescale(card.raw_image, self.manager.small_card)
            image = ImageTk.PhotoImage(image)
            self.images.append(image)
            label = ttk.Label(self.house_frame, image=image)
            label.grid(column=0, row=index, pady=1)
            self.labels.append(label)
            label.bind("<Button-1>", lambda _: self.manager.notebook.select(self.manager.tabs['update_house']))

        for i in range(5 - house_size):
            # Display blank cards for empty community card slots
            label = ttk.Label(self.house_frame, image=self.blank)
            label.grid(column=0, row=5 - i, pady=1)
            self.labels.append(label)
            label.bind("<Button-1>", lambda _: self.manager.notebook.select(self.manager.tabs['update_house']))

        if self.manager.game_data['equity']:
            # Update the equity label with the player's equity
            self.equity_label.configure(textvariable=self.manager.game_data['equity']['hero'])
        self.update()
