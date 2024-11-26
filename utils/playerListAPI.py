import requests
import json

url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerList"

headers = {
	"x-rapidapi-key": "38d3e355bfmsh9e8afb063bdd322p10c8abjsnd724ba830a42",
	"x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
response_data = response.json()

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

if __name__ == "__main__":
    
    player_info = get_player_info("Jayden Daniels")
    if player_info:
        print(player_info["id"])  # Accessing by key
        print(player_info["pos"])  # Accessing by key
    else:
        print("Player not found.")
            
    