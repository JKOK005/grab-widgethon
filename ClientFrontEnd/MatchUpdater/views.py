# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from MatchUpdater.models import *
from datetime import datetime, timedelta
import json

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

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		resp_json = json.loads(request.body)
		buffer_time_in_seconds = resp_json['buffer']
		present_time = datetime.now()
		cut_off_time = present_time - timedelta(seconds=buffer_time_in_seconds)
		