# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from MatchUpdater.models import *

# Create your models here.
class LatestMatchesDataArchive(LatestMatchesData):
	def __str__(self):
		return str(self.league_id) + "-" + self.home_name + "-vs-" + self.away_name + "-archived"