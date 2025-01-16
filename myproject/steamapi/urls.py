from django.urls import path
from .views import SteamUserView
from . import views


urlpatterns = [
    path('steam/<str:steam_id>/', SteamUserView.as_view(), name='steam-user'),
    path('index/', views.index_view, name='index'),
    path("history/", views.history_view, name="history"),
]