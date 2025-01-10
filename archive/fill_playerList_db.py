import requests, json
from website import create_app, db
from website.models import PlayerInfo

###
## this file calls the tank01 api to get the data of all the players in the nfl and fill the sqlite player_info table
## to request playerID, player name, team, pos, profile pic


# I USED depthchart.py TO POPULATE THE PLAYERS TABLE NOT THIS ONE !!!!!!!!!!!


url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerList"

headers = {
	"x-rapidapi-key": "38d3e355bfmsh9e8afb063bdd322p10c8abjsnd724ba830a42",
	"x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
}


def fetch_player_data():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    return response.json()

def add_players_to_db(response_data):
    
    if not response_data or "body" not in response_data:
        print("Invalid response data!")
        return
    
    with app.app_context():
        
        
        new_players = []
    
        for player_data in response_data.get("body", []): 
            player_id = player_data.get('playerID')
            
            if PlayerInfo.query.filter_by(playerID=player_id).first():
                # print(f"Skipping player {player_data.get('longName')} with ID {player_id} (already exists)")
                continue
            
            if not player_data.get('longName'):
                print(f"Skipping player with missing longName: {player_data}")
                continue
            
            new_player = PlayerInfo(
                playerID=player_id,
                longName=player_data.get('longName'),
                pos=player_data.get('pos'),
                team=player_data.get('team'),
                teamID=player_data.get('teamID'),
                headShot=player_data.get('espnHeadshot')
            )
            new_players.append(new_player)
        
        if new_players:
            try:
                db.session.bulk_save_objects(new_players)
                db.session.commit()
                print(f"{len(new_players)} players added successfully")
            except Exception as err:
                db.session.rollback()
                print(f"Error while adding players: {err}")
        else:
            print("No new players to add.")
        
if __name__ == "__main__":
    app = create_app()
    response_data = fetch_player_data()
    if response_data:
        add_players_to_db(response_data)