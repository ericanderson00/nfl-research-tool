import requests

# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = 'f532d86c1852e792e8ca334450c7ad0d'

SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'american' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# sports_response = requests.get(
#     'https://api.the-odds-api.com/v4/sports', 
#     params={
#         'api_key': API_KEY
#     }
# )


# if sports_response.status_code != 200:
#     print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

# else:
#     print('List of in season sports:', sports_response.json())



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get(
    # f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    f'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={API_KEY}&regions=us&markets={MARKETS}&oddsFormat=american',
    # f'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={API_KEY}&regions=us&markets=h2h,spreads&oddsFormat=american'
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    
    #initalize list of dict from the odds api response
    game_odds = []

    for game in odds_json:
        # Iterate through bookmakers
        for bookmaker in game['bookmakers']:
            if bookmaker['key'] in ['fanduel', 'draftkings']:  # Filter by FanDuel and DraftKings
                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':  # Filter by "h2h" market
                        game_odds.append({
                            'game_id': game['id'],
                            'home_team': game['home_team'],
                            'away_team': game['away_team'],
                            'bookmaker': bookmaker['key'],
                            'outcomes': market['outcomes']
                        })
    
    # Print the filtered outcomes
    for outcome in game_odds:
        print(outcome)

    
    # print('Number of events:', len(odds_json))
    # print(odds_json)

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])