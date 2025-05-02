#!/usr/bin/env python3

import time
from flask import Flask, request
from pprint import pprint
from sleeper_api import (get_user_leagues, get_user, get_player_data,
                         get_roster_ids, get_matchups, get_user_roster_id)

app = Flask(__name__)

@app.route("/")
def main():
    return '''
    Enter Username:
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    user_id = get_user(input_text)
    if user_id is None:
        print( "User not found")
    print (f'UserID: {user_id['user_id']}')
    league = get_user_leagues(user_id['user_id'], season="2023")
    pprint(league[0])
    rosters = get_roster_ids(league[0]['league_id'])
    pprint(rosters)
    user_roster_id = get_user_roster_id(rosters, user_id['user_id'])
    pprint(user_roster_id)
    # player_data = get_player_data()
    # time.sleep(5)
    # pprint(player_data)
    return "username Roster id: " + str(user_roster_id)
