#!/usr/bin/env python3

import time
from flask import Flask, request
from pprint import pprint
from db import db
from players_database import Player
import players_database
from sleeper_api import (get_user_leagues, get_user, get_player_data,
                         get_roster_ids, get_matchups, get_roster_by_id)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Players.sqlite3'

db.init_app(app)

@app.route("/")
def main():
    return '''
    Echo User Input:
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     Enter Sleeper Username to get Roster IDs:
     <form action="/get_roster" method="POST">
         <input name="sleeper_username" value="slugaroo">
         <input type="submit" value="Get Roster IDs">
     </form>
     Enter Sleeper Username to analyze Points For vs Points Against:
     <form action="/analyze_points_for_vs_against" method="POST">
         <input name="sleeper_username_vs" value="slugaroo">
         <input type="submit" value="Analyze Points">
     </form>
     Lookup player data by ID:
     <form action="/get_player_data" method="POST">
         <input name="player_id">
         <input type="submit" value="Get Player Data">
     </form>
     <button onclick="location.href='/refresh_player_db'" type="button">
         Refresh Player Database (may take a while)
     </button>
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
    league = get_user_leagues(user_id['user_id'], season="2023")
    rosters = get_roster_ids(league[0]['league_id'])
    user_roster = get_roster_by_id(rosters, user_id['user_id'])
    return "Player IDs: " + user_roster['players'].__str__()

@app.route("/get_player_data", methods=["POST"])
def get_players():
    input_text = request.form.get("player_id", "")
    player = Player.query.filter_by(player_id=input_text).first()
    if player is None:
        return "Player not found in database. Try refreshing the database."
    return f"Player {player.name}, Position: {player.position}, Team: {player.team}"

@app.route("/analyze_points_for_vs_against", methods=["POST"])
def analyze_points():
    input_text = request.form.get("sleeper_username_vs", "")
    user_id = get_user(input_text)
    if user_id is None:
        return "User not found"
    league = get_user_leagues(user_id['user_id'], season="2023")
    rosters = get_roster_ids(league[0]['league_id'])
    user_roster = get_roster_by_id(rosters, user_id['user_id'])
    if user_roster is None:
        return "User roster not found in league."
    points_for = user_roster.get('settings').get('fpts', 0)
    points_against = user_roster.get('settings').get('fpts_against', 0)
    if points_for > points_against:
        result = f"Your team did well! Points For: {points_for}, Points Against: {points_against}"
    elif points_for < points_against:
        result = f"Your team didnt do well. Points For: {points_for}, Points Against: {points_against}"
    else:
        result = f"Your team perfectly tied. Points For: {points_for}, Points Against: {points_against}"
    return result

@app.route("/refresh_player_db")
def refresh_player_db():
    players_database.update_player_database()
    return "Player database refreshed!"
