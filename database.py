import sqlite3
from datetime import datetime, timezone

con = sqlite3.connect('odds.db')
cur = con.cursor()

def insert(games):

    cur.execute('''
        CREATE TABLE IF NOT EXISTS odds (
            id INTEGER,
            market TEXT,
            awayTeam TEXT,
            awayOddsAmerican REAL,
            awayOddsDecimal REAL,
            homeTeam TEXT,
            homeOddsAmerican REAL,
            homeOddsDecimal REAL,
            startTime TEXT,
            book TEXT,
            PRIMARY KEY (id, market)
        )
    ''')
    cur.executemany('''INSERT OR IGNORE INTO odds (
                        id, 
                        market,
                        awayTeam, 
                        awayOddsAmerican,
                        awayOddsDecimal,
                        homeTeam, 
                        homeOddsAmerican,
                        homeOddsDecimal, 
                        startTime,
                        book
                    ) VALUES (
                        :gameId, 
                        :market,
                        :awayTeam, 
                        :awayOddsAmerican,
                        :awayOddsDecimal,
                        :homeTeam,
                        :homeOddsAmerican,
                        :homeOddsDecimal,
                        :startTime,
                        :book
        )
    ''', games)
    
    cur.executemany('''
        UPDATE odds
        SET awayOddsAmerican = :awayOddsAmerican, 
            awayOddsDecimal = :awayOddsDecimal,
            homeOddsAmerican = :homeOddsAmerican, 
            homeOddsDecimal = :homeOddsDecimal, 
            startTime = :startTime 
        WHERE id = :gameId AND market = :market AND book = :book
    ''', games)
    con.commit()

def drop_table():
    
    cur.execute("DROP TABLE IF EXISTS odds;")
    con.commit()    
    
def find_best_odds():
    
    cur.execute("DROP TABLE IF EXISTS best_odds;")
    cur.execute("""
        CREATE TABLE best_odds AS
        WITH max_home AS (
            SELECT *, 
                ROW_NUMBER() OVER (
                    PARTITION BY homeTeam, awayTeam, market 
                    ORDER BY homeOddsDecimal DESC
                ) AS rn
            FROM odds
        ),
        max_away AS (
            SELECT *, 
                ROW_NUMBER() OVER (
                    PARTITION BY homeTeam, awayTeam, market 
                    ORDER BY awayOddsDecimal DESC
                ) AS rn
            FROM odds
        )
        SELECT 
            h.market,
            h.homeTeam,
            a.awayTeam,
            h.homeOddsDecimal AS bestHomeTeamOdds,
            h.book AS homeBook,
            a.awayOddsDecimal AS bestAwayTeamOdds,
            a.book AS awayBook
        FROM max_home h
        JOIN max_away a
            ON h.homeTeam = a.homeTeam 
            AND h.awayTeam = a.awayTeam
            AND h.market = a.market
        WHERE h.rn = 1 AND a.rn = 1 AND h.book != a.book;
    """)


    
    """ cur.execute('''INSERT OR IGNORE INTO best_odds (
                        market,
                        awayTeam,
                        bestAwayTeamOdds,
                        awayBook,
                        homeTeam,
                        bestHomeTeamOdds,
                        homeBook
                    ) VALUES (
                        'Moneyline',
                        'oakley', 
                        1.80,
                        "Fanduel",
                        'finn',
                        2.30,
                        "DraftKings"
        )
    ''') """
    
    con.commit()
    
def read_odds():
    cur.execute("SELECT * FROM best_odds")
    return cur.fetchall()

def clean_up():
    cur.execute("SELECT id, startTime FROM odds")
    rows = cur.fetchall()

    for row in rows:
        row_id, start_time_str = row

        try:
            # Parse the startTime string into a datetime object
            # Remove the trailing 'Z' and parse the rest
            start_time = datetime.strptime(start_time_str[:-1], "%Y-%m-%dT%H:%M:%S.%f")
            start_time = start_time.replace(tzinfo=timezone.utc)

            # Get current UTC time
            now = datetime.now(timezone.utc)

            # If the game has started, delete the row
            if start_time <= now:
                cur.execute("DELETE FROM odds WHERE id = ?", (row_id,))
        except Exception as e:
            print(f"Error parsing time for row {row_id}: {e}")
    con.commit()
