welcome_message = ("Welcome to Texas Hold 'Em Helper! This tool is your key to mastering the blend of skill "
                   "and luck in poker. \nWe'll help you make the right calls, bets, and shoves. "
                   "Here's how to get started:\n\n"
                   "Step 1: Choose Your Hand\n"
                   "Select a hand you're unsure about. We'll analyze the actions of your opponents.\n \n"
                   "Step 2: Card Selection\n"
                   "Select the cards you were dealt in the Card Selection tab.\n\n"
                   "Step 3: Evaluate Ranges\n"
                   "Judge your opponents' possible hands. Do they play tight or loose? "
                   "Exclude weak and strong hands using our sliders and hand selection options.\n\n"
                   "Step 4: House Selection\n"
                   "Choose the house cards dealt in the House Selection tab.\n\n"
                   "Step 5: Analyze Equity\n"
                   "In the Overview tab, you can see your equity against the selected ranges, "
                   "your chances of making a strong hand, and your win rate.\n\n"
                   "Step 6: Bet Wisely\n"
                   "Use the Bet Helper to select hands your opponents might call with. "
                   "Calculate how much you can profitably bet.\n\n"
                   "Step 7: Expected Value Calculation\n"
                   "In the EV Calculator tab, choose calling hands, enter pot and bet size. "
                   "Calculate the EV of your move.\n\n"
                   "Step 8: Track Villains\n"
                   "After a round of betting, deduce which hands have been folded by your opponents in the "
                   "Villains tab and return to stage 4.\n\n"
                   "Get ready to enhance your poker skills and make winning decisions. Let's dive in!")

selector_text = "Judge Your Opponents' Range.\nExclude/Include Hands.\nCommit to Play."

overview_text = "Check Your Equity.\nAssess Hand Strength."

bet_helper_text = "Maximize Your Bets.\nChoose Opponent Calls.\nSee What's Possible."

shove_calc_text = "Set Your Bet.\nCalculate Expected Value.\nTake Control of the Game."

villains_text = "Gather Info.\nFilter Folded Hands.\nMove On to the Next Round."

card_selection_text = "Pick Your Hole Cards.\nLet's Play!"

house_selection_text = "Choose House Cards.\nBuild Your Hand."

values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

short_suits = {"C": "Clubs",
               "D": "Diamonds",
               "H": "Hearts",
               "S": "Spades"
               }

suits_alpha = {"Clubs": 1,
               "Diamonds": 2,
               "Hearts": 3,
               "Spades": 4,
               }

suit_colours = {"Clubs": "green",
                "Diamonds": "blue",
                "Hearts": "red",
                "Spades": "black",
                }


suit_symbols = {"Clubs": "♣",
                "Diamonds": "♦",
                "Hearts": "♥",
                "Spades": "♠",
                }

made_hands = {2: 'High Card',
              3: 'Pair',
              4: 'Two Pair',
              5: 'Three of a Kind',
              6: 'Straight',
              7: 'Flush',
              8: 'Full House',
              9: 'Quads',
              10: 'Straight Flush'}

starting_hand_ranks = {"AA": 0.004524886877828055,
                       "KK": 0.00904977375565611,
                       "QQ": 0.013574660633484163,
                       "AKs": 0.016591251885369532,
                       "JJ": 0.021116138763197588,
                       "AQs": 0.024132730015082957,
                       "KQs": 0.027149321266968326,
                       "AJs": 0.030165912518853696,
                       "KJs": 0.033182503770739065,
                       "TT": 0.03770739064856712,
                       "AK": 0.04675716440422323,
                       "ATs": 0.0497737556561086,
                       "QJs": 0.052790346907993974,
                       "KTs": 0.055806938159879346,
                       "QTs": 0.05882352941176472,
                       "JTs": 0.06184012066365009,
                       "99": 0.06636500754147814,
                       "AQ": 0.07541478129713425,
                       "A9s": 0.07843137254901962,
                       "KQ": 0.08748114630467572,
                       "88": 0.09200603318250378,
                       "K9s": 0.09502262443438915,
                       "T9s": 0.09803921568627452,
                       "A8s": 0.1010558069381599,
                       "Q9s": 0.10407239819004527,
                       "J9s": 0.10708898944193064,
                       "AJ": 0.11613876319758674,
                       "A5s": 0.11915535444947212,
                       "77": 0.12368024132730017,
                       "A7s": 0.12669683257918554,
                       "KJ": 0.13574660633484165,
                       "A4s": 0.138763197586727,
                       "A3s": 0.14177978883861236,
                       "A6s": 0.14479638009049772,
                       "QJ": 0.15384615384615383,
                       "66": 0.1583710407239819,
                       "K8s": 0.16138763197586725,
                       "T8s": 0.1644042232277526,
                       "A2s": 0.16742081447963797,
                       "98s": 0.17043740573152333,
                       "J8s": 0.1734539969834087,
                       "AT": 0.1825037707390648,
                       "Q8s": 0.18552036199095015,
                       "K7s": 0.1885369532428355,
                       "KT": 0.1975867269984916,
                       "55": 0.20211161387631968,
                       "JT": 0.21116138763197578,
                       "87s": 0.21417797888386114,
                       "QT": 0.22322775263951725,
                       "44": 0.2277526395173453,
                       "33": 0.23227752639517338,
                       "22": 0.23680241327300144,
                       "K6s": 0.2398190045248868,
                       "97s": 0.24283559577677216,
                       "K5s": 0.24585218702865752,
                       "76s": 0.24886877828054288,
                       "T7s": 0.25188536953242824,
                       "K4s": 0.2549019607843136,
                       "K3s": 0.25791855203619896,
                       "K2s": 0.2609351432880843,
                       "Q7s": 0.2639517345399697,
                       "86s": 0.26696832579185503,
                       "65s": 0.2699849170437404,
                       "J7s": 0.27300150829562575,
                       "54s": 0.2760180995475111,
                       "Q6s": 0.27903469079939647,
                       "75s": 0.2820512820512818,
                       "96s": 0.2850678733031672,
                       "Q5s": 0.28808446455505254,
                       "64s": 0.2911010558069379,
                       "Q4s": 0.29411764705882326,
                       "Q3s": 0.2971342383107086,
                       "T9": 0.30618401206636475,
                       "T6s": 0.3092006033182501,
                       "Q2s": 0.31221719457013547,
                       "A9": 0.3212669683257916,
                       "53s": 0.32428355957767696,
                       "85s": 0.3273001508295623,
                       "J6s": 0.3303167420814477,
                       "J9": 0.3393665158371038,
                       "K9": 0.34841628959275994,
                       "J5s": 0.3514328808446453,
                       "Q9": 0.36048265460030143,
                       "43s": 0.3634992458521868,
                       "74s": 0.36651583710407215,
                       "J4s": 0.3695324283559575,
                       "J3s": 0.37254901960784287,
                       "95s": 0.3755656108597282,
                       "J2s": 0.3785822021116136,
                       "63s": 0.38159879336349894,
                       "A8": 0.3906485671191551,
                       "52s": 0.39366515837104044,
                       "T5s": 0.3966817496229258,
                       "84s": 0.39969834087481115,
                       "T4s": 0.4027149321266965,
                       "T3s": 0.40573152337858187,
                       "42s": 0.40874811463046723,
                       "T2s": 0.4117647058823526,
                       "98": 0.4208144796380087,
                       "T8": 0.42986425339366485,
                       "A5": 0.438914027149321,
                       "A7": 0.4479638009049771,
                       "73s": 0.4509803921568625,
                       "A4": 0.4600301659125186,
                       "32s": 0.46304675716440397,
                       "94s": 0.4660633484162893,
                       "93s": 0.4690799396681747,
                       "J8": 0.4781297134238308,
                       "A3": 0.48717948717948695,
                       "62s": 0.4901960784313723,
                       "92s": 0.49321266968325767,
                       "K8": 0.5022624434389138,
                       "A6": 0.5113122171945699,
                       "87": 0.520361990950226,
                       "Q8": 0.529411764705882,
                       "83s": 0.5324283559577674,
                       "A2": 0.5414781297134235,
                       "82s": 0.5444947209653088,
                       "97": 0.5535444947209649,
                       "72s": 0.5565610859728503,
                       "76": 0.5656108597285063,
                       "K7": 0.5746606334841624,
                       "65": 0.5837104072398185,
                       "T7": 0.5927601809954746,
                       "K6": 0.6018099547511306,
                       "86": 0.6108597285067867,
                       "54": 0.6199095022624428,
                       "K5": 0.6289592760180989,
                       "J7": 0.6380090497737549,
                       "75": 0.647058823529411,
                       "Q7": 0.6561085972850671,
                       "K4": 0.6651583710407232,
                       "K3": 0.6742081447963792,
                       "K2": 0.6832579185520353,
                       "96": 0.6923076923076914,
                       "64": 0.7013574660633475,
                       "Q6": 0.7104072398190036,
                       "53": 0.7194570135746596,
                       "85": 0.7285067873303157,
                       "T6": 0.7375565610859718,
                       "Q5": 0.7466063348416279,
                       "43": 0.7556561085972839,
                       "Q4": 0.76470588235294,
                       "Q3": 0.7737556561085961,
                       "Q2": 0.7828054298642522,
                       "74": 0.7918552036199082,
                       "J6": 0.8009049773755643,
                       "63": 0.8099547511312204,
                       "J5": 0.8190045248868765,
                       "95": 0.8280542986425325,
                       "52": 0.8371040723981886,
                       "J4": 0.8461538461538447,
                       "J3": 0.8552036199095008,
                       "42": 0.8642533936651569,
                       "J2": 0.8733031674208129,
                       "84": 0.882352941176469,
                       "T5": 0.8914027149321251,
                       "T4": 0.9004524886877812,
                       "32": 0.9095022624434372,
                       "T3": 0.9185520361990933,
                       "73": 0.9276018099547494,
                       "T2": 0.9366515837104055,
                       "62": 0.9457013574660615,
                       "94": 0.9547511312217176,
                       "93": 0.9638009049773737,
                       "92": 0.9728506787330298,
                       "83": 0.9819004524886858,
                       "82": 0.9909502262443419,
                       "72": 0.999999999999998,

                       }
