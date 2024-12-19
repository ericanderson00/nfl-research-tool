import requests
import json
# from website import db
from website.models import PlayerInfo

url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerList"

headers = {
	"x-rapidapi-key": "38d3e355bfmsh9e8afb063bdd322p10c8abjsnd724ba830a42",
	"x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
response_data = response.json()

# Check response status and JSON validity
if response.status_code != 200:
    print(f"Error: Failed to fetch data, status code: {response.status_code}")
    exit()

try:
    response_data = response.json()
except json.JSONDecodeError:
    print("Error: Response is not valid JSON")
    exit()


def get_player_info(player_name):
    
    for player in response_data.get("body", []):
        if player.get("longName", "").lower() == player_name.lower():
            return {
                "id" : player.get("playerID"),
                "pos" : player.get("pos"),
                "profilePic" : player.get("espnHeadshot"),
                "team" : player.get("team"),
                "height" : player.get("height"),
                "weight" : player.get("weight"),
                "jerseyNum" : player.get("jerseyNum"),
                "longName" :player.get("longName")
                
            }
         
# def add_players_to_db(response_data):
#     existing_ids = {player.playerID for player in PlayerInfo.query.all()}
#     new_players = []
    
#     for player_data in response_data.get("body", []): 
        
#         player_id = player_data.get('playerID')
#         if player_id in existing_ids:
#             continue
        
#         if not player_data.get('longName'):
#             print(f"Skipping player with missing longName: {player_data}")
#             continue
        
#         new_player = PlayerInfo(
#             playerID=player_id,
#             longName=player_data.get('longName'),
#             pos=player_data.get('pos'),
#             team=player_data.get('team'),
#             teamID=player_data.get('teamID'),
#             headShot=player_data.get('espnHeadShot')
#         )
#         new_players.append(new_player)
    
#     if new_players:
#         db.session.bulk_save_objects(new_players)
#         db.session.commit()
#         print(f"{len(new_players)} players added successfully")
#     else:
#         print("No new players to add.")
    

if __name__ == "__main__":
    
    print("starting player db population")