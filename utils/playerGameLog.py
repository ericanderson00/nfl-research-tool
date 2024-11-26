import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

from .playerListAPI import get_player_info


def get_player_game_log(player_name):
    player_info = get_player_info(player_name)
    
    if not player_info:
        return {"error": "Player not found"}
    
    player_id = player_info.get("id")
    player_pos = player_info.get("pos")
    long_name = player_info.get("longName")
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
            
            game_info = {
                "game_id": game_id,
                "player_name" : game_data.get("longName"),
                }
            
            passing_stats = game_data.get("Passing", {}) #get passing stats default to empty dict if not exist
            rushing_stats = game_data.get("Rushing", {}) #get rushing stat default to empty dict if not exist
            rec_stats = game_data.get("Receiving", {})  # get receiving stats default to empty dict if not exist
            
            # if rushing stat exists in dict append to game_info
            if rushing_stats: 
                game_info["rushing_stats"] = rushing_stats
            else:
                game_info["rushing_stats"] = None
                    
            # if rec stat exists in dict append to game_info
            if rec_stats: 
                game_info["rec_stats"] = rec_stats
            else:
                game_info["rec_stats"] = None
            
            # if passing stat exists in dict append to game_info
            if  passing_stats:
                game_info["passing_stats"] = passing_stats
            else:
                game_info["passing_stats"] = None
                
            #append game_info to the game_log list
            game_log.append(game_info)
        
        return {
            "player_id" :player_id,
            "player_name" : long_name,
            "player_pos" : player_pos,
            "game_log" : game_log,
            "player_pic": player_pic            
        }
        # this print was just to test endpoint on rapidapi to make sure the player id matches (delete later)
        # print(player_id)
    else:
        return {"Error":"No valid data found in response."}

def get_and_plot_player_receptions(player_name):
    player_data = get_player_game_log(player_name)
    
    if "game_log" not in player_data:
        return {"error":"no game data found"}
    
    rec_data = []
    
    for game in player_data['game_log']:
        game_id = game['game_id']
        rec_stats = game.get('rec_stats', {})
        
        receptions = rec_stats.get('receptions', 0)
    
        rec_data.append({'game_id': game_id, 'receptions':receptions})
        
    if not rec_data:
        return {"error": "No reception data available"}
    
    game_ids = [str(game['game_id']) for game in rec_data]
    receptions = [float(game['receptions']) for game in rec_data]
    
    # make bar graph
    positions = range(len(receptions))
    
    plt.bar(game_ids, receptions, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.show()


if __name__ == "__main__":
    
    get_and_plot_player_receptions("Justin Jefferson")