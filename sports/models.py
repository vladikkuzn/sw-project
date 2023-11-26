# sports/models.py
from django.db import models


class Athlete(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    positions = models.ManyToManyField('Position', blank=True)
    teams = models.ManyToManyField('Team', blank=True)
    events = models.ManyToManyField('FootballEvent', blank=True)


class Position(models.Model):
    label = models.CharField(max_length=100)


class Team(models.Model):
    label = models.CharField(max_length=100)


class FootballEvent(models.Model):
    label = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    champions = models.CharField(max_length=100)
    athlete_names = models.TextField()
