import re

import requests

import input
import save_squad_lib

session = requests.Session()
headers = {
    'User-Agent': 'Futbin Android'
}
session.headers.update(headers)

KNOWN_COUNTRIES = [
    'Germany',
    'Spain',
    'Portugal',
    'France'
]

KNOWN_LEAGUES = [
    'Ligue 1 Uber Eats',
    'LALIGA EA SPORTS',
    'Serie A TIM',
    "Premier League",
    'Bundesliga'
]

def get_challenges_by_set_id(set_id):
    return session.get("https://futbin.org/futbin/api/getChallengesBySetId?set_id={}".format(set_id)).json()["data"]


def get_sbc_squads_ids(challenge_id):
    sbc_squads = session.get(
        "https://futbin.org/futbin/api/getChallengeTopSquads?platform={}&chal_id={}".format('PS', challenge_id)).json()[
        "data"]
    return sbc_squads

def get_challenge_requirements(set_id, challenge_id):
    challenges = get_challenges_by_set_id(set_id)
    challenge = [x for x in challenges if x['challengeId'] == challenge_id][0]
    reqs = challenge['reqs']

    formation = get_sbc_squads_ids(challenge_id)[0]['formation']
    input.FORMATION = [key for key,value in save_squad_lib.FUTBIN_FORMATION_DICT.items() if value == formation][0]

    for req in reqs:

        if m := re.search("Team Chemistry: Min (\d+)", req):
            input.CHEMISTRY = int(m.group(1))
        elif m := re.search("Same League Count: Min (\d+)", req):
            input.MIN_NUM_LEAGUE = int(m.group(1))
        elif m := re.search("Same League Count: Max (\d+)", req):
            input.MAX_NUM_LEAGUE = int(m.group(1))
        elif m := re.search("Same Club Count: Min (\d+)", req):
            input.MIN_NUM_CLUB = int(m.group(1))
        elif m := re.search("Same Club Count: Max (\d+)", req):
            input.MAX_NUM_CLUB = int(m.group(1))
        elif m := re.search("Same Nation Count: Min (\d+)", req):
            input.MIN_NUM_COUNTRY = int(m.group(1))
        elif m := re.search("Same Nation Count: Max (\d+)", req):
            input.MAX_NUM_COUNTRY = int(m.group(1))
        elif m := re.search("Squad Rating: Min (\d+)", req):
            input.SQUAD_RATING = int(m.group(1))
        elif m := re.search("Rare: Min (\d+)", req):
            input.RARITY_2 += ["Rare"]
            input.NUM_RARITY_2 += [int(m.group(1))]
        elif m := re.search("# of players from (.+): Min (\d+)", req):
            if m.group(1) in KNOWN_LEAGUES:
                input.LEAGUE += [[m.group(1)]]
                input.NUM_LEAGUE += [int(m.group(2))]
            elif m.group(1) in KNOWN_COUNTRIES:
                input.COUNTRY += [[m.group(1)]]
                input.NUM_COUNTRY += [int(m.group(2))]
            else:
                input.CLUB += [[m.group(1)]]
                input.NUM_CLUB += [int(m.group(2))]
        elif m := re.search("Nationalities: Min (\d+)", req):
            input.NUM_UNIQUE_COUNTRY = [int(m.group(1)), "Min"]
        elif m := re.search("Nationalities: Max (\d+)", req):
            input.NUM_UNIQUE_COUNTRY = [int(m.group(1)), "Max"]
        elif m := re.search("Nationalities: Exactly (\d+)", req):
            input.NUM_UNIQUE_COUNTRY = [int(m.group(1)), "Exactly"]
        elif m := re.search("Gold Players: Min (\d+)", req):
            input.RARITY_2 += ["Gold"]
            input.NUM_RARITY_2 += [int(m.group(1))]
        elif req == 'Player Level: Min Silver':
            input.MIN_RATING = 65
        elif m := re.search("Leagues: Min (\d+)", req):
            input.NUM_UNIQUE_LEAGUE = [int(m.group(1)), "Min"]
        elif m := re.search("Leagues: Max (\d+)", req):
            input.NUM_UNIQUE_LEAGUE = [int(m.group(1)), "Max"]
        elif m := re.search("Leagues: Exactly (\d+)", req):
            input.NUM_UNIQUE_LEAGUE = [int(m.group(1)), "Exactly"]
        elif m := re.search("Clubs: Min (\d+)", req):
            input.NUM_UNIQUE_CLUB = [int(m.group(1)), "Min"]
        elif m := re.search("Clubs: Max (\d+)", req):
            input.NUM_UNIQUE_CLUB = [int(m.group(1)), "Max"]
        elif m := re.search("Clubs: Exactly (\d+)", req):
            input.NUM_UNIQUE_CLUB = [int(m.group(1)), "Exactly"]
        # elif m := re.search("IF  Players: Min (\d+)", req):
        #     input.RARITY_2 += ["Team of the Week"]
        #     input.NUM_RARITY_2 += [int(m.group(1))]
        elif m := re.search("TOTS or TOTW: Min (\d+)", req):
            input.RARITY_2 += ["Team of the Week"]
            input.NUM_RARITY_2 += [int(m.group(1))]
        elif m := re.search("Minimum OVR of (\d+) : Min (\d+)", req):
            input.MIN_OVERALL = [int(m.group(1))]
            input.NUM_MIN_OVERALL = [int(m.group(2))]

    print('input.FORMATION = ', input.FORMATION)
    print('input.CHEMISTRY = ', input.CHEMISTRY)
    print('input.SQUAD_RATING = ', input.SQUAD_RATING)
    print('input.MIN_RATING = ', input.MIN_RATING)
    print('input.MIN_NUM_LEAGUE =', input.MIN_NUM_LEAGUE)
    print('input.MAX_NUM_LEAGUE =', input.MAX_NUM_LEAGUE)
    print('input.MIN_NUM_CLUB =', input.MIN_NUM_CLUB)
    print('input.MAX_NUM_CLUB =', input.MAX_NUM_CLUB)
    print('input.MIN_NUM_COUNTRY =', input.MIN_NUM_COUNTRY)
    print('input.MAX_NUM_COUNTRY =', input.MAX_NUM_COUNTRY)
    print('input.RARITY_2 =', input.RARITY_2)
    print('input.NUM_RARITY_2 =', input.NUM_RARITY_2)
    print('input.CLUB =', input.CLUB)
    print('input.NUM_CLUB =', input.NUM_CLUB)
    print('input.LEAGUE =', input.LEAGUE)
    print('input.NUM_LEAGUE =', input.NUM_LEAGUE)
    print('input.COUNTRY =', input.COUNTRY)
    print('input.NUM_COUNTRY =', input.NUM_COUNTRY)
    print('input.NUM_UNIQUE_CLUB = ', input.NUM_UNIQUE_CLUB)
    print('input.NUM_UNIQUE_LEAGUE = ', input.NUM_UNIQUE_LEAGUE)
    print('input.NUM_UNIQUE_COUNTRY = ', input.NUM_UNIQUE_COUNTRY)
    print('input.MIN_OVERALL = ', input.MIN_OVERALL)
    print('input.NUM_MIN_OVERALL = ', input.NUM_MIN_OVERALL)