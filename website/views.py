from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Team
from . import db
from . import top_scorer
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		team_name = request.form.get('team')

		player_result = top_scorer.main(team_name)
		

		return render_template("result.html", player=player_result)

	return render_template("home.html")