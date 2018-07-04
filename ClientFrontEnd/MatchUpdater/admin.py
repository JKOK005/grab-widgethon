# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from MatchUpdater.models import *

# Register your models here.
@admin.register(LatestMatchesData)
class LatestMatchesDataAdmin(admin.ModelAdmin):
	pass

@admin.register(LatestMatchesDataStaging)
class LatestMatchesDataStagingAdmin(admin.ModelAdmin):
	pass