from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, timezone

from sleeper_api import get_roster_ids, get_user, get_user_leagues, get_roster_by_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Sleeper.sqlite3'

db = SQLAlchemy(app)

'''
Define a model for the Sleeper data we want to store.
''' 
class Sleeper(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=lambda:datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=False)
    league_id = db.Column(db.Integer, nullable=False)
    players = db.Column(db.JSON, nullable=False)

'''
In main we first get the current temperature and then 
create a new object that we can add to the database. 
'''
if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Create tables
        username = "slugaroo"  # Replace with actual username input
        user_id = get_user(username)
        # print(f"UserID: {user_id['user_id']}")
        league = get_user_leagues(user_id['user_id'], season="2023")
        # pprint(league[0])
        rosters = get_roster_ids(league[0]['league_id'])
        # pprint(rosters)
        user_roster = get_roster_by_id(rosters, user_id['user_id'])
        pprint(user_roster['players'])
        new_entry = Sleeper(user_id=user_id['user_id'], league_id=league[0]['league_id'], players=user_roster['players'])
        db.session.add(new_entry)
        db.session.commit()