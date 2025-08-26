#!/usr/bin/env python3

import time
from flask import Flask, request
from pprint import pprint
from sleeper_api import (get_user_leagues, get_user, get_player_data,
                         get_roster_ids, get_matchups, get_roster_by_id)

app = Flask(__name__)

@app.route("/")
def main():
    return '''
    Echo User Input:
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     Enter Sleeper Username:
     <form action="/get_roster" method="POST">
         <input name="sleeper_username">
         <input type="submit" value="Get Roster">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

@app.route("/get_roster", methods=["POST"])
def get_roster():
    input_text = request.form.get("sleeper_username", "")
    user_id = get_user(input_text)
    if user_id is None:
        return "User not found"
    print(f"UserID: {user_id['user_id']}")
    league = get_user_leagues(user_id['user_id'], season="2023")
    rosters = get_roster_ids(league[0]['league_id'])
    user_roster = get_roster_by_id(rosters, user_id['user_id'])
    return "roster IDs: " + user_roster['players'].__str__()