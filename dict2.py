import requests, json
from website import create_app, db
from website.models import PlayerInfo
from os import path
from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask

app = create_app()
with app.app_context():
  
  with open('playersDepthChartJSON.json', 'r') as file:
    response_data = json.load(file)
    
  body = response_data["body"]

  positions_to_extract = ["RB", "QB", "TE", "WR"]
  max_depths = {"RB": 3, "QB": 3, "WR": 5, "TE": 2}


    

  for team in response_data["body"]:
      team_abv = team.get("teamID")
      depthChartDict = team.get("depthChart")
      team_id = team.get("teamAbv")
      
      for pos in positions_to_extract:
        players = depthChartDict.get(pos, [])
        max_depth = max_depths.get(pos, 3)
        
        for depth, player in enumerate(players[:max_depth]):
          name = player.get("longName")
          depth_position = player.get("depthPosition")
          player_id = player.get("playerID")
          print(f"{name}, {depth_position}, {player_id}, {team_abv}, {team_id}")
          
          new_player = PlayerInfo(
            playerID= player_id,
            longName=name,
            pos=pos,
            depth_pos=depth_position,
            team=team_abv,
            teamID=team_id
          )
          db.session.add(new_player)
          db.session.commit()  

# if __name__ == "__main__":
#     app = create_app()





