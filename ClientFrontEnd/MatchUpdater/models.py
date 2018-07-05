# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class LatestMatchesData(models.Model):
	league_id = models.IntegerField(null=False)
	match_id = models.IntegerField(default=-1)
	home_name = models.CharField(max_length=20, blank=False)
	away_name = models.CharField(max_length=20, blank=False)
	kick_off_time = models.DateTimeField(auto_now=False)
	created_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.league_id) + "-" + self.home_name + "-vs-" + self.away_name

class LatestMatchesDataStaging(LatestMatchesData):
	def __str__(self):
		return str(self.league_id) + "-" + self.home_name + "-vs-" + self.away_name + "-staging"
	
class Prediction(models.Model):
	user_id = models.IntegerField()
	match_id = models.IntegerField()
	home_score = models.IntegerField()
	away_score = models.IntegerField()

	def __str__(self):
		return str(self.user_id) + "-" + self.match_id + " : " + self.home_score + "-" + self.away_score