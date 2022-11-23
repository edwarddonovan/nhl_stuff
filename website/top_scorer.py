import requests
import json 
from unidecode import unidecode


class TopScorer:
	#declare API URL as class attribute
	API_URL = 'https://statsapi.web.nhl.com/api/v1'

	def __init__(self, team_name):
		self.user_input = team_name
		self.year_input = '20222023' #init year input as current season because it is annoying to type

	def get_team(self):
		#fetch team data, served in JSON
		response = requests.get(TopScorer.API_URL + '/teams')
		data = response.json()

		#get team id from user input
		team_id = 0
		for team in data['teams']:
			if unidecode(team['name'].lower()) == self.user_input.lower():
				print(team['name'])
				team_id = team['id']
		if team_id > 0:
			self.team_id = team_id
		else:
			print("Please enter a valid team name (City and Team)")


	def get_players(self):
		#fetch team data, served in JSON
		response = requests.get(TopScorer.API_URL + '/teams/'+ str(self.team_id) +'?expand=team.roster')
		data = response.json()

		player_ids =[] #init list to hold player ids of the given team

		for team in data['teams']:
			for roster in team['roster']['roster']:
				player_ids.append(roster['person'].get('id'))
		self.player_ids = player_ids


	def get_player_stats(self):
		#we need a list of dictionaries to hold player stats
		player_stats = []

		#this time we loop over each player id to make unique requests to get their stat data
		for player_id in self.player_ids:
			response = requests.get(TopScorer.API_URL + '/people/' + str(player_id) + '/stats?stats=statsSingleSeason&season=' + str(self.year_input))
			data = response.json()
			try: 
				player_stats.append({'player_id' : player_id
									,'points' : data['stats'][0]['splits'][0]['stat']['points']
									,'goals' : data['stats'][0]['splits'][0]['stat']['goals']
									,'assists' : data['stats'][0]['splits'][0]['stat']['assists']
										})
			except: continue
		self.player_stats = player_stats

	def get_top_scorer(self):
		max_points = max(self.player_stats, key=lambda x:x['points'])
		for dict_items in self.player_stats:
			for key, value in dict_items.items():
				if value == max_points['points']:
					response = requests.get(TopScorer.API_URL + '/people/' + str(max_points['player_id']))
					data = response.json()
					line_1 = (data['people'][0]['fullName'] + " leads the team with " + str(max_points['goals']) + " goals and " + str(max_points['assists']) + " assists, for " + str(max_points['points']) + " points")
					response = requests.get(TopScorer.API_URL + '/people/' + str(max_points['player_id']) + '/stats?stats=regularSeasonStatRankings&season=' + str(self.year_input))
					data = response.json()
					rank = data['stats'][0]['splits'][0]['stat']['rankPoints']
					line_2 = (", which puts them " + rank + " in the NHL")

					return line_1 + '\n' + line_2

def main(team_name):
	while True:
		try:
			team = TopScorer(team_name)
			team.get_team()
			team.get_players()
			team.get_player_stats()
			return team.get_top_scorer()
		except:
			return "Please enter a valid team name (City and Team)"
		else:
			return "Please enter a valid team name (City and Team)"