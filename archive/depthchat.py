import requests, json
from website import create_app, db
from website.models import PlayerInfo

url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLDepthCharts"

headers = {
	"x-rapidapi-key": "38d3e355bfmsh9e8afb063bdd322p10c8abjsnd724ba830a42",
	"x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

response_data = response.json()

positions_to_extract = ["RB", "QB", "TE", "WR"]

def fetch_player_data():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    return response.json()




def add_players_to_db(response_data):
    with app.app_context():
        body = response_data["body"]
        
# for each team get depth chart team abv and ID
        for team in body:
            depth_chart = team.get("depthChart", {})
            team_abv = team.get("teamAbv")
            team_id = team.get("teamID")
            
            # print(f"Team: {team_abv}, Team ID: {team_id}")
            
            for pos in positions_to_extract:
                players = depth_chart.get(pos, [])
                # print(f"Position: {pos}")
                
                
                for i, player in enumerate(players):
                    depth_pos = player
                    player_id = player.get("playerID")
                    long_name = player.get("longName")
                    # print(f"{player['longName']} (ID: {player['playerID']})")
                    
                        
                    new_player = PlayerInfo(
                        playerID= player_id,
                        longName=long_name,
                        pos=pos,
                        depth_pos=i+1,
                        team=team_abv,
                        teamID=team_id
                        
                    )
                    db.session.add(new_player)
                    db.session.commit()
                    # print(f"Added player {long_name} (ID: {player_id}) to database.")

if __name__ == "__main__":
    app = create_app()
    response_data = fetch_player_data()
    if response_data:
        add_players_to_db(response_data)


    
    
    
            
    
    