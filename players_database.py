from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, timezone
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Players.sqlite3'
db.init_app(app)

'''
Define a model for the Player data we want to store.
'''
class Player(db.Model):
    player_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=True)
    team = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    data = db.Column(db.JSON, nullable=False)



def update_player_database():
    from sleeper_api import get_player_data
    with app.app_context():
        db.create_all()  # Create tables
        players = get_player_data()
        for player_id, details in players.items():
            print(f"Processing player: {player_id} - {details.get('first_name', 'Unknown')} {details.get('last_name', 'Unknown')} - {details.get('position', 'Unknown')} - {details.get('team', 'Unknown')}")
        
            new_player = Player(
                player_id=player_id,
                name=f"{details.get('first_name', 'Unknown')} {details.get('last_name', 'Unknown')}",
                position=details.get('position', 'Unknown'),
                team=details.get('team', 'Unknown'),
                data=details
            )
            db.session.merge(new_player)  # Use merge to handle updates
        db.session.commit()

'''
In main we first get the current player data and then
create new objects that we can add to the database.
'''
if __name__ == "__main__":
    update_player_database()
    print("Player database updated.")
