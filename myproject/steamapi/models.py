from django.db import models

class SteamUser(models.Model):
    steam_id = models.CharField(max_length=17, unique=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
