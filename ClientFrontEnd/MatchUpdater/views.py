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
		print("Matches started: {0}, Matches remaining: {1}".format(len(matches_started), len(matches_not_started)))
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
		buffer_time_in_seconds = int(resp_json['buffer'])
		present_time = datetime.now()
		cut_off_time = present_time - timedelta(seconds=buffer_time_in_seconds) 
		matches_to_staging = self.moveStartedMatchesToStaging(cut_off_time)
		return HttpResponse("Matches moved to staging: {0}".format(matches_to_staging), status=200)

@method_decorator(csrf_exempt, name='dispatch')
class RefreshMatchesView(View):
	def __init__(self, *args, **kwargs):
		super(RefreshMatchesView, self).__init__(*args, **kwargs)

	def constructMatchObject(self, match_json):
		league_id = match_json['league_id']
		match_id = match_json['id']
		home_name = match_json['home_name']
		away_name = match_json['away_name']
		kick_off_time = datetime.strptime(match_json['date'] + " " + match_json['time'], "%Y-%m-%d %H:%M:%S")
		created_at = datetime.now().replace(tzinfo=pytz.UTC)
		return LatestMatchesData(league_id=league_id, match_id=match_id, home_name=home_name,
								 away_name=away_name, kick_off_time=kick_off_time, created_at=created_at)

	def checkMatchExists(self, match_obj):
		return LatestMatchesData.objects.filter(match_id__exact = match_obj.match_id).count() > 0 	# If match_id is present, return 1 > 0 -> True

	def updateMatchTable(self, matches, max_allowable_matches):
		current_matchs = LatestMatchesData.objects.count()
		new_matches_to_add = max(-1, max_allowable_matches - current_matchs)
		match_added_counter = 0
		for match_candidate in matches:
			if(match_added_counter > new_matches_to_add):
				break

			match_obj = self.constructMatchObject(match_candidate)			
			if not self.checkMatchExists(match_obj):
				match_obj.save()
				match_added_counter += 1
				print("Added match_id: {0}".format(match_obj.match_id))
			else:
				print("Match_id: {0} already exists".format(match_obj.match_id))
		print("Updated a total of {0} new matches".format(match_added_counter))
		return

	def post(self, request, *args, **kwargs):
		resp_json = json.loads(request.body)
		max_allowable_matches = int(resp_json['max_matches'])
		live_fixtures = PredictorApi.getLiveFixtures()
		self.updateMatchTable(live_fixtures, max_allowable_matches)
		return HttpResponse("Refreshed matches", status=200)

