import database
import scrapers.fanduel_scrape as fanduel_scrape, scrapers.draftkings_scrape as draftkings_scrape
import arb_engine

database.connect_db()
database.clean_up()

fanduel_scrape.scrape_fd_api()
draftkings_scrape.scrape_dk_api()
    
database.find_best_odds()

opportunities = database.read_odds()

count = 0;
arb_lines = []
for line in opportunities:
    if (arb_engine.raise_implied(line)):
        count += 1
        arb_lines.append(line)
        
print(f"Found {count} arbitrage opportunities:")
for arb in arb_lines:
    print(arb)

if count == 0:
    print("No arbitrage opportunities found.")
    exit()
    
winnings = input("Enter your total desired winnings: $")

for arb in arb_lines:
    arb_engine.calculate_stakes(arb, winnings)