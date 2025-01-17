# steamapi/views.py
import os
import datetime as dt
from pathlib import Path

from django.http import JsonResponse
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SteamUser
from .serializers import SteamUserSerializer
import requests


load_dotenv(dotenv_path=Path('../..') / '.env.secret', override=True)
API_KEY = os.environ.get('API_KEY')

def home_redirect(request):
    return redirect('/api/index')

def index_view(request):
    return render(request, 'index.html')

def history_view(request):
    # Фильтрация записей за последние сутки
    last_day = dt.datetime.now() - dt.timedelta(days=1)
    history = SteamUser.objects.filter(last_updated__gte=last_day).values(
        "steam_id", "total_cost", "last_updated"
    )
    return JsonResponse(list(history), safe=False)

class SteamUserView(APIView):
    def get(self, request, steam_id):
        url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
        params = {"key": API_KEY, "steamid": steam_id, "include_appinfo": True}
        response = requests.get(url, params=params)
        if response.ok:
            data = response.json()
            total_cost = 0
            for game in data.get("response", {}).get("games", []):
                total_cost += self.get_game_price(game["appid"])

            user, created = SteamUser.objects.update_or_create(
                steam_id=steam_id,
                defaults={"total_cost": total_cost},
            )
            serializer = SteamUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Steam API error"}, status=status.HTTP_400_BAD_REQUEST)

    def get_game_price(self, appid):
        url = f"https://store.steampowered.com/api/appdetails"
        params = {"appids": appid, "cc": "ru", "l": "ru"} # cc - COUNTRY_CODE, l - LANG
        response = requests.get(url, params=params)
        data = response.json()
        price_info = data.get(str(appid), {}).get("data", {}).get("price_overview", {})
        return price_info.get("final", 0) / 100
