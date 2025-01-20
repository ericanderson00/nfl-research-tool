# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import time

# # Path to the ChromeDriver executable
# chrome_driver_path = "./chromedriver.exe"

# # Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run Chrome in headless mode
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

# # Set up the WebDriver
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # URL of the Fanduel Sportsbook NFL page
# url = 'https://sportsbook.fanduel.com/navigation/nfl'

# # Open the URL in the browser
# driver.get(url)

# # Wait for the page to load (you might need to adjust the sleep time)
# time.sleep(10)

# # Get the page source and parse it with BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# # Find the container that holds the betting odds
# labels = soup.find_all('span')

# for i in labels:
#     print(i)

# # Close the browser
# driver.quit()


import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL of the request
url = "https://smp.az.sportsbook.fanduel.com/api/sports/fixedodds/readonly/v1/getMarketPrices"

# Headers copied from the network tab
headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://sportsbook.fanduel.com",
    "referer": "https://sportsbook.fanduel.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/XX.XX.XXX Safari/537.36",
}

# Replace this with the exact payload seen in the request
payload = {
    "marketIds": [
        "704.108594473", "704.108594475", "704.108594472", "704.109118931", "704.109118929", "704.109118930",
        "704.108594801", "704.108594803", "704.108594800", "704.108592616", "704.108592615", "704.108592617"
    ]
}

def fetch_market_prices(url, headers, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def parse_market_prices(data):
    if not data or not isinstance(data, list):
        logging.error("Invalid response data")
        return []

    games = []
    for market in data:
        game = {
            "marketId": market.get("marketId"),
            "runners": []
        }
        for runner in market.get("runnerDetails", []):
            runner_data = {
                "runnerId": runner.get("runnerId"),
                "name": runner.get("runnerName"),
                "odds": runner.get("winRunnerOdds", {}).get("americanDisplayOdds", {}).get("americanOddsInt")
            }
            game["runners"].append(runner_data)
        games.append(game)
    return games

def main():
    response_data = fetch_market_prices(url, headers, payload)
    if response_data:
        games = parse_market_prices(response_data)
        for game in games:
            print(f"Game: {game['marketId']}")
            for runner in game['runners']:
                print(f"  Runner: {runner['name']} - Odds: {runner['odds']}")
    else:
        print("Failed to fetch market prices")

if __name__ == "__main__":
    main()