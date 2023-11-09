import tkinter.ttk as ttk
from functions import *


class CardButton(ttk.Button):
    """
    Button widget representing a playing card.

    Args:
        card (Card): The playing card associated with this button.
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the ttk.Button constructor.
    """
    def __init__(self, card, manager, tab, *args, **kwargs):
        super().__init__(command=self.pressed, *args, **kwargs)
        self.manager = manager
        self.tab = tab
        self.card = card
        self.image = ImageTk.PhotoImage(rescale(self.card.raw_image, self.manager.small_card))
        self.blank = get_blank_card(self.manager.small_card)
        self.refresh()

    def refresh(self):
        """
        Refresh the card button's image to represent the current state of the associated playing card in the deck.
        """
        if self.manager.game_data['deck'].cards[self.card]:
            self.configure(image=self.image)
        else:
            self.configure(image=self.blank)

    def pressed(self):
        """
        Handle the button press event for the card button.

        If the associated playing card is available in the deck, this method handles the following steps:
        1. Stop any ongoing calculations in the manager.
        2. Find the first available card display slot.
        3. Deal the associated playing card to that slot.
        4. Refresh the 'Add Hero Hand' and 'Update House' tabs in the manager.

        Note that this method is typically invoked when the user clicks the card button.
        """
        if self.manager.game_data['deck'].cards[self.card]:
            for calculation in self.manager.calculating:
                self.manager.calculating[calculation] = False
            for display in self.tab.displayed_cards:
                if not display.card:
                    self.manager.game_data['deck'].deal_card(self.card)
                    display.card = self.card
                    self.manager.tabs['add_hero_hand'].refresh()
                    self.manager.tabs['update_house'].refresh()
                    break


class DisplayCardButton(ttk.Button):
    """
    Button widget representing a displayed playing card.

    Args:
        manager (Manager): The parent GUI manager.
        *args, **kwargs: Additional arguments for the ttk.Button constructor.
    """
    def __init__(self, manager, *args, **kwargs):
        super().__init__(command=self.pressed, *args, **kwargs)
        self.card = None
        self.manager = manager
        self.image = get_blank_card(self.manager.large_card)
        self.card_image = None
        self.configure(image=self.image)

    def pressed(self):
        """
        Handle the button press event.

        If there is a displayed card, this method is called when the button is pressed.
        It resets ongoing calculations, adds the displayed card back to the deck, clears
        the displayed card, and triggers a refresh of relevant tabs in the GUI.

        This method effectively removes the displayed card when the button is pressed.

        """
        if self.card:
            # Reset ongoing calculations
            for calculation in self.manager.calculating:
                self.manager.calculating[calculation] = False

            # Add the displayed card back to the deck
            self.manager.game_data['deck'].add_cards(self.card)

            # Clear the displayed card
            self.card = None

            # Refresh relevant tabs in the GUI
            self.manager.tabs['add_hero_hand'].refresh()
            self.manager.tabs['update_house'].refresh()


class HandButton(ttk.Button):
    """
    Button widget representing a group of hands with the same name.

    Args:
        manager (Manager): The parent GUI manager.
        hand_name (str): The name of the group of hands.
        villain_range (VillainRange): The opponent's hand range.
        *args, **kwargs: Additional arguments for the ttk.Button constructor.
    """
    def __init__(self, manager, hand_name, villain_range, *args, **kwargs):
        super().__init__(text=hand_name, width=0, style='Hand.TButton', *args, **kwargs)
        self.villain_range = villain_range
        self.manager = manager
        self.hand_name = hand_name
        self.hands = [hand for hand in self.villain_range.hands
                      if self.villain_range.hands[hand] and hand.name == self.hand_name]
        self.selected = False
        self.default_style = 'Hand.TButton'

    def highlight(self, widget):
        """
        Toggle the highlight style of the button and update the selected hands.

        Args:
            widget: The parent widget (either RangeFilter or RangeDisplay).
        """
        already_clicked = False
        for hand in self.hands:
            if hand in widget.clicked_hands or hand in widget.selected_hands:
                already_clicked = True

        if already_clicked:
            # If the hands are already clicked, un-highlight them and remove them from the selected hands.
            self.configure(style=self.default_style)
            for hand in self.hands:
                widget.clicked_hands.discard(hand)
                widget.selected_hands.discard(hand)
        else:
            # If the hands are not clicked, highlight them and add them to the selected hands.
            self.configure(style='Highlighted.Hand.TButton')
            for hand in self.hands:
                widget.clicked_hands.add(hand)
                widget.selected_hands.add(hand)
        widget.selected_hands_count.set(f'{len(widget.selected_hands)} selected')


class SuitedHandButton(ttk.Button):
    """
    Button widget representing a suited hand.

    Args:
        manager (Manager): The parent GUI manager.
        hand (Hand): The suited hand associated with this button.
        style (str): The style to apply to the button.
        villain_range (VillainRange): The villain's hand range.
        *args, **kwargs: Additional arguments for the ttk.Button constructor.
    """
    def __init__(self, manager, hand, style, villain_range, *args, **kwargs):
        super().__init__(text=hand.name[:2], style=style, width=0, *args, **kwargs)
        self.manager = manager
        self.villain_range = villain_range
        self.hands = [hand]
        self.selected = False
        self.default_style = style

    def highlight(self, widget):
        """
        Toggle the highlight state of the button and update the selected hands in the widget.

        Args:
            widget: The widget (e.g., RangeFilter or RangeDisplay) where the selection is managed.
        """
        already_clicked = False
        for hand in self.hands:
            if hand in widget.selected_hands:
                already_clicked = True

        if already_clicked:
            # Unselect the hand
            self.configure(style=self.default_style)
            for hand in self.hands:
                widget.clicked_hands.discard(hand)
                widget.selected_hands.discard(hand)
        else:
            # Select the hand
            self.configure(style='Highlighted.Hand.TButton')
            for hand in self.hands:
                widget.clicked_hands.add(hand)
                widget.selected_hands.add(hand)

        # Update the count of selected hands in the widget
        widget.selected_hands_count.set(f'{len(widget.selected_hands)} selected')
