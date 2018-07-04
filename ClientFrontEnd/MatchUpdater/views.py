# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.
class GetMatchesView(View):
	def __init__(self, *args, **kwargs):
		super(GetMatchesView, self).__init__(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		match_counts = kwargs['count_limits']
		return HttpResponse("Success in get matches view: {0}".format(match_counts))