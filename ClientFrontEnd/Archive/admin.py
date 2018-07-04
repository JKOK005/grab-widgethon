# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from Archive.models import *

# Register your models here.
class LatestMatchesDataArchiveAdmin(admin.ModelAdmin):
	pass

admin.site.register(LatestMatchesDataArchive, LatestMatchesDataArchiveAdmin)