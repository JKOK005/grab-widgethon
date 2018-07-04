# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from MatchUpdater.models import *
import json

# Create your views here.
class GetLeaderboardView(View):
	def __init__(self, *args, **kwargs):

		super(GetLeaderboardView, self).__init__(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		return HttpResponse("Success in get matches view:")


class ListMatchesView(View):
	def __init__(self, *args, **kwargs):
		super(ListMatchesView, self).__init__(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		matches = LatestMatchesData.objects.all()
		leagues = {}

		for m in matches:	
			match_days = {}
			match_date = m.kick_off_time.strftime("%Y-%m-%d")

			if m.league_id in leagues.keys():
				print("here")
				if match_date in leagues.get(m.league_id).keys():
					match_days[league_id][match_date].append(m)
				else:
					leagues[m.league_id][match_date] = []
					leagues[m.league_id][match_date].append(m)
			else:
				res = {}

				leagues[m.league_id] = {}
				leagues[m.league_id][match_date] = []
				leagues[m.league_id][match_date].append(m)

		response = []

		print(leagues)

		for lk, lv in leagues.items():
			league = {}

			league["league_id"] = lk
			league["league_img_url"] = ""

			match_days = []

			for dk, dv in lv.items():
				match_day = {}
				match_day["date"] = dk
				
				matches = []
				for m in dv: 
					res = {}
					res["league_id"] = m.league_id
					res["home_name"] = m.home_name
					res["away_name"] = m.away_name
					res["kickoff_time"] = m.kick_off_time.strftime("%Y-%m-%d %H:%M:%S")
					#res["id"] = m.match_id
					res["id"] = 1

					matches.append(res)

				match_day["matches"] = matches

				match_days.append(match_day)

			league["match_days"] = match_days

			response.append(league)

		return HttpResponse(json.dumps(response))
'''
		for key, value in leagues.items():
			response.match_days[l]
'''
			
		


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePredictionView(View):
	def __init__(self, *args, **kwargs):
		super(UpdatePredictionView, self).__init__(*args, **kwargs)

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		resp_json = json.loads(request.body)
		match_counts = resp_json['request']

		#insert to database

		return HttpResponse("Success in get matches view: {0}")


		