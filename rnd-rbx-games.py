import random
import requests
from datetime import datetime
from dateutil import parser

def get_universe_id(place_id):
    url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("universeId")
    return None

def get_user_join_date(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return parser.parse(resp.json()["created"])
    return None

def is_valid_game(universe_id):
    url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        games = data["data"]
        if not games:
            return False
        game = games[0]
        title = game["name"]
        price = game["price"]
        creator = game["creator"]
        game_created = parser.parse(game["created"])
        if "'s Place" in title or price:
            return False
        user_created = get_user_join_date(creator["id"])
        if user_created:
            delta = abs((game_created - user_created).total_seconds())
        if delta < 600:  # less than 10 minutes
            return False
        return True
    return False

# Main loop
for _ in range(100): # Try 20 random games
    place_id = random.randint(1000000, 1700000000)
    universe_id = get_universe_id(place_id)
    if universe_id and is_valid_game(universe_id):
        print(f"Interesting game: https://www.roblox.com/games/{place_id}")
