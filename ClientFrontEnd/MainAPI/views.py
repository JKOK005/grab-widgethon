# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from MatchUpdater.models import *
from rest_framework.views import APIView, Response
import json, random

# Create your views here.
class GetLeaderboardView(View):
	def __init__(self, *args, **kwargs):

		super(GetLeaderboardView, self).__init__(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		return HttpResponse("Success in get matches view:")


class ListMatchesView(APIView):
	def get(self, request, format=None):
		league_names = {
		130 : "Singapore League", 
		297: "Indonesia League",
		802: "World Cup"
		}

		matches = LatestMatchesData.objects.all()
		latest_matches = {}

		for m in matches:	
			match_date = m.kick_off_time.strftime("%Y-%m-%d")

			if m.league_id in latest_matches.keys():
				if match_date in latest_matches.get(m.league_id).keys():
					latest_matches[m.league_id][match_date].append(m)
				else:
					latest_matches[m.league_id][match_date] = []
					latest_matches[m.league_id][match_date].append(m)
			else:
				res = {}

				latest_matches[m.league_id] = {}
				latest_matches[m.league_id][match_date] = []
				latest_matches[m.league_id][match_date].append(m)



		response = []

		for lk, lv in latest_matches.items():
			league = {}

			league["league_id"] = lk
			league["league_name"] = league_names.get(lk, "")
			league["league_img_url"] = ""

			match_days = []

			for dk, dv in lv.items():
				match_day = {}
				match_day["date"] = dk
				
				matches = []
				for m in dv: 
					res = {}
					res["match_id"] = m.match_id
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

		r = Response(response)

		r["Access-Control-Allow-Origin"] = "*"

		return r 
'''
		for key, value in leagues.items():
			response.match_days[l]
'''
			
		


class UpdatePredictionView(APIView):
	def post(self, request, format=None):
		req = json.loads(request.body)
		print(req)
		#insert to database


		r = Response({"success": "true"})

		r["Access-Control-Allow-Origin"] = "*"

		return r


		

class GetLeaderboardView(APIView):
	def get(self, request, *args, **kwargs):
		response = {}
		response["user_id"] = kwargs["user_id"]
		
		leagues = []
		for l in [130, 297] :
			league = {}
			league["league_id"] = l

			ranks = {}

			dummy_score = random.randint(3500, 3699)

			for r in range(1, 9):
				rank = {}
				rank["user_id"] = random.randint(100000, 2000000)
				rank["name"] = "John Doe"

				if (r == 6):
					dummy_score = random.randint(600, 800)
					dummy_rank = random.randint(90, 110)

				if (r < 6) :
					rank_number = str(r) 
					score = dummy_score
					dummy_score = random.randint(2500, dummy_score)
				else :
					rank_number = str(dummy_rank - r)
					score = dummy_score
					dummy_score = random.randint(400, dummy_score)

				rank["score"] = score
				
				ranks[rank_number] = rank
			
			league["ranks"] = ranks

			leagues.append(league)


		response["leagues"] = leagues


		r = Response(response)
		r["Access-Control-Allow-Origin"] = "*"


		return r