'''INPUTS'''

DATASET = 'LiverKlopp.csv'

FORMATION = ""

CLUB = []
NUM_CLUB = []  # Total players from i^th list >= NUM_CLUB[i]

MAX_NUM_CLUB = 0  # Same Club Count: Max X
MIN_NUM_CLUB = 0  # Same Club Count: Min X
NUM_UNIQUE_CLUB = []  # Clubs: Max / Min / Exactly X

# LEAGUE = [["Premier League", "LaLiga Santander"]]
LEAGUE = []
NUM_LEAGUE = []  # Total players from i^th list >= NUM_LEAGUE[i]

MAX_NUM_LEAGUE = 0  # Same League Count: Max X
MIN_NUM_LEAGUE = 0  # Same League Count: Min X
NUM_UNIQUE_LEAGUE = []  # Leagues: Max / Min / Exactly X

COUNTRY = []
NUM_COUNTRY = []  # Total players from i^th list >= NUM_COUNTRY[i]

MAX_NUM_COUNTRY = 0  # Same Nation Count: Max X
MIN_NUM_COUNTRY = 0  # Same Nation Count: Min X
NUM_UNIQUE_COUNTRY = []  # Nations: Max / Min / Exactly X

RARITY_1 = [['Gold', 'TOTW']]
NUM_RARITY_1 = [1]  # This is for cases like "Gold IF: Min X (0/X)"

RARITY_2 = []
NUM_RARITY_2 = []  # Total players from i^th Rarity >= NUM_RARITY_2[i]

MIN_RATING = 0
MAX_RATING = 0
SQUAD_RATING = 0  # Squad Rating: Min XX

MIN_OVERALL = []
NUM_MIN_OVERALL = []  # Minimum OVR of XX : Min X

CHEMISTRY = 0
# Squad Total Chemistry Points: Min X
# If there is no constraint on total chemistry, then set this to 0.

CHEM_PER_PLAYER = 0  # Chemistry Points Per Player: Min X

'''INPUTS'''

NUM_PLAYERS = 11

FIX_PLAYERS = 0  # FIX_PLAYERS = 1 => players will be picked based on the formation and 0 otherwise.

# Set only one of the below to True and the other to False. Both can't be False.
USE_PREFERRED_POSITION = False
USE_ALTERNATE_POSITIONS = True

# Set only one of the below to True and the others to False if duplicates are to be prioritized.
USE_ALL_DUPLICATES = True
USE_AT_LEAST_HALF_DUPLICATES = False
USE_AT_LEAST_ONE_DUPLICATE = True

formation_dict = {
    "3-4-1-2": ["GK", "CB", "CB", "CB", "LM", "CM", "CM", "RM", "CAM", "ST", "ST"],
    "3-4-2-1": ["GK", "CB", "CB", "CB", "LM", "CM", "CM", "RM", "CF", "ST", "CF"],
    "3-1-4-2": ["GK", "CB", "CB", "CB", "LM", "CM", "CDM", "CM", "RM", "ST", "ST"],
    # "3-4-3": ["GK", "CB", "CB", "CB", "LM", "CM", "CM", "RM", "CAM", "ST", "ST"],
    "3-5-2": ["GK", "CB", "CB", "CB", "CDM", "CDM", "LM", "CAM", "RM", "ST", "ST"],
    "3-4-3": ["GK", "CB", "CB", "CB", "LM", "CM", "CM", "RM", "LW", "ST", "RW"],
    "4-1-2-1-2": ["GK", "LB", "CB", "CB", "RB", "CDM", "LM", "CAM", "RM", "ST", "ST"],
    "4-1-2-1-2[2]": ["GK", "LB", "CB", "CB", "RB", "CDM", "CM", "CAM", "CM", "ST", "ST"],
    "4-1-4-1": ["GK", "LB", "CB", "CB", "RB", "CDM", "LM", "CM", "CM", "RM", "ST"],
    "4-2-1-3": ["GK", "LB", "CB", "CB", "RB", "CDM", "CDM", "CAM", "LW", "ST", "RW"],
    "4-2-3-1": ["GK", "LB", "CB", "CB", "RB", "CDM", "CDM", "CAM", "CAM", "CAM", "ST"],
    "4-2-3-1[2]": ["GK", "LB", "CB", "CB", "RB", "CDM", "CDM", "CAM", "LM", "ST", "RM"],
    "4-2-2-2": ["GK", "LB", "CB", "CB", "RB", "CDM", "CDM", "CAM", "CAM", "ST", "ST"],
    "4-2-4": ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "LW", "ST", "ST", "RW"],
    "4-3-1-2": ["GK", "CB", "CB", "LB", "RB", "CM", "CM", "CM", "CAM", "ST", "ST"],
    "4-1-3-2": ["GK", "LB", "CB", "CB", "RB", "CDM", "LM", "CM", "RM", "ST", "ST"],
    "4-3-2-1": ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "CM", "CF", "ST", "CF"],
    "4-3-3": ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "CM", "LW", "ST", "RW"],
    "4-3-3[2]": ["GK", "LB", "CB", "CB", "RB", "CM", "CDM", "CM", "LW", "ST", "RW"],
    "4-3-3[3]": ["GK", "LB", "CB", "CB", "RB", "CDM", "CDM", "CM", "LW", "ST", "RW"],
    "4-3-3[4]": ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "CAM", "LW", "ST", "RW"],
    "4-3-3[5]": ["GK", "LB", "CB", "CB", "RB", "CDM", "CM", "CM", "LW", "CF", "RW"],
    "4-4-1-1": ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "LM", "CF", "RM", "ST"],
    "4-4-1-1[2]": ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "LM", "CAM", "RM", "ST"],
    "4-4-2": ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "CM", "RM", "ST", "ST"],
    "4-4-2[2]": ["GK", "LB", "CB", "CB", "RB", "LM", "CDM", "CDM", "RM", "ST", "ST"],
    "4-5-1": ["GK", "CB", "CB", "LB", "RB", "CM", "LM", "CAM", "CAM", "RM", "ST"],
    "4-5-1[2]": ["GK", "CB", "CB", "LB", "RB", "CM", "LM", "CM", "CM", "RM", "ST"],
    "5-2-1-2": ["GK", "LWB", "CB", "CB", "CB", "RWB", "CM", "CM", "CAM", "ST", "ST"],
    "5-2-2-1": ["GK", "LWB", "CB", "CB", "CB", "RWB", "CM", "CM", "LW", "ST", "RW"],
    "5-3-2": ["GK", "LWB", "CB", "CB", "CB", "RWB", "CM", "CDM", "CM", "ST", "ST"],
    "5-4-1": ["GK", "LWB", "CB", "CB", "CB", "RWB", "CM", "CM", "LM", "RM", "ST"]
}

FUTBIN_POSITIONS_DICT = {
    "4-5-1": ["ST", "LM", "CAM", "CM", "CAM", "RM", "LB", "CB", "CB", "RB", "GK"],
    "4-1-4-1": ["ST", "LM", "CM", "CM", "RM", "CDM", "LB", "CB", "CB", "RB", "GK"],
    "4-3-2-1": ["CF", "ST", "CF", "CM", "CM", "CM", "LB", "CB", "CB", "RB", "GK"],
    "4-3-3": ["LW", "ST", "RW", "CM", "CM", "CM", "LB", "CB", "CB", "RB", "GK"],
    "4-4-2": ["ST", "ST", "LM", "CM", "CM", "RM", "LB", "CB", "CB", "RB", "GK"],
    "4-4-2[2]": ["ST", "ST", "CDM", "CDM", "LM", "RM", "LB", "CB", "CB", "RB", "GK"],
    "4-2-2-2": ["ST", "ST",  "CAM", "CAM", "CDM", "CDM", "LB", "CB", "CB", "RB", "GK"],
    "4-4-1-1": ["ST", "CF", "LM", "CM", "CM", "RM", "LB", "CB", "CB", "RB", "GK"],
    "4-3-3[4]": ["LW", "ST", "RW", "CM", "CAM", "CM", "LB", "CB", "CB", "RB", "GK"],
    "4-3-3[3]": ["LW", "ST", "RW", "CDM", "CAM", "CDM", "LB", "CB", "CB", "RB", "GK"],
    "4-3-3[2]": ["LW", "ST", "RW", "CM", "CDM", "CM", "LB", "CB", "CB", "RB", "GK"],
    "4-1-2-1-2[2]": ["ST", "CAM", "ST", "CM", "CDM", "CM", "LB", "CB", "CB", "RB", "GK"],
    "4-2-3-1": ["ST", "CAM", "CAM", "CAM", "CDM", "CDM", "LB", "CB", "CB", "RB", "GK"],
    "3-5-2": ["ST", "CAM", "ST", "LM", "CDM", "CDM", "RM", "CB", "CB", "CB", "GK"]
}

status_dict = {
    0: "UNKNOWN: The status of the model is still unknown. A search limit has been reached before any of the statuses below could be determined.",
    1: "MODEL_INVALID: The given CpModelProto didn't pass the validation step.",
    2: "FEASIBLE: A feasible solution has been found. But the search was stopped before we could prove optimality.",
    3: "INFEASIBLE: The problem has been proven infeasible.",
    4: "OPTIMAL: An optimal feasible solution has been found."
}


def calc_squad_rating(rating):
    '''https://www.reddit.com/r/EASportsFC/comments/5osq7k/new_overall_rating_figured_out'''
    rat_sum = sum(rating)
    avg_rat = rat_sum / NUM_PLAYERS
    excess = sum(max(rat - avg_rat, 0) for rat in rating)
    return round(rat_sum + excess) // NUM_PLAYERS


LOG_RUNTIME = True
