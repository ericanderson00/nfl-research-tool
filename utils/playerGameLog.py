import requests
import json

from .playerListAPI import get_player_info


def get_player_game_log(player_name):
    player_info = get_player_info(player_name)
    
    if not player_info:
        return {"error": "Player not found"}
    
    player_id = player_info.get("id")
    player_pos = player_info.get("pos")
    # player_name = player_name.get("longName")
    player_name = get_player_info(player_name)["longName"]
    player_pic = player_info.get("profilePic")
    
    #api query and request
    querystring = {"playerID":player_id}

    url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLGamesForPlayer"

    headers = {
        "x-rapidapi-key": "38d3e355bfmsh9e8afb063bdd322p10c8abjsnd724ba830a42",
        "x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()    


    # right now only pulls data for rec and rushing

    if "body" in response_data:
        games = response_data["body"]
        
        game_log = []
        
        #game_id = key ; game_data = value
        for game_id, game_data in games.items():  # Loop through each game
            
            #gets player name and game id and prints
            player_name = game_data.get("longName")
            game_info = {
                "game_id": game_id,
                "player_name" : game_data.get("longName"),
                }
            
            rushing_stats = game_data.get("Rushing", {}) #get rushing stat
            rec_stats = game_data.get("Receiving", {})  # get receiving stats
            
            # print rec stat if it exists in dict
            if rushing_stats: 
                game_info["rushing_stats"] = rushing_stats
            else:
                game_info["rushing_stats"] = None
                    
            # print rusing stat if it exists in dict
            if rec_stats: 
                game_info["rec_stats"] = rec_stats
            else:
                game_info["rec_stats"] = None

            game_log.append(game_info)
        
        return {
            "player_id" :player_id,
            "player_name" : player_name,
            "player_pos" : player_pos,
            "game_log" : game_log,
            "player_pic": player_pic            
        }
        # this print was just to test endpoint on rapidapi to make sure the player id matches (delete later)
        # print(player_id)
    else:
        return {"Error":"No valid data found in response."}
    
    

if __name__ == "__main__":
    print(get_player_game_log("Justin Jefferson"))