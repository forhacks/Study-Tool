from django.db import models


class Deck(models.Model):
    deck_name = models.CharField(max_length=100)


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
