import requests

BASE_URL = "https://api.sleeper.app/v1"

def get_user(username):
    res = requests.get(f"{BASE_URL}/user/{username}")
    return res.json() if res.status_code == 200 else None

def get_user_leagues(user_id, season="2023"):
    res = requests.get(f"{BASE_URL}/user/{user_id}/leagues/nfl/{season}")
    return res.json() if res.status_code == 200 else []

def get_player_data():
    res = requests.get(f"{BASE_URL}/players/nfl")
    return res.json() if res.status_code == 200 else {}

def get_roster_ids(league_id):
    res = requests.get(f"{BASE_URL}/league/{league_id}/rosters")
    return res.json() if res.status_code == 200 else []

def get_matchups(league_id, week):
    res = requests.get(f"{BASE_URL}/league/{league_id}/matchups/{week}")
    return res.json() if res.status_code == 200 else []

def get_user_roster_id(rosters, user_id):
    for r in rosters:
        if r.get("owner_id") == user_id:
            return r.get("roster_id")
    return None