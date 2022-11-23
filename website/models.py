from . import db

class Team(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	team_name = db.Column(db.String(200))