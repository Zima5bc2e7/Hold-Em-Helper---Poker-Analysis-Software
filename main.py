from tabs import *


root = Interface()
root.state('zoomed')

# Use received window size to set font sizes
TAB_FONT = 'Times', int(8 * root.resize_ratio)
LABEL_FONT = 'Calibri', int(12 * root.resize_ratio)
BUTTON_FONT = 'Times', int(8 * root.resize_ratio)
HAND_BUTTON_FONT = 'Times', int(6 * root.resize_ratio)
BOLD_HAND_BUTTON_FONT = 'Times', int(6 * root.resize_ratio), 'bold'
TITLE_FONT = 'Times', int(20 * root.resize_ratio), 'bold'

# Style
style = ttk.Style()

# Set the overall theme to 'clam'
style.theme_use('clam')

# Button styles
style.configure('TButton', relief=tk.RAISED, background='deeppink', foreground='#FFEAEA', font=BUTTON_FONT)
style.configure('Hand.TButton', background='gray', foreground='#FFEAEA', font=HAND_BUTTON_FONT)

# Button style mapping
style.map('TButton', foreground=[('pressed', 'deeppink')], background=[('pressed', 'black'), ('active', 'green')])
style.map('Hand.TButton', background=[('active', 'darkgoldenrod'), ('pressed', 'deeppink')])

# Highlighted button style
style.configure('Highlighted.Hand.TButton', background='yellow', foreground='blue', font=BOLD_HAND_BUTTON_FONT)

# Configure button styles for suits
for suit in suits:
    style_name = f'{suit}.Hand.TButton'
    style.configure(style_name, background=suit_colours[suit], foreground='#FFEAEA')

# Label styles
style.configure('TLabel', background='deeppink', font=LABEL_FONT, foreground='#FFEAEA')
style.configure('Title.TLabel', font=TITLE_FONT)
style.configure('Guide.TLabel', background='black')

# Configure label styles for suits
for suit in suits:
    style.configure(f'{suit}.TLabel', background='pink1', foreground=suit_colours[suit], font=LABEL_FONT)

# Frame styles
style.configure('TFrame', background='black', bordercolor='deeppink')
style.configure('Range.TFrame', background='pink1')

# Notebook styles
style.configure('TNotebook', tabposition='w', background='black', darkcolor='deeppink', foreground='deeppink',
                lightcolor='#BC767C', bordercolor='deeppink', sticky='nsew')
style.configure('Ranges.TNotebook', tabposition='n', sticky='nsew')
style.configure('TNotebook.Tab', background='deeppink', expand=(0, 0, 0, 0), foreground='black',
                bordercolor='deeppink', font=TAB_FONT, padding=(0, 0, 0, 0), focuscolor='green')

# Checkbutton styles
style.configure('TCheckbutton', background='black', foreground='white', width=25)

# Checkbutton style mapping
style.map('TCheckbutton', background=[('active', 'green'), ('selected', 'yellow')], foreground=[('selected', 'blue')],
          font=[('selected', BOLD_HAND_BUTTON_FONT)])

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
