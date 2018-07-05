#import urllib2
import os
import json

class PredictorApi(object):

	@staticmethod
	def getLiveFixtures():
		key = os.getenv('LIVE_SCORE_KEY')
		secret = os.getenv('LIVE_SCORE_SECRET_KEY')
		base_url = "http://livescore-api.com/api-client/fixtures/matches.json"
		req = urllib2.Request("{0}?key={1}&secret={2}".format(base_url, key, secret))
		response = urllib2.urlopen(req)
		
		if(response.code != 200):
			raise Exception("Live Score Fixture API errored out with code: {0}".format(response.code))
		json_response = json.loads(response.read())
		return json_response['data']['fixtures']
