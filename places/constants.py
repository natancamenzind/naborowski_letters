from django.db import models


class PlaceRole(models.IntegerChoices):
    SEND_FROM = 0, 'wysłane z'
    RECEIVED_IN = 1, 'odebrane w'
    MENTION = 2, 'wspomninie'
