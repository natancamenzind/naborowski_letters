from django.db import models


class Role(models.IntegerChoices):
    AUTHOR = 0, 'autor'
    RECEIVER = 1, 'odbiorca'
    MENTION = 2, 'wspomninie'
