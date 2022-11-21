import requests
import json 

#declare API URL as constant
API_URL = 'https://statsapi.web.nhl.com/api/v1'

#fetch bruins team data, expand roster info, served in JSON
response = requests.get(API_URL + '/standings')

data = response.json()
#pretty json using dumps
pretty = json.dumps(data, indent=4)

for team_record in data['records']:
	for team in team_record['teamRecords']:
		if team['team']['name'] == 'Boston Bruins':
			bruins_points = team['points']
		elif team['team']['name'] == 'Buffalo Sabres':
			sabres_points = team['points']

if bruins_points > sabres_points:
	print("The bruins are ",bruins_points - sabres_points, " points ahead of the sabres")
elif bruins_points < sabres_points:
	print("The sabres are ", sabres_points - bruins_points, " points ahead of the bruins")
else:
	print("The bruins and sabres are tied")

