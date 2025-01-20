import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json




if __name__ == "__main__":
    
    
    # #This code gets the odds of the games at https://sportsbook.fanduel.com/navigation/nfl
    # import requests

    # # URL of the request
    # url = "https://smp.az.sportsbook.fanduel.com/api/sports/fixedodds/readonly/v1/getMarketPrices"

    # # Headers copied from the network tab
    # headers = {
    # "accept": "application/json",
    # "accept-encoding": "gzip, deflate, br, zstd",
    # "accept-language": "en-US,en;q=0.9",
    # "content-type": "application/json",
    # "origin": "https://sportsbook.fanduel.com",
    # "referer": "https://sportsbook.fanduel.com/",
    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/XX.XX.XXX Safari/537.36",
    # }

    # # Replace this with the exact payload seen in the request
    # payload = {
    #     # Populate the payload based on the "Payload" tab in your network request
    #     "marketIds":["704.108594473","704.108594475","704.108594472","704.109118931","704.109118929","704.109118930","704.108594801","704.108594803","704.108594800","704.108592616","704.108592615","704.108592617"]
    # }

    # # Send the POST request
    # response = requests.post(url, headers=headers, json=payload)
    # response_data = response.json()
    # # Handle the response
    # if response.status_code == 200:
    #     print("Response JSON:")
    #     counter = 1
    #     print(f"game{counter}")
                
    #     for i in response_data:
    #         for j in i["runnerDetails"]:
    #             print(j["winRunnerOdds"]["americanDisplayOdds"]["americanOddsInt"])
                
    #     print("test")
    #     # print(response.json())
    # else:
    #     print(f"Error: {response.status_code}")
    #     print(response.text)

    
    
    
    # driver = webdriver.Chrome()
    
    # url = "https://sportsbook.fanduel.com/navigation/nfl"
    
    # driver.get(url)
    
    # time.sleep(30)
    
    # headers = {
    # "accept": "application/json",
    # "accept-encoding": "gzip, deflate, br, zstd",
    # "accept-language": "en-US,en;q=0.9",
    # "content-type": "application/json",
    # "origin": "https://sportsbook.fanduel.com",
    # "referer": "https://sportsbook.fanduel.com/",
    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/XX.XX.XXX Safari/537.36",
    # }

    # response = requests.get(url,headers=headers)
    # print(response)
    # if response.status_code == 200:  # Check if the request was successful
    #     soup = BeautifulSoup(response.text, "html.parser")

    #     # Example: Finding elements by class
    #     spreads = soup.find_all(class_="kh ki aw ko ex bz")
    #     odds = soup.find_all(class_="kh ki fe ex ko kp bz")

    #     for spread, odd in zip(spreads, odds):  # Pair spreads and odds
    #         print("Spread:", spread.get_text(strip=True))
    #         print("Odds:", odd.get_text(strip=True))
    # else:
    #     print(f"Failed to fetch page. Status code: {response.status_code}")    
    
    
    
    
    
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import time

    driver = webdriver.Chrome()
    
    url = "https://sportsbook.fanduel.com/navigation/nfl"
    
    driver.get(url)
    
    time.sleep(30)

    # Get the rendered page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Scrape the data (adjust the classes as needed)
    spreads = soup.find_all(class_="kh ki aw ko ex bz")
    odds = soup.find_all(class_="kh ki fe ex ko kp bz")

    for spread, odd in zip(spreads, odds):
        print("Spread:", spread.get_text(strip=True))
        print("Odds:", odd.get_text(strip=True))

    # Close the browser
    driver.quit()
        