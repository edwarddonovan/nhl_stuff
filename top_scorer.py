import requests
import json 

#declare API URL as constant
API_URL = 'https://statsapi.web.nhl.com/api/v1'

def get_team(user_input):
	#fetch team data, served in JSON
	response = requests.get(API_URL + '/teams')
	data = response.json()

	#get team id from user input
	team_id = 0
	for team in data['teams']:
		if team['name'].lower() == user_input:
			print(team['name'])
			team_id = team['id']
	return team_id

def get_players(team_id):
	#fetch team data, served in JSON
	response = requests.get(API_URL + '/teams/'+ str(team_id) +'?expand=team.roster')
	data = response.json()

	player_ids =[] #init list to hold player ids of the given team

	for team in data['teams']:
		for roster in team['roster']['roster']:
			player_ids.append(roster['person'].get('id'))
	return player_ids


def get_player_stats(player_ids, year_input):
	#we need a list of dictionaries to hold player stats
	player_stats = []

	#this time we loop over each player id to make unique requests to get their stat data
	for player_id in player_ids:
		response = requests.get(API_URL + '/people/' + str(player_id) + '/stats?stats=statsSingleSeason&season=' + str(year_input))
		data = response.json()
		try: 
			player_stats.append({'player_id' : player_id
								,'points' : data['stats'][0]['splits'][0]['stat']['points']
								,'goals' : data['stats'][0]['splits'][0]['stat']['goals']
								,'assists' : data['stats'][0]['splits'][0]['stat']['assists']
									})
		except: continue
	return player_stats

def get_top_scorer(player_stats, year_input):
	max_points = max(player_stats, key=lambda x:x['points'])
	for dict_items in player_stats:
		for key, value in dict_items.items():
			if value == max_points['points']:
				response = requests.get(API_URL + '/people/' + str(max_points['player_id']))
				data = response.json()
				print(data['people'][0]['fullName'] + " leads the team with " + str(max_points['goals']) + " goals and " + str(max_points['assists']) + " assists, for " + str(max_points['points']) + " points")
				response = requests.get(API_URL + '/people/' + str(max_points['player_id']) + '/stats?stats=regularSeasonStatRankings&season=' + str(year_input))
				data = response.json()
				rank = data['stats'][0]['splits'][0]['stat']['rankPoints']
				print("Which puts them " + rank + " in the NHL")





year_input = '20222023' #init year input as current season because it is annoying to type

user_input = input("Please enter a team name to recieve info on their leading scorer: ").lower()
#year_input = input("Please enter years of the season as YYYYYYYY - leave blank for 2022/2023 season: ") #this is broken because i am using current team rosters instead of team id

team_id = get_team(user_input)
player_ids = get_players(team_id)
player_stats = get_player_stats(player_ids,year_input)
get_top_scorer(player_stats,year_input)