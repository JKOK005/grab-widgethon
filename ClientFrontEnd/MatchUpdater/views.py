# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from MatchUpdater.models import *
from datetime import datetime, timedelta
from Predictor.PredictorApi import PredictorApi
import json
import pytz

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class GetMatchesView(View):
	def __init__(self, *args, **kwargs):
		super(GetMatchesView, self).__init__(*args, **kwargs)

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		resp_json = json.loads(request.body)
		match_counts = resp_json['count_limits']
		return HttpResponse("Success in get matches view: {0}".format(match_counts))

@method_decorator(csrf_exempt, name='dispatch')
class CleanMatchesView(View):
	def __init__(self, *args, **kwargs):
		super(CleanMatchesView, self).__init__(*args, **kwargs)

	def moveStartedMatchesToStaging(self, cut_off_time):
		cut_off_time_tz = cut_off_time.replace(tzinfo=pytz.UTC)
		matches_not_started = LatestMatchesData.objects.all().filter(kick_off_time__gte=cut_off_time_tz)
		matches_started = LatestMatchesData.objects.all().exclude(kick_off_time__gte=cut_off_time_tz)
		print("Matches started: {0}, Matches remaining: {2}".format(len(matches_started), len(matches_not_started)))
		matches_started_count = len(matches_started)
		try:
			for each_matches_started in matches_started:
				to_staging_model = LatestMatchesDataStaging()
				for each_field in each_matches_started._meta.fields:
					if(each_field.name == 'id'):
						pass
					val = getattr(each_matches_started, each_field.name)
					setattr(to_staging_model, each_field.name, val)
				to_staging_model.save()
				each_matches_started.delete()
			return matches_started_count
		except Exception as ex:
			print(ex)

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		resp_json = json.loads(request.body)
		buffer_time_in_seconds = resp_json['buffer']
		present_time = datetime.now()
		cut_off_time = present_time - timedelta(seconds=buffer_time_in_seconds) 
		matches_to_staging = self.moveStartedMatchesToStaging(cut_off_time)
		return HttpResponse("Matches moved to staging: {0}".format(matches_to_staging), status=200)

@method_decorator(csrf_exempt, name='dispatch')
class RefreshMatchesView(View):
	def __init__(self, *args, **kwargs):
		super(RefreshMatchesView, self).__init__(*args, **kwargs)

