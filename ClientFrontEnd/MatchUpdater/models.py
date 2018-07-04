# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class LatestMatchesData(models.Model):
	league_id = models.IntegerField()
	home_name = models.CharField(max_length=20, blank=False)
	away_name = models.CharField(max_length=20, blank=False)
	kick_off_time = models.DateTimeField(auto_now=False)