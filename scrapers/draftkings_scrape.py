import requests, sys
import database
    
def scrape_dk_api():
    url = "https://sportsbook-nash.draftkings.com/sites/CA-ON-SB/api/sportscontent/controldata/league/leagueSubcategory/v1/markets?isBatchable=false&templateVars=88808%2C4518&eventsQuery=%24filter%3DleagueId%20eq%20%2788808%27%20AND%20clientMetadata%2FSubcategories%2Fany%28s%3A%20s%2FId%20eq%20%274518%27%29&marketsQuery=%24filter%3DclientMetadata%2FsubCategoryId%20eq%20%274518%27%20AND%20tags%2Fall%28t%3A%20t%20ne%20%27SportcastBetBuilder%27%29&include=Events&entity=events"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    code = response.status_code
    if code != 200:
        print("Request Error: {code}")
        return
    
    data = response.json()
    odds = []
    market = data["selections"]
    events = data["events"]
    for i in range(0, len(market), 6):
        startTime = events[i//6]["startEventDate"][:-5] + "Z"
        mlData = {"gameId": int(market[i]["marketId"]),
                    "market": "Moneyline",
                    "awayTeam": market[i]["participants"][0]["name"],
                    "awayOddsAmerican": int(market[i]["displayOdds"]["american"].replace('−', '-')),
                    "awayOddsDecimal": float(market[i]["displayOdds"]["decimal"].replace('−', '-')),  
                    "homeTeam": market[i+1]["participants"][0]["name"], 
                    "homeOddsAmerican": int(market[i+1]["displayOdds"]["american"].replace('−', '-')), 
                    "homeOddsDecimal": float(market[i+1]["displayOdds"]["decimal"].replace('−', '-')), 
                    "startTime": startTime,
                    "book": "DraftKings"}
        hcData = {"gameId": int(market[i+2]["marketId"]),
                    "market": "Spread",
                    "awayTeam": market[i+2]["participants"][0]["name"],
                    "awayOddsAmerican": int(market[i+2]["displayOdds"]["american"].replace('−', '-')),
                    "awayOddsDecimal": float(market[i+2]["displayOdds"]["decimal"].replace('−', '-')),  
                    "homeTeam": market[i+3]["participants"][0]["name"], 
                    "homeOddsAmerican": int(market[i+3]["displayOdds"]["american"].replace('−', '-')), 
                    "homeOddsDecimal": float(market[i+3]["displayOdds"]["decimal"].replace('−', '-')), 
                    "startTime": startTime,
                    "book": "DraftKings"}
        odds.append(mlData)
        odds.append(hcData)       
    database.insert(odds)