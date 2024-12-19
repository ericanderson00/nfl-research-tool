import requests
from website import create_app, db
from website.models import GameLog, PlayerInfo

# app = create_app()

def fetch_and_fill_gamelogs():
    with app.app_context():
        
        players = PlayerInfo.query.all()
        
        
        url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLGamesForPlayer"

        headers = {
            "x-rapidapi-key": "38d3e355bfmsh9e8afb063bdd322p10c8abjsnd724ba830a42",
            "x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
        }

        
        
        
        for player in players:
            player_id = player.playerID
            querystring = {"playerID" : player_id}
            response = requests.get(url, headers=headers, params=querystring)
            response_data = response.json()
            
            if "body" in response_data:
                games = response_data["body"]
                
                for game_id, game_data in games.items():
                    long_name = game_data.get("longName", "Unknown player")
                    team_abv = game_data.get("team", "Unknown team")
                    fantasy_points = game_data.get("fantasyPoints")
                    
                    #get rec stats
                    receiving_stats = game_data.get("Receiving", {})
                    receptions = receiving_stats.get("receptions",0)
                    rec_yards = receiving_stats.get("recYds",0)
                    rec_td = receiving_stats.get("recTD",0)
                    long_rec = receiving_stats.get("longRec",0)
                    rec_avg = receiving_stats.get("recAvg",0)
                    targets = receiving_stats.get("targets",0)
                    
                    # get rushing stats
                    rushing_stats = game_data.get("Rushing", {})
                    rush_yards = rushing_stats.get("rushYds",0)
                    rush_avg = rushing_stats.get("rushAvg",0)
                    carries = rushing_stats.get("carries",0)
                    long_rush = rushing_stats.get("longRush",0)
                    rush_td = rushing_stats.get("rushTD",0)
                
                    # get passing stats
                    passing_stats = game_data.get("Passing", {})
                    pass_yards = passing_stats.get("passYds",0)
                    pass_comp = passing_stats.get("passCompletions",0)
                    pass_attempts = passing_stats.get("passAttempts",0)
                    pass_avg = passing_stats.get("passAvg",0)
                    pass_td = passing_stats.get("passTD",0)
                    interception = passing_stats.get("interceptions",0)
                    
                    
                    
                    new_game_log = GameLog(
                        gameID=game_id,
                        playerID=player_id,
                        longName=long_name,
                        teamAbv=team_abv,
                        
                        receptions=receptions,
                        recYds=rec_yards,
                        recTD=rec_td,
                        recAvg=rec_avg,
                        recLong=long_rec,
                        targets=targets,
                        
                        rushYards=rush_yards,
                        rushAvg=rush_avg,
                        carries=carries,
                        longRush=long_rush,
                        rushTD=rush_td,
                        
                        passYards=pass_yards,
                        passComp=pass_comp,
                        passAttempts=pass_attempts,
                        passAvg=pass_avg,
                        passTD=pass_td,
                        interceptions=interception,

                        fanPoints=fantasy_points,
                        )
                    
                    db.session.add(new_game_log)
                    # print(f"Added game log for game {game_id}")
                    
        try:
            db.session.commit()
            print("Game logs have been updated")
        except Exception as e:
            db.session.rollback()
            print(f"error commiting to the db: {e}")        
            
 
if __name__ == "__main__":
    fetch_and_fill_gamelogs()