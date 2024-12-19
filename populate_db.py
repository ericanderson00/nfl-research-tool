import os
import json
import subprocess
from website import create_app, db
from website.models import PlayerInfo, GameLog
from sqlalchemy.exc import IntegrityError


#i put the data outside of the project folder to i could commit changes to my main project
repo_url = "https://github.com/hvpkod/NFL-Data.git"  # Replace with your repo URL
data_path = r"C:\Users\eric-\SoftwareProjects\Personal\sportsResearchTool\NFL-Data\NFL-data-Players"  # Path where you want the repo cloned
app = create_app()


def clone_and_update_repo():

    # Check if the repo already exists
    if not os.path.exists(data_path):
        print("Repository not found, cloning...")
        subprocess.run(["git", "clone", repo_url, data_path], check=True)
    else:
        print("Repository already exists, pulling latest changes...")
        subprocess.run(["git", "-C", data_path, "pull"], check=True)


### -------------- This script uses the data from the github that i have saved ---------------------
# def populate_database():
#     with app.app_context():
#         for year in os.listdir(data_path):  # Loop through year folders
#             if int(year) < 2021:
#                 continue
#             year_path = os.path.join(data_path, year)
    
#             if os.path.isdir(year_path):
#                 for week in os.listdir(year_path):  # Loop through week folders
#                     week_path = os.path.join(year_path, week)
                    
#                     if not os.path.isdir(week_path) or week == "projected":
#                         continue
                    
#                     for file in os.listdir(week_path):  # Loop through JSON files
#                         if not file.endswith(".json") or "season" in file.lower():  # Skip unwanted JSON files
#                             continue
#                         if file.endswith(".json"):
#                             pos = file.replace(".json", "")
#                             file_path = os.path.join(week_path, file)

#                             # Load the JSON data
#                             with open(file_path, "r") as f:
#                                 data = json.load(f)

#                             for player in data:  # Process each player's data
#                                 player_id = int(player["PlayerId"])
#                                 player_name = player["PlayerName"]
#                                 position = player["Pos"]
#                                 team = player["Team"]

#                                 # 1. Check if PlayerInfo already exists
#                                 existing_player = PlayerInfo.query.filter_by(playerID=player_id).first()
#                                 if not existing_player:  # Add new player if they don't exist
#                                     new_player = PlayerInfo(
#                                         playerID=player_id,
#                                         playerName=player_name,
#                                         pos=position,
#                                         team=team
#                                     )
#                                     db.session.add(new_player)

#                                 # 2. Check if GameLog already exists for this player, year, and week
#                                 existing_log = GameLog.query.filter_by(
#                                     playerID=player_id,
#                                     year=(year),
#                                     week=int(week.replace("week_", ""))
#                                 ).first()

#                                 if not existing_log:  # Add game log only if it doesn't exist
#                                     game_log = GameLog(
#                                         playerID=player_id,
#                                         playerOpp=player.get("PlayerOpponent"),
#                                         week=int(week.replace("week_", "")),
#                                         year=int(year),
                                        
#                                         rushYards=int(player.get("RushingYDS", 0) or 0),
#                                         rushTD=int(player.get("RushingTD", 0) or 0),
                                        
#                                         receptions=int(player.get("ReceivingRec", 0) or 0),
#                                         recYds=int(player.get("ReceivingYDS", 0) or 0),
#                                         recTD=int(player.get("ReceivingTD", 0) or 0),
                                        
#                                         passYards=int(player.get("PassingYDS", 0) or 0),
#                                         passTD=int(player.get("PassingTD", 0) or 0),
#                                         interceptions=int(player.get("PassingInt", 0) or 0),
                                        
#                                         targets=int(player.get("Targets", 0) or 0),
#                                         carries=int(player.get("TouchCarries", 0) or 0)
#                                     )
#                                     db.session.add(game_log)

#         # Commit all changes to the database after processing all files
#         db.session.commit()
#         print("Database successfully populated with the latest data!")
def populate_database():
    with app.app_context():
        
        # Preload all players and game logs to avoid redundant database queries
        existing_players = {player.playerID: player for player in PlayerInfo.query.all()}
        existing_game_logs = {
            (log.playerID, log.year, log.week): log for log in GameLog.query.all()
        }

        # Prepare batch lists for adding new records
        new_players = []
        new_game_logs = []

        for year in os.listdir(data_path):  # Loop through year folders
            if int(year) < 2021:
                continue
            year_path = os.path.join(data_path, year)

            if os.path.isdir(year_path):
                for week in os.listdir(year_path):  # Loop through week folders
                    week_path = os.path.join(year_path, week)

                    if not os.path.isdir(week_path) or week == "projected":
                        continue
                    
                    for file in os.listdir(week_path):  # Loop through JSON files
                        if not file.endswith(".json") or "season" in file.lower():  # Skip unwanted JSON files
                            continue

                        file_path = os.path.join(week_path, file)
                        pos = file.replace(".json", "")

                        # Load the JSON data
                        with open(file_path, "r") as f:
                            data = json.load(f)

                        for player in data:  # Process each player's data
                            player_id = int(player["PlayerId"])
                            player_name = player["PlayerName"]
                            position = player["Pos"]
                            team = player["Team"]

                            # Add new player if they don't exist
                            if player_id not in existing_players:
                                new_player = PlayerInfo(
                                    playerID=player_id,
                                    playerName=player_name,
                                    pos=position,
                                    team=team
                                )
                                new_players.append(new_player)
                                existing_players[player_id] = new_player  # Cache the new player

                            # Check if GameLog already exists
                            week_number = int(week.replace("week_", ""))
                            if (player_id, int(year), week_number) not in existing_game_logs:
                                game_log = GameLog(
                                    playerID=player_id,
                                    playerOpp=player.get("PlayerOpponent"),
                                    week=week_number,
                                    year=int(year),
                                    rushYards=int(player.get("RushingYDS", 0) or 0),
                                    rushTD=int(player.get("RushingTD", 0) or 0),
                                    receptions=int(player.get("ReceivingRec", 0) or 0),
                                    recYds=int(player.get("ReceivingYDS", 0) or 0),
                                    recTD=int(player.get("ReceivingTD", 0) or 0),
                                    passYards=int(player.get("PassingYDS", 0) or 0),
                                    passTD=int(player.get("PassingTD", 0) or 0),
                                    interceptions=int(player.get("PassingInt", 0) or 0),
                                    targets=int(player.get("Targets", 0) or 0),
                                    carries=int(player.get("TouchCarries", 0) or 0)
                                )
                                new_game_logs.append(game_log)
                                existing_game_logs[(player_id, int(year), week_number)] = game_log  # Cache the new log

        # Bulk insert all new players and game logs
        if new_players:
            db.session.bulk_save_objects(new_players)
        if new_game_logs:
            db.session.bulk_save_objects(new_game_logs)

        # Commit all changes to the database at once
        db.session.commit()
        print("Database successfully populated with the latest data!")
        


print("Starting repository update and database population...")
# clone_and_update_repo()  # Clone or pull the latest data
populate_database()  # Populate the database with the latest data
print("All tasks completed successfully!")