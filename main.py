import requests
from urls import GET_REALM_INFO_URL, GET_MYTHIC_LEADERBOARD_URL, ACCESS_TOKEN_STRING

import json


class PlayerData:
    realm = ""
    name = ""

    def __init__(self, name, realm):
        self.name = name
        self.realm = realm.lower()


dungs = {
    "Atal'dazar": 244,
    'Freehold': 245,
    'Tol Dagor': 246,
    'The MOTHERLODE!!': 247,
    'Waycrest Manor': 248,
    "Kings' Rest": 249,
    'Temple of Sethraliss': 250,
    'The Underrot': 251,
    'Shrine of the Storm': 252,
    'Siege of Boralus': 353
}

mockdung_id = 249
mockdata = ["[20:47] Mlemmi-Draenor ", "[20:47] Tillie-Kazzak "]

players = []
for somedata in mockdata:
    # split the input into [name, realm] for each player, this is fragile for now
    player_and_realm = somedata.split("] ")[1].strip().split("-")

    # unpacks the list of 2 things -> [name, realm]
    playerdata = PlayerData(*player_and_realm)
    players.append(playerdata)

for player in players:
    response = requests.get(GET_REALM_INFO_URL.format(player.realm))
    realm_info_json = json.loads(response.text)
    # +1 moves the index in front of the slash
    connected_id_start = realm_info_json["connected_realm"]["href"].rfind(
        "/") + 1
    connected_id_end = realm_info_json["connected_realm"]["href"].rfind("?")
    connected_id = realm_info_json["connected_realm"]["href"][
        connected_id_start:connected_id_end]
    print("Connected realm id", connected_id)

    mythic_leaderboard_response = requests.get(
        GET_MYTHIC_LEADERBOARD_URL.format(connected_id))
    mythic_leaderboard_json = json.loads(mythic_leaderboard_response.text)

    for leaderboard in mythic_leaderboard_json["current_leaderboards"]:
        if leaderboard["id"] == mockdung_id:
            leaderboard_response = requests.get(leaderboard["key"]["href"] +
                                                "&" + ACCESS_TOKEN_STRING)
            leaderboard_json = json.loads(leaderboard_response.text)
            last_group = leaderboard_json["leading_groups"][-1]
            seconds = (last_group["duration"] / 1000) % 60
            minutes = (last_group["duration"] / (1000 * 60)) % 60
            print("Last group level", last_group["keystone_level"], "Duration",
                  "{0}m {1}s".format(minutes, seconds))

            break
