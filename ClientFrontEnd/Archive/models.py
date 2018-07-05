# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from MatchUpdater.models import *

# Create your models here.
class LatestMatchesDataArchive(models.Model):
	league_id = models.IntegerField(null=False)
	match_id = models.IntegerField(default=-1)
	home_name = models.CharField(max_length=20, default=None)
	away_name = models.CharField(max_length=20, default=None)
	kick_off_time = models.DateTimeField(auto_now=False)
	created_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return str(self.league_id) + "-" + self.home_name + "-vs-" + self.away_name + "-archived"