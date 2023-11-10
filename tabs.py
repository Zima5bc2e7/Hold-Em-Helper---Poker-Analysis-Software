import tkinter.ttk as ttk
import tkinter.messagebox as msg
from widgets import *
import copy
import time


class Tab(ttk.Frame):
    """Base class for tab frames"""
    def __init__(self, *args, **kwargs):
        super().__init__(padding=5, *args, **kwargs)
        self['relief'] = 'raised'
        self.grid_propagate(False)


class WelcomeTab(Tab):
    """
    Welcomes the user and provides a basic introduction to the application.

    Args:
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the Tab constructor.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['welcome'] = self     # Register this tab with the manager

        # Create and configure widgets
        self.message = ttk.Label(self, text="Welcome to Hold 'Em Helper", style='Title.TLabel')
        self.intro = ttk.Label(self, text=welcome_message, style='Guide.TLabel', justify='center')
        self.start_button = ttk.Button(self, text='Get Started', command=self.get_started)

        # Pack widgets to display
        self.message.pack(pady=self.manager.small_pad)
        self.intro.pack(pady=self.manager.small_pad)
        self.start_button.pack(pady=self.manager.small_pad)

    def get_started(self):
        """Switch to the Hero Hand tab to start using the application."""
        self.manager.notebook.select(self.manager.tabs['add_hero_hand'])

    def refresh(self):
        # this page has no dynamic elements but refresh is called when any tab is opened
        pass


class OverviewTab(Tab):
    """
    Displays information about the current game situation.

    This tab provides an overview of the current game situation, including player information and relevant game details.

    Args:
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the ttk.Frame constructor.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['overview'] = self

        # Initialise variables
        self.blank = get_blank_card(self.manager.small_card)
        self.labels = []
        self.player_bars = {}
        self.in_depth = InDepthTab(master=self, manager=self.manager)

        # Create widgets
        self.instructions = ttk.Label(self, text=overview_text, style='Guide.TLabel', justify='right')
        self.next_tab = ttk.Button(self, text='Done', command=self.move_on)
        self.players_frame = ttk.Frame(self, height=int(manager.height * 0.42), width=int(manager.width * 0.4))
        self.players_frame['relief'] = 'raised'
        self.players_frame.grid_propagate(False)

        # Place widgets in the layout
        self.in_depth.grid(column=0, row=0, rowspan=4, pady=self.manager.small_pad, padx=self.manager.small_pad)
        self.instructions.grid(column=1, row=0, sticky='ne')
        self.next_tab.grid(column=1, row=1, sticky='ne')
        self.players_frame.grid(column=0, row=4)

        self.columnconfigure(1, weight=1)

    def move_on(self):
        """
        Switch to the 'Bet for Value' tab.

        This method is called when the 'Done' button is clicked on the OverviewTab. It navigates to the 'Bet for Value'
        tab in the GUI manager's notebook.

        """
        self.manager.notebook.select(self.manager.tabs['bet_for_value'])

    @threaded
    def calculate(self):
        """
        Calculate the equity of each player based on game data.

        This method clears existing labels, checks for necessary data, and creates display widgets for equity
        calculations.

        If the required data is available, it calculates equity for the hero and each opponent, updates the display,
        and allows incremental calculation to avoid freezing the GUI.

        """
        # Clear existing labels
        for label in self.labels:
            label.destroy()

        # Check if necessary data is available
        if self.manager.game_data['hand'] and self.manager.game_data['ranges']:
            self.manager.calculating['equity'] = True
            self.manager.game_data['equity'] = {}

            # Create display widgets for the user
            self.manager.game_data['equity']['hero'] = tk.StringVar()
            hero_equity_label = ttk.Label(self.players_frame, textvariable=self.manager.game_data['equity']['hero'],
                                          width=6, anchor='e')
            hero_equity_label.grid(column=1, row=0, padx=self.manager.small_pad, sticky='w')
            self.labels.append(hero_equity_label)
            hero_name_label = ttk.Label(self.players_frame, text='Hero', width=8, anchor='e')
            self.labels.append(hero_name_label)
            hero_name_label.grid(column=0, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad, sticky='w')
            hero_bar = ttk.Label(self.players_frame, style='Bar.TLabel')
            self.labels.append(hero_bar)
            self.player_bars['hero'] = hero_bar
            hero_bar.grid(column=2, row=0, sticky='w', padx=self.manager.small_pad)

            # Create display widgets for each opponent
            for count, villain in enumerate(self.manager.game_data['ranges']):
                self.manager.game_data['equity'][count] = tk.StringVar()
                new_label = ttk.Label(self.players_frame, textvariable=self.manager.game_data['equity'][count],
                                      anchor='e', width=6)
                self.labels.append(new_label)
                new_label.grid(column=1, row=count + 1, padx=self.manager.small_pad, pady=self.manager.small_pad,
                               sticky='w')
                player_label = ttk.Label(self.players_frame, text=f'Villain {count + 1}', width=8, anchor='e')
                self.labels.append(player_label)
                player_label.grid(column=0, row=count + 1, padx=self.manager.small_pad, sticky='w')
                player_bar = ttk.Label(self.players_frame, style='Bar.TLabel')
                self.labels.append(player_bar)
                player_bar.grid(column=2, row=count + 1, sticky='w', padx=self.manager.small_pad)
                self.player_bars[count] = player_bar

            # Create copies of game data for equity calculation
            ranges = copy.deepcopy(self.manager.game_data['ranges'])
            deck = copy.deepcopy(self.manager.game_data['deck'])
            for villain in ranges:
                villain.deck = deck

            # Iterate through equity calculations
            n = 0
            for i in calculate_equity(self.manager.game_data['hand'], deck, ranges,
                                      tuple(self.manager.game_data['house'])):
                if not self.manager.calculating['equity']:
                    break
                else:
                    for player in self.manager.game_data['equity']:
                        self.manager.game_data['equity'][player].set(f'{round(i[0][player], 1)}%')
                        equity = i[0][player]
                        if equity >= 50:
                            colour = 'green'
                        elif equity >= 20:
                            colour = 'orange'
                        else:
                            colour = 'red'
                        self.player_bars[player].configure(width=int(equity / 2), background=colour)
                        self.manager.game_data['hands_breakdown'] = i[1]
                        n += 1
                    if n == 100:
                        self.in_depth.refresh()
                    if n % 100 == 0:
                        self.in_depth.calculate()
                    self.update()

    def refresh(self):
        """
        Refresh the In-Depth tab and update information.

        This method refreshes the In-Depth tab display and updates the information as needed. It may be used to
        periodically update the tab's contents, particularly when equity calculations are in progress.

        """
        self.update()
        if self.manager.calculating['equity']:
            # Wait for the in-depth display to be ready before reloading it
            self.in_depth.after(5000, self.in_depth.refresh)


class AddHeroHandTab(Tab):
    """
    Interface for adding the cards the user was dealt.

    This tab provides an interface for the user to add the two cards they were dealt in the poker game.
    The user can click on the cards to select them.

    Args:
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the ttk.Frame constructor.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['add_hero_hand'] = self

        # Create a frame for displaying user's cards
        self.display_frame = ttk.Frame(self)

        # Create buttons for displaying user's first and second cards
        self.first_card = DisplayCardButton(master=self.display_frame, manager=self.manager)
        self.second_card = DisplayCardButton(master=self.display_frame, manager=self.manager)

        # Grid placement for card buttons
        self.first_card.grid(column=0, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad)
        self.second_card.grid(column=1, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad)
        self.display_frame.grid(column=5, row=0, columnspan=3, rowspan=2, pady=self.manager.large_pad)

        self.displayed_cards = [self.first_card, self.second_card]
        self.card_buttons = []

        # Instructions Label
        self.instructions = ttk.Label(self, style='Guide.TLabel', text=card_selection_text, justify='right')
        self.instructions.grid(column=10, row=0, columnspan=3, sticky='ne')

        # Button to move to the next tab
        self.next_button = ttk.Button(self, text='Done', command=self.move_on)
        self.next_button.grid(column=10, row=1, columnspan=3, sticky='ne')

        # Create card buttons for user to select their hand
        for card in self.manager.game_data['deck'].cards:
            new_button = CardButton(master=self, card=card, manager=self.manager, tab=self)
            self.card_buttons.append(new_button)
            if card.suit == 'Diamonds':
                row = 3
            elif card.suit == 'Clubs':
                row = 2
            elif card.suit == 'Hearts':
                row = 4
            else:
                row = 5
            col = card.value - 2
            new_button.grid(row=row, column=col, padx=self.manager.small_pad, pady=self.manager.small_pad)

            for col in range(13):
                self.columnconfigure(col, weight=1)

    def move_on(self):
        """
        Move to the next tab for range selection.

        This method is called when the user clicks the "Done" button to move to the next tab for range selection.
        It checks if both user's cards are selected, and if not, it asks for confirmation to proceed.

        """
        # Check if both user's cards are selected
        if not (self.first_card.card and self.second_card.card):
            # If not, ask for confirmation to proceed
            proceed = msg.askokcancel(title='No hand selected', message='Continue anyway?')
            if not proceed:
                return
        # Move to the next tab for range selection
        self.manager.notebook.select(self.manager.tabs['range_select'])

    def refresh(self):
        """
        Refresh the tab's content.

        This method updates the displayed cards' images and refreshes card buttons.
        It is called when the user switches to this tab to ensure the displayed cards reflect the user's selections.

        """
        # Update the displayed cards' images
        for button in self.displayed_cards:
            if button.card:
                button.card_image = ImageTk.PhotoImage(rescale(button.card.raw_image, self.manager.large_card))
                button.configure(image=button.card_image)
            else:
                button.configure(image=button.image)
        # Refresh card buttons
        for button in self.card_buttons:
            button.refresh()


class UpdateHouseTab(Tab):
    """
    Interface for updating the community cards (house).

    Args:
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the Tab constructor.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['update_house'] = self
        self.house_frame = ttk.Frame(self)

        # Create buttons for displaying the community cards (house)
        self.first_card = DisplayCardButton(master=self.house_frame, manager=self.manager)
        self.second_card = DisplayCardButton(master=self.house_frame, manager=self.manager)
        self.third_card = DisplayCardButton(master=self.house_frame, manager=self.manager)
        self.fourth_card = DisplayCardButton(master=self.house_frame, manager=self.manager)
        self.fifth_card = DisplayCardButton(master=self.house_frame, manager=self.manager)

        # Grid positions for displaying community cards
        cards_grid = [
            self.first_card, self.second_card, self.third_card, self.fourth_card, self.fifth_card
        ]
        for index, card_button in enumerate(cards_grid):
            card_button.grid(column=index, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad)

        # Place the card buttons inside a frame
        self.house_frame.grid(column=3, row=0, columnspan=7, rowspan=2, pady=self.manager.large_pad)

        # Create a list of card buttons for easy access
        self.displayed_cards = [self.first_card, self.second_card, self.third_card, self.fourth_card, self.fifth_card]

        # Create a list of card buttons for selection
        self.card_buttons = []

        # Instructions for the user
        self.instructions = ttk.Label(self, style='Guide.TLabel', text=house_selection_text, justify='right')
        self.instructions.grid(column=10, row=0, columnspan=3, sticky='ne')

        # Button to move to the next tab
        self.next_button = ttk.Button(self, text='Done', command=self.move_on)
        self.next_button.grid(column=10, row=1, columnspan=3, sticky='ne')

        # Create buttons for each card in the deck
        for card in self.manager.game_data['deck'].cards:
            new_button = CardButton(master=self, card=card, manager=self.manager, tab=self)
            self.card_buttons.append(new_button)

            # Determine the row and column for displaying the card based on suit and value
            if card.suit == 'Diamonds':
                row = 3
            elif card.suit == 'Clubs':
                row = 2
            elif card.suit == 'Hearts':
                row = 4
            else:
                row = 5
            col = card.value - 2
            new_button.grid(row=row, column=col, padx=self.manager.small_pad, pady=self.manager.small_pad)

        for col in range(13):
            self.columnconfigure(col, weight=1)

    def move_on(self):
        """
        Move to the Overview tab.

        Check if at least three community cards (flop) are selected. If not, ask for confirmation to proceed.

        This method is called when the user clicks the "Done" button to move to the Overview tab.
        """
        # Check if at least three community cards (flop) are selected
        if not (self.first_card.card and self.second_card.card and self.third_card.card):
            proceed = msg.askokcancel(title='No Flop Entered', message='Continue anyway?')
            if not proceed:
                return
        self.manager.notebook.select(self.manager.tabs['overview'])

    def refresh(self):
        """
        Refresh displayed cards and card buttons.

        This method updates the images of displayed cards and card buttons based on the selected cards and their state.
        It is called to ensure that the interface reflects the current selection of house cards.
        """
        for button in self.displayed_cards:
            if button.card:
                button.card_image = ImageTk.PhotoImage(rescale(button.card.raw_image, self.manager.large_card))
                button.configure(image=button.card_image)
            else:
                button.configure(image=button.image)
        for button in self.card_buttons:
            button.refresh()


class RangeSelectionTab(Tab):
    """
    Interface for selecting opponent ranges.

    This tab provides the user with controls to select opponent ranges by defining the top and bottom percentages of
    a range slider. Users can commit the selected range, view the number of villains added, and the count of selected
    hands in the range.

    Args:
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the ttk.Frame constructor.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['range_select'] = self
        self.range = None
        self.range_display = None
        self.columnconfigure(2, weight=1)

        # Variables for top and bottom range sliders
        self.top = tk.StringVar(self, value='0%')
        self.bottom = tk.StringVar(self, value='100%')

        # Labels for the top and bottom range sliders
        self.scales_frame = ttk.Frame(self, width=int(self.manager.width * 0.3), height=int(self.manager.height * 0.15))
        self.scales_frame['relief'] = 'raised'
        for row in range(4):
            self.scales_frame.rowconfigure(row, weight=1)

        for col in range(3):
            self.scales_frame.columnconfigure(col, weight=1)

        self.scales_frame.grid_propagate(False)
        self.top_label = ttk.Label(master=self.scales_frame, text="Top of Range")
        self.top_label.grid(column=0, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad, sticky='w')
        self.top_value = ttk.Label(master=self.scales_frame, textvariable=self.top, width=5, anchor='e')
        self.top_value.grid(column=1, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad, sticky='w')
        self.bottom_label = ttk.Label(master=self.scales_frame, text="Bottom of Range")
        self.bottom_label.grid(column=0, row=2, padx=self.manager.small_pad, pady=self.manager.small_pad, sticky='w')
        self.bottom_value = ttk.Label(master=self.scales_frame, textvariable=self.bottom, width=5, anchor='e')
        self.bottom_value.grid(column=1, row=2, padx=self.manager.small_pad, pady=self.manager.small_pad, sticky='w')

        # Sliders for defining the range
        self.top_scale = ttk.Scale(master=self.scales_frame, from_=0, to=99, command=self.top_used,
                                   length=self.manager.scale_length)
        self.top_scale.grid(column=0, row=1, columnspan=2, sticky='ew', padx=self.manager.small_pad,
                            pady=self.manager.small_pad)
        self.bottom_scale = ttk.Scale(master=self.scales_frame, from_=1, to=100, command=self.bottom_used)
        self.bottom_scale.grid(column=0, row=3, columnspan=2, sticky='ew', padx=self.manager.small_pad,
                               pady=self.manager.small_pad)
        self.bottom_scale.set(100)
        self.top_scale.bind('<ButtonRelease-1>', self.release_mouse_button)
        self.bottom_scale.bind('<ButtonRelease-1>', self.release_mouse_button)

        self.scales_frame.grid(column=0, row=0, rowspan=2, sticky='nsew', padx=self.manager.small_pad,
                               pady=self.manager.small_pad)

        # Instructions for the user
        self.instructions = ttk.Label(self, text=selector_text, style='Guide.TLabel', justify='right')
        self.instructions.grid(column=2, row=0, sticky='ne')

        # Button to commit the selected range
        self.add_range_button = ttk.Button(self.scales_frame, text='Commit', command=self.commit_range)
        self.add_range_button.grid(column=2, row=0, rowspan=4, sticky='nsew', pady=self.manager.large_pad,
                                   padx=self.manager.large_pad)

        # Label for displaying the number of villains added
        self.number_of_villains = tk.StringVar(value='0 villains added')
        self.current_villains = ttk.Label(self, textvariable=self.number_of_villains)
        self.current_villains.grid(column=1, row=3, padx=self.manager.small_pad, pady=self.manager.small_pad)

        # Label for displaying the count of selected hands
        self.hand_count = ttk.Label(self)
        self.hand_count.grid(column=0, row=3)

        # Button to move to the next tab
        self.next_button = ttk.Button(self, text='Done', command=self.move_on)
        self.next_button.grid(column=2, row=1, padx=self.manager.small_pad, sticky='ne')

        self.columnconfigure(2, weight=1)

    def move_on(self):
        """
        Move to the next tab for updating the community cards (house) after checking if any opponents (villains) are
        added.

        If no opponents are added, the user is asked for confirmation to continue. If confirmed, the user proceeds to
        the tab for updating the community cards (house).
        """
        # Check if any opponents (villains) are added, ask for confirmation if none
        if not self.manager.game_data['ranges']:
            proceed = msg.askokcancel(title='No opponents added', message='Continue anyway?')
            if not proceed:
                return
        self.manager.notebook.select(self.manager.tabs['update_house'])

    def top_used(self, value):
        """
        Update the top range value and adjust the bottom slider accordingly.

        Args:
            value (string): The value selected on the top range slider.
        """
        top = int(float(value))
        self.top.set(f'{top}%')
        self.bottom_scale.config(from_=top + 1)

    def bottom_used(self, value):
        """
        Update the bottom range value and adjust the top slider accordingly.

        Args:
            value (string): The value selected on the bottom range slider.
        """
        bottom = int(float(value))
        self.bottom.set(f'{bottom}%')
        self.top_scale.config(to=bottom - 1)

    def show(self):
        """
        Highlight hands within the selected range based on top and bottom sliders.

        This method identifies and highlights hands within the range defined by the top and bottom sliders.
        It updates the display to reflect the selected hands.
        """
        self.range_display.selected_hands = set()      # Clear the previously selected hands
        for button in self.range_display.buttons:
            button.configure(style=button.default_style)    # Reset button styles
            highlighted = False
            for hand in button.hands:
                if (float(self.top.get()[:-1]) / 100 <= starting_hand_ranks[hand.name]
                        <= float(self.bottom.get()[:-1]) / 100):
                    self.range_display.selected_hands.add(hand)
                    highlighted = True
            if highlighted:
                button.configure(style='Highlighted.Hand.TButton')      # Highlight buttons for selected hands
        self.range_display.selected_hands_count.set(f'{len(self.range_display.selected_hands)} selected')

    def release_mouse_button(self, _):
        """
        Handle the mouse button release event and update the displayed hands based on the range selection.

        This method is called when the mouse button is released after adjusting the top and bottom sliders.
        It triggers the display of hands within the selected range based on the slider positions.

        Args:
            _: Placeholder for the event argument (not used).
        """
        self.show()

    def commit_range(self):
        """
        Commit the selected range and add it to the list of opponent ranges.

        This method finalizes the selected range, creates a new opponent range based on the selection,
        and adds it to the list of opponent ranges in the game data.

        If there are hands within the selected range, those hands are added to the opponent's range,
        and any previously selected hands that fall within this new range are removed.
        """
        if self.range_display.selected_hands:
            villain_hands = self.range_display.selected_hands
            top = tk.IntVar(value=0)
            bottom = tk.IntVar(value=100)
            villain = Range(self.manager.game_data['deck'], top, bottom)
            for hand in villain.hands:
                villain.removed_hands.add(hand)
            for hand in villain_hands:
                villain.removed_hands.remove(hand)
            villain.refresh()
            self.manager.game_data['ranges'].append(villain)
            self.manager.stop_calculating()
            self.refresh()
        else:
            msg.showwarning("No Hands Selected",
                            "Please select one or more hands for the opponent's range before committing.")

    def refresh(self):
        """
        Reset range sliders and update the range display.

        This method resets the top and bottom range sliders to their default values and updates the range display.
        The range display provides an interface for the user to interact with and visualize the selected opponent's
        range.
        """
        # Reset the range sliders
        self.top_scale.set(0)
        self.bottom_scale.set(100)

        # Destroy the existing range display if it exists
        if self.range_display:
            self.range_display.destroy()

        # Create a new opponent range with default values
        top = tk.IntVar(value=0)
        bottom = tk.IntVar(value=100)
        # clean this up
        self.range = Range(self.manager.game_data['deck'], top, bottom)

        # Create a range display widget and place it in the layout
        self.range_display = RangeDisplay(master=self, manager=self.manager, villain_range=self.range)
        self.range_display.grid(column=0, row=2, columnspan=2, sticky='w', padx=self.manager.small_pad)

        # Update the label displaying the number of villains added
        villains = len(self.manager.game_data['ranges'])
        if villains == 1:
            self.number_of_villains.set('1 villain added')
        else:
            self.number_of_villains.set(f'{villains} villains added')

        # Configure the behavior of range display buttons
        for button in self.range_display.buttons:
            button.configure(command=lambda i=button: i.highlight(self.range_display))

        # Update the label displaying the count of selected hands
        self.hand_count.configure(textvariable=self.range_display.selected_hands_count)


class RangesTab(Tab):
    """
    Interface for managing opponent ranges.

    This class provides the user interface for managing opponent (villain) ranges. It includes a Notebook widget that
    allows the user to view and manipulate multiple opponent range displays.

    Args:
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the Tab constructor.

    Attributes:
        notebook (ttk.Notebook): The Notebook widget for displaying opponent range displays.
        remove_selected (ttk.Button): A button to remove the selected range.
        ranges (dict): A dictionary to store opponent ranges.
        filters (dict): A dictionary to store range filters.
        range_displays (dict): A dictionary to store opponent range display widgets.
        frames (list): A list to store frames for organizing range displays.
        instructions (ttk.Label): Instructions label for user guidance.
        next_button (ttk.Button): Button to move on to the next tab.

    Methods:
        remove_selected_range(): Remove the selected opponent range.
        move_on(): Move to the next tab.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['ranges'] = self

        # Create a Notebook for displaying multiple opponent range displays
        self.notebook = ttk.Notebook(self, style='Ranges.TNotebook')
        self.notebook.grid(column=0, row=1, padx=self.manager.small_pad)

        # Button for removing the selected range
        self.remove_selected = ttk.Button(self, text='Remove Selected Range', command=self.remove_selected_range)
        self.remove_selected.grid(column=0, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad)

        # Structures to store widgets
        self.ranges = {}
        self.filters = {}
        self.range_displays = {}
        self.frames = []

        # Instructions label
        self.instructions = ttk.Label(self, text=villains_text, style='Guide.TLabel', justify='right')
        self.instructions.grid(column=0, row=0, columnspan=2, sticky='ne')

        # "Done" button to move on to the next tab
        self.next_button = ttk.Button(self, text='Done', command=self.move_on)
        self.next_button.grid(column=1, row=1, sticky='ne')

        self.columnconfigure(1, weight=1)

    def move_on(self):
        """
        Move to the next tab (Update House) when the user clicks the "Done" button.

        This method is called when the user clicks the "Done" button in the RangesTab. It selects the "Update House" tab
        in the notebook, allowing the user to proceed to the next step of the application.
        """
        self.manager.notebook.select(self.manager.tabs['update_house'])

    def refresh(self):
        """
        Refresh the display of opponent ranges in the RangesTab.

        This method updates the list of opponent ranges and their corresponding RangeDisplays and RangeFilters. It
        destroys any existing frames, creates displays for each opponent's range, and adds these displays to the
        notebook for the user to manage and interact with.
        """
        # Clear the existing data
        self.ranges = {}
        self.filters = {}
        self.range_displays = {}

        # Destroy existing frames
        for frame in self.frames:
            frame.destroy()
        self.frames = []

        # Create displays for each opponent range
        for count, villain in enumerate(self.manager.game_data['ranges']):
            villain.refresh()
            new_frame = ttk.Frame(self)
            self.frames.append(new_frame)

            # Create a RangeDisplay for the opponent's range
            new_range_display = RangeDisplay(master=new_frame, manager=self.manager, villain_range=villain)
            self.range_displays[count] = new_range_display
            self.ranges[count] = villain
            new_range_display.grid(column=0, row=0, rowspan=2)
            # new_range_display.configure(width=int(self.manager.width * 0.6))

            # Create range filter for each range display
            range_filter = RangeFilter(self.manager, self.ranges[count], self.range_displays[count], 'filter',
                                       master=new_range_display)
            self.filters[count] = range_filter

            # Bind click events for range buttons
            for button in new_range_display.buttons:
                button.configure(command=lambda i=button, j=count: i.highlight(self.filters[j]))
            range_filter.grid(column=34, row=0, rowspan=15, padx=self.manager.small_pad)

            # Add the opponent's range display to the notebook
            self.notebook.add(new_frame, text=f'Villain {count + 1}')

    def remove_selected_range(self):
        """
        Remove the selected opponent range.

        This method removes the opponent range that corresponds to the currently selected tab in the notebook. It stops
        any ongoing calculations related to the removed range and destroys the frame associated with the removed range.
        After the removal, it refreshes the display of opponent ranges in the RangesTab.
        """
        if self.manager.game_data['ranges']:
            # Get the index of the currently selected tab in the notebook
            index = self.notebook.index('current')

            # Remove the opponent range at the given index
            del self.manager.game_data['ranges'][index]

            # Stop ongoing calculations for removed range
            for calculation in self.manager.calculating:
                self.manager.calculating[calculation] = False

            # Destroy the frame associated with the removed range
            self.frames[index].destroy()

        # Refresh the display of opponent ranges
        self.refresh()


class ShoveCalculatorTab(Tab):
    """
    Interface for finding the expected value of a bet.

    This class represents a tab in the application for calculating the expected value (EV) of a bet.
    Users can input the bet size and pot size and calculate the EV of shoving all-in.

    Attributes:
        manager (Manager): The main application manager.
        ranges (list): List of opponent ranges.
        frames (list): Frames for displaying opponent range information.
        range_displays (list): RangeDisplay instances for displaying opponent ranges.
        deck (Deck): A copy of the game deck for calculations.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['shove_calculator'] = self

        # Initialize class variables
        self.ranges = None
        self.frames = []
        self.range_displays = []
        self.deck = copy.deepcopy(self.manager.game_data['deck'])

        # Create a Notebook for displaying multiple range displays
        self.notebook = ttk.Notebook(self, style='Ranges.TNotebook')
        self.notebook.grid(column=0, row=1, rowspan=2, sticky='w', padx=self.manager.small_pad,
                           pady=self.manager.small_pad)

        # Labels and input fields for bet size and pot size
        self.calculation_frame = ttk.Frame(self, relief='raised', padding=self.manager.small_pad)
        bet_size_label = ttk.Label(self.calculation_frame, text='Bet Size:')
        bet_size_label.grid(column=2, row=0, padx=self.manager.small_pad)
        pot_size_label = ttk.Label(self.calculation_frame, text='Pot Size:')
        pot_size_label.grid(column=0, row=0, padx=self.manager.small_pad)
        self.bet_size = ttk.Entry(self.calculation_frame)
        self.bet_size.grid(column=3, row=0, padx=self.manager.small_pad)
        self.pot_amount = ttk.Entry(self.calculation_frame)
        self.pot_amount.grid(column=1, row=0, padx=self.manager.small_pad)
        self.bet_size.insert(tk.END, '100')
        self.pot_amount.insert(tk.END, '100')

        # Calculate button
        self.calculate_button = ttk.Button(self.calculation_frame, text='Calculate', command=self.calculate)
        self.calculate_button.grid(column=5, row=0, padx=self.manager.small_pad)

        # Reset button
        self.reset_button = ttk.Button(self.calculation_frame, text='Reset', command=self.reset)
        self.reset_button.grid(column=4, row=0, padx=self.manager.small_pad)

        # Expected value (EV) label
        ev_label = ttk.Label(self.calculation_frame, text='Expected Value vs. Checking:')
        ev_label.grid(column=6, row=0, padx=self.manager.small_pad)
        self.ev = tk.StringVar()
        self.ev_label = ttk.Label(self.calculation_frame, textvariable=self.ev, width=4, anchor='e')
        self.ev_label.grid(column=7, row=0, padx=self.manager.small_pad)
        self.calculation_frame.grid(column=0, row=0, sticky='w', padx=self.manager.small_pad,
                                    pady=self.manager.small_pad)

        # Instructions label
        self.instructions = ttk.Label(self, text=shove_calc_text, style='Guide.TLabel', justify='right')
        self.instructions.grid(column=0, row=0, columnspan=2, sticky='ne')

        # "Done" button to move on to the next tab
        self.next_button = ttk.Button(self, text='Done', command=self.move_on)
        self.next_button.grid(column=1, row=1, sticky='ne')

        self.columnconfigure(1, weight=1)

    def move_on(self):
        """
        Switch to the "RangesTab" when moving on to the next tab in the application.
        """
        self.manager.notebook.select(self.manager.tabs['ranges'])

    def reset(self):
        """
        Reset the state of the ShoveCalculatorTab, including removing any range displays, stopping ongoing calculations,
        and reconstructing range displays for each opponent (villain).
        """
        for frame in self.frames:
            frame.destroy()
        self.frames = []
        self.range_displays = []
        self.ev.set('')

        # Stop current calculation
        self.manager.calculating['shove'] = False

        # Reconstruct range displays for each villain
        for count, villain in enumerate(self.manager.game_data['ranges']):
            villain.refresh()
            new_frame = ttk.Frame(self)
            self.frames.append(new_frame)
            new_range_display = CallingRangeDisplay(master=self.frames[count],
                                                    villain_range=self.manager.game_data['ranges'][count],
                                                    manager=self.manager)
            new_range_display.villain_calls_with.destroy()
            new_range_display.grid(column=0, row=0)
            self.range_displays.append(new_range_display)
            for button in new_range_display.buttons:
                button.configure(command=lambda i=button, j=count: i.highlight(self.range_displays[j].filter))
            self.notebook.add(new_frame, text=f'Villain {count + 1}')

    def refresh(self):
        """
        Refresh the ShoveCalculatorTab by calling the reset method, effectively resetting the tab's state.
        """
        self.reset()

    @threaded
    def calculate(self):
        """
        Perform EV (Expected Value) calculation for a bet scenario.

        This method calculates the expected value of a bet based on the user's input, including the bet size,
        pot size, and opponent ranges. It updates the EV label with the result.

        It first stops any ongoing calculations, then checks if the necessary game data (hand and ranges) are available.
        It creates copies of the game data for the calculation and iterates through the range displays for each villain
        to update their ranges based on user filters. Finally, it performs the EV calculation and updates the EV label.
        """
        # Stop any ongoing calculations
        if self.manager.calculating['shove']:
            self.manager.calculating['shove'] = False

        # Pause briefly to allow the previous calculation to stop
        time.sleep(0.2)

        # Check if hand and ranges are available for calculation
        if self.manager.game_data['hand'] and self.manager.game_data['ranges']:
            self.manager.calculating['shove'] = True

            # Create copies of game data for calculation
            self.deck = copy.deepcopy(self.manager.game_data['deck'])
            initial_ranges = copy.deepcopy(self.manager.game_data['ranges'])

            # Update the packs of all villains in the initial_ranges
            for villain in initial_ranges:
                villain.deck = self.deck

            self.ranges = []
            high = tk.IntVar(value=0)
            low = tk.IntVar(value=100)

            # Iterate through the range displays for each villain
            for i, display in enumerate(self.range_displays):
                villain = Range(self.deck, high, low)

                # Remove hands from the villain's range based on the filter in the range display
                for hand in villain.hands:
                    villain.removed_hands.add(hand)
                for hand in display.filter.selected_hands:
                    villain.removed_hands.remove(hand)
                villain.refresh()
                self.ranges.append(villain)

            # Get the bet size and pot amount from the input fields
            bet = float(self.bet_size.get())
            pot = float(self.pot_amount.get())

            # Perform the EV calculation
            for j in calculate_shove_ev(self.manager.game_data['hand'], self.deck, self.ranges, pot, bet,
                                        initial_ranges, tuple(self.manager.game_data['house'])):
                if not self.manager.calculating['shove']:
                    break
                else:
                    checking_equity = float(self.manager.game_data['equity']['hero'].get()[:-1]) / 100
                    checking_ev = checking_equity * pot
                    ev_vs_checking = j - checking_ev

                    # Update the EV label with the result
                    self.ev.set(str(int(ev_vs_checking)))
                    self.update()


class BetForValueTab(Tab):
    """
    This class provides a user interface for bet and call sizing assistance.

    It assists the user in determining optimal bet and call sizes based on opponent ranges and other game parameters.
    The user can calculate maximum profitable bet size, equity, fold equity, and maximum callable bet size for
    different betting scenarios.

    This tab allows the user to input opponent ranges and other relevant game data to calculate the optimal bet and
    call sizes.
    After calculation, the tab provides information on the maximum profitable bet size, equity, fold equity, and
    maximum callable bet size for the selected betting scenario.

    The user can click the "Calculate" button to perform the calculations and view the results. Once the user has
    determined the desired bet or call size, they can click "Done" to proceed to the next tab.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.manager.tabs['bet_for_value'] = self
        self.manager.calculating['value'] = False

        # Initialise class variables
        self.ranges = None
        self.frames = []
        self.range_displays = []
        self.deck = copy.deepcopy(self.manager.game_data['deck'])

        # Notebook for opponents
        self.notebook = ttk.Notebook(self, style='Ranges.TNotebook')
        self.notebook.grid(column=0, row=1, columnspan=6, rowspan=3, sticky='w', padx=self.manager.small_pad)

        # Buttons to initialise calculation
        self.calculation_frame = ttk.Frame(self, relief='raised', padding=self.manager.small_pad)
        self.calculate_button = ttk.Button(self.calculation_frame, text='Calculate', command=self.calculate)
        self.calculate_button.grid(column=5, row=0, padx=self.manager.small_pad)
        self.reset_button = ttk.Button(self.calculation_frame, text='Reset', command=self.reset)
        self.reset_button.grid(column=4, row=0)

        # Labels to display calculated values
        self.max_bet = tk.StringVar()
        self.max_bet_label = ttk.Label(self.calculation_frame, textvariable=self.max_bet, width=18, anchor='e')
        self.max_bet_label.grid(column=0, row=0, padx=self.manager.small_pad)
        self.equity = tk.StringVar()
        self.equity_label = ttk.Label(self.calculation_frame, textvariable=self.equity, width=20, anchor='e')
        self.equity_label.grid(column=1, row=0, padx=self.manager.small_pad)
        self.fold = tk.StringVar()
        self.fold_label = ttk.Label(self.calculation_frame, textvariable=self.fold, width=10, anchor='e')
        self.fold_label.grid(column=2, row=0, padx=self.manager.small_pad)
        self.max_call = tk.StringVar()
        self.max_call_label = ttk.Label(self.calculation_frame, textvariable=self.max_call, width=16, anchor='e')
        self.max_call_label.grid(column=3, row=0, padx=self.manager.small_pad)
        self.calculation_frame.grid(column=0, row=0, padx=self.manager.small_pad, pady=self.manager.small_pad)

        # Instructions label
        self.instructions = ttk.Label(self, text=bet_helper_text, style='Guide.TLabel', justify='right')
        self.instructions.grid(column=0, row=0, columnspan=2, sticky='ne')

        # Button to move to the next tab
        self.next_button = ttk.Button(self, text='Done', command=self.move_on)
        self.next_button.grid(column=1, row=1, sticky='ne')

        self.columnconfigure(1, weight=1)

    def move_on(self):
        """
        Move to the next tab when the bet and call sizing calculations are complete.

        This method allows the user to proceed to the next tab in the interface once they have determined
        the desired bet or call size and clicked the "Done" button. The next tab is typically the "ShoveCalculatorTab"
        where additional calculations and decisions can be made.
        """
        self.manager.notebook.select(self.manager.tabs['shove_calculator'])

    def reset(self):
        """
        Reset the interface and calculations to their initial state.

        This method stops any ongoing calculations for bet and call sizing, clears existing data and frames,
        and re-initialises the range displays for each opponent. It is used to start calculations from scratch
        and refresh the interface.

        """
        # Stop any ongoing calculations
        self.manager.calculating['value'] = False

        # Remove all existing frames
        for frame in self.frames:
            frame.destroy()

        # Clear existing data
        self.frames = []
        self.range_displays = []
        self.max_bet.set('')
        self.equity.set('')
        self.fold.set('')
        self.max_call.set('')

        # Reinitialize the range displays
        for count, villain in enumerate(self.manager.game_data['ranges']):
            villain.refresh()
            new_frame = ttk.Frame(self)
            self.frames.append(new_frame)
            new_range_display = CallingRangeDisplay(master=self.frames[count],
                                                    villain_range=self.manager.game_data['ranges'][count],
                                                    manager=self.manager)
            # legacy feature no longer required
            new_range_display.villain_calls_with.destroy()

            new_range_display.grid(column=0, row=0)
            self.range_displays.append(new_range_display)
            for button in new_range_display.buttons:
                button.configure(command=lambda i=button, j=count: i.highlight(self.range_displays[j].filter))
            self.notebook.add(new_frame, text=f'Villain {count + 1}')

    def refresh(self):
        """
        Refresh the interface to its initial state.

        This method is used to reset the entire interface and calculations, effectively starting from scratch.
        It stops any ongoing calculations, clears existing data and frames, and re-initialises the range displays for
        each opponent.

        """
        self.reset()

    @threaded
    def calculate(self):
        """
        Calculate and display various values related to bet sizing and equity.

        This method performs calculations to determine the equity, fold percentage, maximum call percentage, and
        betting recommendations based on the selected hands and bet sizing. It updates the interface to display these
        calculated values.

        The calculated values are as follows:
        - Equity: The equity percentage of the hero's hand against the selected range.
        - Fold Percentage: The percentage of the opponent folding against the hero's bet.
        - Maximum Call Percentage: The maximum percentage of an opponent's hand to call the hero's bet.
        - Betting Recommendations: Recommendations for bet sizing based on equity and the current situation.

        The method stops ongoing calculations if the 'value' flag is set to False and pauses briefly between
        calculations.
        """
        # Stop ongoing calculation
        if self.manager.calculating['value']:
            self.manager.calculating['value'] = False

        # Wait for calculation to stop
        time.sleep(0.2)

        # Check if necessary data is present
        if self.manager.game_data['hand'] and self.manager.game_data['ranges']:
            self.manager.calculating['value'] = True

            # Copy data for calculation
            self.deck = copy.deepcopy(self.manager.game_data['deck'])
            initial_ranges = copy.deepcopy(self.manager.game_data['ranges'])

            # Set up ranges
            self.ranges = []
            high = tk.IntVar(value=0)
            low = tk.IntVar(value=100)
            for villain in initial_ranges:
                villain.deck = self.deck
            for i, display in enumerate(self.range_displays):

                # Initialise villain's range
                villain = Range(self.deck, high, low)
                for hand in villain.hands:
                    villain.removed_hands.add(hand)

                # Adjust the range based on the selected hands
                for hand in display.filter.selected_hands:
                    villain.removed_hands.remove(hand)
                villain.refresh()
                self.ranges.append(villain)

            # Calculate equity and bet amounts
            for j in calculate_called_equity(self.manager.game_data['hand'], self.deck, self.ranges,
                                             initial_ranges, tuple(self.manager.game_data['house'])):
                if not self.manager.calculating['value']:
                    break
                else:
                    checking_equity = float(self.manager.game_data['equity']['hero'].get()[:-1])
                    called_equity = j[0] * 100
                    fold = j[1] * 100

                    # Calculate the maximum call percentage
                    if called_equity < 100:
                        max_call = called_equity * 100 / (100 - 2 * called_equity)
                    else:
                        max_call = 999999999

                    # Calculate maximum bet amount
                    bet_amount = find_bet(called_equity, fold, 100, checking_equity, j[2])

                    # Update the interface with calculated values
                    self.equity.set(f'Equity {int(called_equity)}% vs selected')
                    self.fold.set(f'{int(fold)}% folded')
                    self.max_call.set(f'Max Call: {int(max_call)}% pot')

                    # Provide betting recommendations
                    if called_equity > 50:
                        self.max_bet.set('Any bet is profitable')
                    elif bet_amount[0] == 'Max Bet:' and bet_amount[1] <= 0:
                        self.max_bet.set('Better off checking')
                    else:
                        self.max_bet.set(f'{bet_amount[0]} {bet_amount[1]}% pot')

                    # Trigger an update of the interface
                    self.update()


class InDepthTab(Tab):
    def __init__(self, manager, *args, **kwargs):
        """
        This class displays in-depth data about the current game situation.
        It provides statistics for made hands, occurrence, win percentage, and relative win percentage.
        """
        super().__init__(height=int(manager.height * 0.45), width=int(manager.width * 0.4), *args, **kwargs)
        self.manager = manager
        self.manager.tabs['in_depth'] = self
        self.choose_player = None
        self.chosen_player = tk.StringVar()
        self.labels = []

        # Labels for different statistics
        self.made_hand_label = ttk.Label(self, text='Made Hand')
        self.occurrence_label = ttk.Label(self, text='Occurrence')
        self.win_percentage_label = ttk.Label(self, text='Wins By')
        self.relative_win_percentage_label = ttk.Label(self, text='Win rate when made')
        self.made_hand_label.grid(column=0, row=1, padx=(self.manager.small_pad, 0), pady=self.manager.small_pad,
                                  sticky='e')
        self.occurrence_label.grid(column=1, row=1, padx=(self.manager.small_pad, 0), pady=self.manager.small_pad,
                                   sticky='e')
        self.win_percentage_label.grid(column=2, row=1, padx=(self.manager.small_pad, 0), pady=self.manager.small_pad,
                                       sticky='e')
        self.relative_win_percentage_label.grid(column=3, row=1, padx=(self.manager.small_pad, 0),
                                                pady=self.manager.small_pad, sticky='e')

        # A dictionary to store hand probabilities
        self.probabilities = {}

    def setup_player_combobox(self):
        """
        Sets up a player selection combobox and binds it to the 'calculate' method when a player is selected.
        """
        # Check if a player selection combobox already exists and destroy it if it does
        if self.choose_player:
            self.choose_player.destroy()

        # Check if equity calculation is enabled
        if self.manager.calculating['equity']:
            # Create a list of player options including 'hero' and 'Villain X' for each villain
            players = ['hero'] + [f'Villain {n + 1}' for n in range(len(self.manager.game_data['equity']) - 1)]

            # Create and configure the player selection combobox
            self.choose_player = ttk.Combobox(self, values=players, textvariable=self.chosen_player)
            self.choose_player.grid(column=0, row=0, columnspan=4, padx=self.manager.small_pad,
                                    pady=self.manager.small_pad, sticky='w')
            self.choose_player.current(0)

            # Bind the 'combobox_selected' event handler to the combobox
            self.choose_player.bind('<<ComboboxSelected>>', self.combobox_selected)

            # Trigger the initial calculation when a player is selected
            self.calculate()

    def calculate(self):
        """
        Calculate and update hand statistics based on the selected player.

        This method retrieves the selected player from the combobox and calculates various hand statistics,
        including occurrence percentage, win percentage, and relative win rate percentage for each made hand.
        The calculated statistics are then updated and displayed in the user interface.
        """
        # Get the selected player from the combobox
        player = self.chosen_player.get()

        # Check if a player is selected
        if not player:
            return

        # If the selected player is not 'hero', convert it to the corresponding index
        if player != 'hero':
            player = int(player[-1]) - 1

        # Iterate through the made hands for the selected player
        for made_hand in self.manager.game_data['hands_breakdown'][player]:
            stats = self.manager.game_data['hands_breakdown'][player][made_hand]

            # Calculate and update occurrence percentage
            occurrence_raw = stats['made']
            occurrence = round(occurrence_raw * 100, 1)
            self.probabilities[made_hand]['occurs'].set(f'{occurrence}%')

            # Calculate and update win percentage
            win_percentage_raw = stats['wins']
            win_percentage = round(win_percentage_raw * 100, 1)
            self.probabilities[made_hand]['wins'].set(f'{win_percentage}%')

            # Calculate and update relative win rate percentage
            if occurrence == 0:
                relative_win_percentage = 0
            else:
                relative_win_percentage = round(win_percentage_raw * 100 / occurrence_raw, 0)

            self.probabilities[made_hand]['win_rate'].set(f'{int(relative_win_percentage)}%')

    def refresh(self):
        """
        Refresh the interface and data for displaying hand statistics.

        This method updates the interface to display hand statistics for various made hands. It creates labels for
        made hands and their corresponding statistics, such as occurrence percentage, win percentage, and relative
        win rate percentage. These statistics are updated and displayed for the selected player based on the combobox
        selection.
        """
        # Check if labels are already created
        if not self.labels:
            # Initialize a dictionary to store statistics variables for each made hand
            self.probabilities = {i: {'occurs': tk.StringVar(),
                                      'wins': tk.StringVar(),
                                      'win_rate': tk.StringVar()} for i in range(2, 11)}

            # Create labels for made hands
            for made_hand in made_hands:
                new_label = ttk.Label(self, text=made_hands[made_hand])
                new_label.grid(column=0, row=made_hand, pady=(self.manager.small_pad, 0), sticky='e')
                self.labels.append(new_label)

            # Create labels for statistics and associate them with the corresponding variables
            for made_hand in self.probabilities:
                for column, stat in enumerate(self.probabilities[made_hand]):
                    new_label = ttk.Label(self, textvariable=self.probabilities[made_hand][stat])
                    new_label.grid(column=column+1, row=made_hand, sticky='e')
                    self.labels.append(new_label)

        # Set up the player selection combobox
        self.setup_player_combobox()

    def combobox_selected(self, _):
        """
        Handle the ComboBox selection and trigger the 'calculate' method.

        This method is called when a player is selected from the ComboBox. It serves as an event handler to respond
        to the player selection by triggering the 'calculate' method, which updates the hand statistics based on the
        selected player.

        Args:
            _: The event object representing the ComboBox selection.
        """
        self.calculate()


class Analysis(ttk.Notebook):
    """
    Creates a notebook-style interface for the application.

    This class represents the main interface of the poker analysis application, which is implemented as a notebook.
    It provides a structured way to organize and present different tabs to the user for various analysis tasks.

    Args:
        manager (Manager): The main application manager.
        resize (float): The ratio by which the interface is to be resized.
        *args: Additional positional arguments to pass to the ttk.Notebook constructor.
        **kwargs: Additional keyword arguments to pass to the ttk.Notebook constructor.

    Attributes:
        manager (Manager): The main application manager responsible for coordinating various components.
        deck (Deck): The deck of cards used for the analysis.
        resize (float): The ratio by which the interface is to be resized.
        hand: The current hero's hand for analysis.
        house: The current house card(s) for analysis.
        ranges (list): A list of opponent ranges for analysis.

    Notes:
        This class initializes and manages various tabs within the notebook for different analysis tasks.
    """
    def __init__(self, manager, resize, *args, **kwargs):
        # Initialize the notebook with given width and height
        super().__init__(width=int(manager.width * 0.85), height=int(manager.height * 0.9), padding=manager.small_pad,
                         *args, **kwargs)
        self.manager = manager
        self.manager.notebook = self
        self.deck = Deck()
        self.resize = resize
        self.hand = None
        self.house = None
        self.ranges = []

        # Create various tabs within the notebook
        self.welcome_tab = WelcomeTab(master=self, manager=self.manager)
        self.overview_tab = OverviewTab(master=self, manager=self.manager)
        self.add_hand_tab = AddHeroHandTab(manager=self.manager, master=self)
        self.update_house_tab = UpdateHouseTab(manager=self.manager, master=self)
        self.range_selection_tab = RangeSelectionTab(master=self, manager=self.manager)
        self.ranges_tab = RangesTab(master=self, manager=self.manager)
        self.shove_calculator_tab = ShoveCalculatorTab(master=self, manager=self.manager)
        self.bet_for_value_tab = BetForValueTab(master=self, manager=self.manager)

        # Add tabs to the notebook
        self.add(self.welcome_tab, text='Welcome  ', sticky='nsew')
        self.add(self.add_hand_tab, text='My Hand  ', sticky='nsew')
        self.add(self.range_selection_tab, text='New Villain', sticky='nsew')
        self.add(self.update_house_tab, text='House  ', sticky='nsew')
        self.add(self.overview_tab, text='Overview  ', sticky='nsew')
        self.add(self.bet_for_value_tab, text='Bet Helper')
        self.add(self.shove_calculator_tab, text='Bet EV  ', sticky='nsew')
        self.add(self.ranges_tab, text='Villains  ', sticky='nsew')

        self.bind("<<NotebookTabChanged>>", self.tab_change)

    def tab_change(self, event):
        """
        Handle tab change event when the user switches between different analysis tabs.

        This method is called when the user selects a different tab within the application's notebook interface.
        It updates the game data based on the selected house cards and hero's hand, refreshes the content of
        the selected tab, manages calculations, and handles resets as needed.

        Args:
            event (Event): The tab change event triggered when a new tab is selected.

        Notes:
            - The method collects selected house cards from the 'update_house_tab'.
            - It updates the game data with the collected house cards and the selected hero's hand.
            - The method refreshes the content of the selected tab, ensuring up-to-date information.
            - If equity calculations are not in progress, related tabs are reset and background calculation is
            restarted.
            - It stops tab-specific calculations and refreshes the entire application manager.
        """
        # Create an empty list to store house cards
        house = []

        # Collect selected cards from the update_house_tab
        for button in self.update_house_tab.displayed_cards:
            if button.card:
                house.append(button.card)

        # Update the game data with the collected house cards
        self.manager.game_data['house'] = house

        # Check if the hero's hand cards are selected
        if self.add_hand_tab.first_card.card and self.add_hand_tab.second_card.card:
            # Create a Hand object with the selected cards
            self.manager.game_data['hand'] = Hand(self.add_hand_tab.first_card.card, self.add_hand_tab.second_card.card)
        else:
            # If no cards are selected, set the hero's hand to None
            self.manager.game_data['hand'] = None

        # Get the currently selected tab
        tab = event.widget.select()

        # Refresh the content of the selected tab
        for pane in self.manager.tabs:
            if tab == str(self.manager.tabs[pane]):
                self.manager.tabs[pane].refresh()

        # If equity calculations are not in progress, reset related tabs and restart background calculation
        if not self.manager.calculating['equity']:
            self.bet_for_value_tab.reset()
            self.shove_calculator_tab.reset()
            self.overview_tab.calculate()

        # Stop tab specific calculations
        self.manager.calculating['value'] = False
        self.manager.calculating['shove'] = False
        self.manager.refresh()


class Interface(tk.Tk):
    """
    Main application window for Hold 'Em Helper.

    This class represents the main application window for the Hold 'Em Helper tool. It provides a graphical user
    interface for analyzing and calculating poker hands, ranges, and related statistics.

    Attributes:
        manager (Manager): An instance of the Manager class that manages the application's state and data.
        resize_ratio (float): A scaling ratio for resizing elements based on screen dimensions.

    Methods:
        reset(): Reset the application's state and user interface.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(background='black')
        self.title("Hold 'Em Helper")

        # Get screen dimensions for resizing
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.resize_ratio = min(screen_height / 768, screen_width / 1366)

        # Initialize the application manager
        self.manager = Manager(self.resize_ratio)

        # Create a summary sidebar
        self.summary = SummarySidebar(master=self, manager=self.manager)
        self.manager.summary = self.summary

        # Place the summary sidebar
        self.summary.grid(column=1, row=0, padx=5, pady=0)

        # Create the analysis notebook
        self.analysis = Analysis(self.manager, resize=self.resize_ratio, master=self)
        self.analysis.grid(column=0, row=0, rowspan=2, sticky='nsew')

        # Create a reset button
        self.reset_button = ttk.Button(text='Reset', command=self.reset, width=5)
        self.reset_button.grid(column=0, row=0, sticky='nw', padx=self.manager.small_pad, pady=self.manager.small_pad)

        # Refresh the manager to initialize the application
        self.manager.refresh()

    def reset(self):
        """
        Reset the application's state and user interface.

        This method stops ongoing calculations, destroys existing analysis and summary widgets, and recreates the
        application's manager, analysis notebook, and summary sidebar. It is used to reset the application to its
        initial state, allowing users to start a new poker analysis session.

        Note:
            The reset process may take some time due to widget destruction and recreation. Users should wait for the
            process to complete before continuing to use the application.

        """
        # Stop ongoing calculations
        self.manager.stop_calculating()

        # Destroy the existing analysis and summary widgets
        self.after(1000, self.analysis.destroy())
        self.summary.destroy()
        self.reset_button.destroy()

        # Create a new manager with recalculated resize ratio
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.resize_ratio = min(screen_height / 768, screen_width / 1366)
        self.manager = Manager(self.resize_ratio)

        # Recreate the analysis notebook and summary sidebar
        self.analysis = Analysis(self.manager, resize=self.resize_ratio, master=self)
        self.analysis.grid(column=0, row=0, sticky='nsew', rowspan=2)

        self.summary = SummarySidebar(master=self, manager=self.manager)
        self.summary.grid(column=1, row=0, padx=5, pady=0)

        self.reset_button = ttk.Button(text='Reset', command=self.reset, width=5)
        self.reset_button.grid(column=0, row=0, sticky='nw', padx=self.manager.small_pad, pady=self.manager.small_pad)

        # Update the manager's summary reference
        self.manager.summary = self.summary
