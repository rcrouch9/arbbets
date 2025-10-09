import requests, sys
import database
    
def scrape_fd_api():
    url = "https://sbapi.on.sportsbook.fanduel.ca/api/content-managed-page?page=CUSTOM&customPageId=nfl&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    code = response.status_code
    if code != 200:
        print("Request Error: {code}")
        return
    
    markets = ["Moneyline", "Spread"]
    data = response.json()
    odds = []
    market = data["attachments"]["markets"]       
    for event in market:
        if market[event]["marketName"] in markets:
            teams = market[event]["runners"]
            data = {"gameId": market[event]["eventId"],
                    "market": market[event]["marketName"],
                    "awayTeam": teams[0]["nameAbbr"], 
                    "awayOddsAmerican": teams[0]["winRunnerOdds"]["americanDisplayOdds"]["americanOdds"], 
                    "awayOddsDecimal": teams[0]["winRunnerOdds"]["trueOdds"]["decimalOdds"]["decimalOdds"], 
                    "homeTeam": teams[1]["nameAbbr"], 
                    "homeOddsAmerican": teams[1]["winRunnerOdds"]["americanDisplayOdds"]["americanOdds"], 
                    "homeOddsDecimal": teams[1]["winRunnerOdds"]["trueOdds"]["decimalOdds"]["decimalOdds"], 
                    "startTime": market[event]["marketTime"],
                    "book": "Fanduel"}
            odds.append(data)
    database.insert(odds)