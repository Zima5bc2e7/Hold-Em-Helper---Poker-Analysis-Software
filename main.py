from tabs import *


root = Interface()
root.state('zoomed')

# Use received window size to set font sizes
TAB_FONT = 'Impact', int(10 * root.resize_ratio)
LABEL_FONT = 'Comfortaa', int(12 * root.resize_ratio)
BUTTON_FONT = 'Impact', int(12 * root.resize_ratio)
BOLD_BUTTON_FONT = 'Times', int(12 * root.resize_ratio), 'bold'
HAND_BUTTON_FONT = 'Georgia', int(9 * root.resize_ratio)
BOLD_HAND_BUTTON_FONT = 'Georgia', int(9 * root.resize_ratio), 'bold'
TITLE_FONT = 'Times', int(20 * root.resize_ratio), 'bold'
CHECKBUTTON_FONT = 'Georgia', int(9 * root.resize_ratio)
BOLD_CHECKBUTTON_FONT = 'Georgia', int(9 * root.resize_ratio), 'bold'


# Style
style = ttk.Style()

# Set the overall theme to 'clam'
style.theme_use('clam')

# Button styles
style.configure('TButton', relief=tk.RAISED, background='deeppink', foreground='#FFEAEA', font=BUTTON_FONT)
style.configure('Hand.TButton', background='gray', foreground='#FFEAEA', font=BOLD_HAND_BUTTON_FONT,
                padding=0)

# Button style mapping
style.map('TButton', foreground=[('pressed', 'deeppink')], background=[('pressed', '#333333'), ('active', 'green')])
style.map('Hand.TButton', background=[('active', 'darkgoldenrod'), ('pressed', 'deeppink')])

# Highlighted button style
style.configure('Highlighted.Hand.TButton', background='yellow', foreground='blue')

# Configure button styles for suits
for suit in suits:
    style_name = f'{suit}.Hand.TButton'
    style.configure(style_name, background=suit_colours[suit], foreground='#FFEAEA')

# Label styles
style.configure('TLabel', background='black', font=LABEL_FONT, foreground='deeppink')
style.configure('Title.TLabel', font=TITLE_FONT)
style.configure('Guide.TLabel', background='black', foreground='white')

# Configure label styles for suits
for suit in suits:
    style.configure(f'{suit}.TLabel', background='pink1', foreground=suit_colours[suit], font=TITLE_FONT)

# Frame styles
style.configure('TFrame', background='black', bordercolor='deeppink')
style.configure('Range.TFrame', background='pink1')

# Notebook styles
style.configure('TNotebook', tabposition='w', background='black', darkcolor='deeppink', foreground='deeppink',
                lightcolor='#BC767C', bordercolor='deeppink', sticky='nsew')
style.configure('Ranges.TNotebook', tabposition='n', sticky='nsew')
style.configure('TNotebook.Tab', bordercolor='deeppink', font=TAB_FONT, padding=0, focuscolor='deeppink')

# Notebook tab style mapping
style.map('TNotebook.Tab', expand=[('selected', 0), ('!selected', 0)], padding=[('selected', 0), ('!selected', 0)],
          background=[('selected', '#333333'), ('!selected', '#1a1a1a')],
          foreground=[('selected', 'deeppink'), ('!selected', '#ffffff')])

# Checkbutton styles
style.configure('TCheckbutton', background='black', foreground='white', width=20)

# Checkbutton style mapping
style.map('TCheckbutton', background=[('active', 'green'), ('selected', 'yellow')], foreground=[('selected', 'blue')],
          font=[('selected', BOLD_CHECKBUTTON_FONT), ('!selected', CHECKBUTTON_FONT)])

# Horizontal Scale styles
style.configure('Horizontal.TScale', background='deeppink', troughcolor='lavender', bordercolor='white',
                lightcolor='black', arrowsize=15, gripcount=4)

# Horizontal Scale style mapping
style.map('Horizontal.TScale', gripcount=[('pressed', 6), ('active', 5)],
          background=[('pressed', 'black'), ('active', 'green')],
          bordercolor=[('pressed', 'white'), ('active', 'white')],
          lightcolor=[('pressed', 'deeppink'), ('active', 'green')],
          troughcolor=[('pressed', 'black'), ('active', 'green')])

#


root.mainloop()
