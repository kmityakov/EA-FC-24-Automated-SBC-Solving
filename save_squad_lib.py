from time import sleep

import pandas
import requests
import json
import re

import input
from unidecode import unidecode

FUTBIN_FORMATION_DICT = {
    "3-4-1-2": "3412",
    "3-4-2-1": "3421",
    "3-1-4-2": "3142",
    "3-5-2": "352",
    "3-4-3": "343",
    "4-1-2-1-2": "41212",
    "4-1-2-1-2[2]": "41212-2",
    "4-1-4-1": "4141",
    "4-2-1-3": "4213",
    "4-2-3-1": "4231",
    "4-2-3-1[2]": "4231-2",
    "4-2-2-2": "4222",
    "4-2-4": "424",
    "4-3-1-2": "4312",
    "4-1-3-2": "4132",
    "4-3-2-1": "4321",
    "4-3-3": "433",
    "4-3-3[2]": "433-2",
    "4-3-3[3]": "433-3",
    "4-3-3[4]": "433-4",
    "4-3-3[5]": "433-5",
    "4-4-1-1": "4411",
    "4-4-1-1[2]": "4411-2",
    "4-4-2": "442",
    "4-4-2[2]": "442-2",
    "4-5-1": "451",
    "4-5-1[2]": "451-2",
    "5-2-1-2": "5212",
    "5-2-2-1": "5221",
    "5-3-2": "532",
    "5-4-1": "541"
}

session = requests.Session()
headers = {
    'User-Agent': 'Futbin Android'
}
session.headers.update(headers)


def search_player_by_name(name, resource_id):
    # name = re.compile(re.escape('č'), re.IGNORECASE).sub("c", name)
    # name = re.compile(re.escape('ć'), re.IGNORECASE).sub("c", name)
    # name = re.compile(re.escape('ç'), re.IGNORECASE).sub("c", name)
    # name = re.compile(re.escape('á'), re.IGNORECASE).sub("a", name)
    # name = re.compile(re.escape('ą'), re.IGNORECASE).sub("a", name)
    # name = re.compile(re.escape('ã'), re.IGNORECASE).sub("a", name)
    # name = re.compile(re.escape('à'), re.IGNORECASE).sub("a", name)
    # name = re.compile(re.escape('ä'), re.IGNORECASE).sub("a", name)
    # name = re.compile(re.escape('í'), re.IGNORECASE).sub("i", name)
    # name = re.compile(re.escape('é'), re.IGNORECASE).sub("e", name)
    # name = re.compile(re.escape('ê'), re.IGNORECASE).sub("e", name)
    # name = re.compile(re.escape('ó'), re.IGNORECASE).sub("o", name)
    # name = re.compile(re.escape('ò'), re.IGNORECASE).sub("o", name)
    # name = re.compile(re.escape('ø'), re.IGNORECASE).sub("o", name)
    # name = re.compile(re.escape('Ö'), re.IGNORECASE).sub("o", name)
    # name = re.compile(re.escape('ú'), re.IGNORECASE).sub("u", name)
    # name = re.compile(re.escape('ü'), re.IGNORECASE).sub("u", name)
    # name = re.compile(re.escape('ñ'), re.IGNORECASE).sub("n", name)
    # name = re.compile(re.escape('ń'), re.IGNORECASE).sub("n", name)
    # name = re.compile(re.escape('ý'), re.IGNORECASE).sub("y", name)
    # name = re.compile(re.escape('ș'), re.IGNORECASE).sub("s", name)
    # name = re.compile(re.escape('š'), re.IGNORECASE).sub("s", name)
    # name = re.compile(re.escape('ż'), re.IGNORECASE).sub("z", name)
    # name = re.compile(re.escape('ş'), re.IGNORECASE).sub("s", name)

    name = unidecode(name)

    if name.find("ß") >= 0:
        name = name[:name.find("ß")]
    response = session.get("https://futbin.org/futbin/api/searchPlayersByName?playername={}".format(name))
    print(response.json())
    data_list = response.json()["data"]
    filtered_list = list(filter(lambda a: str(resource_id) == a["resource_id"], response.json()["data"]))
    if len(filtered_list) > 0:
        return filtered_list[0]["ID"]
    elif len(data_list) > 0:
        return data_list[0]["ID"]
    else:
        return "0"


def create_squad_body(formation, positions, squad_body_data):
    print(positions)
    result = {
        "Formation": formation,
        "TotalChemistry": 0
    }
    for index, position in enumerate(positions):
        player_at_position = [player for player in squad_body_data if position == player[1] and player[2]]
        player_without_position = [player for player in squad_body_data if not player[2]]

        if player_at_position:
            player_to_add = player_at_position[0]
        elif player_without_position:
            player_to_add = player_without_position[0]
        else:
            player_to_add = squad_body_data[0]

        result[f"cardlid{index + 1}"] = {
            "id": int(player_to_add[0]),
            "cardPosition": player_to_add[1],
            "csi": "BAS",
            "unt": "0",
            "wl": "0",
            "chemistry": 0
        }
        squad_body_data.remove(player_to_add)

    return result


def create_squad_in_futbin(body, formation):
    payload = {'squadData': json.dumps(body),
               'rating': '83',
               'chemistry': '0',
               'formation': formation
               }
    # req = requests.Request('POST',"https://www.futbin.com/24/saveSquad", data=payload)
    # prepared = req.prepare()
    # print("Headers")
    # print(prepared.headers)
    # print("Body")
    # print(prepared.body)
    response = session.post("https://www.futbin.com/24/saveSquad", data=payload)
    print(response.status_code)
    print(response.json())
    print("https://www.futbin.com/24/squad/{}".format(response.json()["squad_id"]))

def save_squad(players, dont_send_request=False):
    print(players)
    squad_body_data = []
    # player_ids = ['761', '909', '1945', '19085', '2568', '1298', '14189', '15710', '4038', '16047', '3581']
    print("FORMATION = ", input.FORMATION)
    print("formation = ", FUTBIN_FORMATION_DICT[input.FORMATION])
    for i in players.index:
        resource_id = players['DefinitionId'][i]
        name = players['Name'][i]
        print(f"player {name} {resource_id}")
        sleep(0.2)
        name_parts = name.split()
        for part in reversed(name_parts):
            futbin_id = search_player_by_name(part, resource_id)
            if futbin_id != "0":
                break
        squad_body_data.append((futbin_id, players['Position'][i], players['Is_Pos'][i]))
        print(f"player https://www.futbin.com/24/player/{futbin_id}")

    body = create_squad_body(FUTBIN_FORMATION_DICT[input.FORMATION], input.FUTBIN_POSITIONS_DICT[input.FORMATION], squad_body_data)
    if dont_send_request:
        print(body)
        return
    create_squad_in_futbin(body, FUTBIN_FORMATION_DICT[input.FORMATION])


def remove_output_from_squad():
    df = pandas.read_csv("output.csv", index_col=False)
    squad = pandas.read_csv(input.DATASET, index_col=False)
    output_ids = df['DefinitionId'].tolist()
    # print('squad.shape[0] = ', squad.shape[0])
    # print(squad[squad['IsDuplicate'] == True].shape[0])
    for id in output_ids:
        # 'IsDuplicate'
        row = squad.loc[squad["DefinitionId"] == id]
        if row.empty:
            continue
        if row.at[row.index[0], 'IsDuplicate']:
            squad.at[row.index[0], 'IsDuplicate'] = False
        else:
            squad = squad.drop(index=row.index)
        # if row['IsDuplicate'] == True:
        #     row['IsDuplicate'] = False
        # print(row['IsDuplicate'])

        # print(row.index[0])
        # print(row.at[row.index[0], 'IsDuplicate'])

        # squad = squad[squad["DefinitionId"].isin(output_ids) == True]
    # print('squad.shape[0] = ', squad.shape[0])
    # print(squad[squad['IsDuplicate'] == True].shape[0])
    # print(output_ids)
    # print(squad.shape[0])
    # print(squad)
    squad.to_csv(input.DATASET, index=False)
    # save_squad(df)


def save_squad_test(formation):
    input.FORMATION = formation
    df = pandas.read_csv("output.csv", index_col=False)
    save_squad(df)
    # squad_body_data = [('507', 'GK', 0), ('267', 'GK', 1), ('263', 'RM', 1), ('768', 'RB', 1), ('1407', 'LB', 1), ('1562', 'CB', 1), ('1524', 'LM', 1), ('20370', 'CB', 1), ('4743', 'ST', 1), ('20869', 'CM', 1), ('16177', 'CAM', 1)]
    # body = create_squad_body(FUTBIN_FORMATION_DICT[input.FORMATION], input.formation_dict[input.FORMATION], squad_body_data)
    # print(body)

# save_squad_test()