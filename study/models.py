from django.contrib.auth.models import User
from django.db import models


class Deck(models.Model):
    deck_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
