import requests


def get_all_owned_games(API_KEY, steamid):
    # URL для метода GetPlayerSummaries
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"

    params = {
        "key": API_KEY,
        "steamid": steamid
    }

    response = requests.get(url, params=params)
    games_appids = list()

    if response.ok:
        data = response.json()
        for i in data:
            games = data[i]['games']
            for j in games:
                games_appids.append(j['appid'])
    else:
        print("Ошибка:", response.status_code)
        return []
    return games_appids


def get_sum_games_prices(COUNTRY_CODE, LANG, games_appids):
    url = f"https://store.steampowered.com/api/appdetails"
    total_price = 0

    for APPID in games_appids:
        params = {
            "appids": APPID,
            "cc": COUNTRY_CODE,
            "l": LANG
        }

        response = requests.get(url, params=params)
        if response.ok:
            data = response.json()
            game_data = data.get(str(APPID), {}).get("data", {})
            if game_data:
                price_info = game_data.get("price_overview", {})
                if price_info:
                    game_price = int(price_info.get('final_formatted')[:-5])
                    print(
                        f'Игра - {APPID} | Цена {price_info.get("final_formatted")} | Цена к суммированию {int(price_info.get('final_formatted')[:-5])}')
                    total_price += game_price
        else:
            print(f"Ошибка: {response.status_code}")
            return 0
    return total_price

def get(steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {"key": API_KEY, "steamid": steam_id, "include_appinfo": True}
    response = requests.get(url, params=params)
    if response.ok:
        data = response.json()
        total_cost = 0
        for game in data.get("response", {}).get("games", []):
            total_cost += get_game_price(game["appid"])

        return total_cost
    return 0

def get_game_price(appid):
    url = f"https://store.steampowered.com/api/appdetails"
    params = {"appids": appid, "cc": "ru", "l": "ru"} # cc - COUNTRY_CODE, l - LANG
    response = requests.get(url, params=params)
    data = response.json()
    price_info = data.get(str(appid), {}).get("data", {}).get("price_overview", {})
    return price_info.get("final", 0) / 100

if __name__ == "__main__":
    total_cost = get(steam_id="76561198218141793")
    print(total_cost)
    # API_KEY = API_KEY
    # steamid = "76561198218141793"
    # COUNTRY_CODE = "ru"
    # LANG = "ru"
    # games_appids = get_all_owned_games(API_KEY, steamid)
    # print(get_sum_games_prices(COUNTRY_CODE, LANG, games_appids))
