from flask import Blueprint
from flask_restplus import Api

from app.api.controllers.games import games
from app.api.models import MODEL_LIST

blueprint = Blueprint('api', import_name=__name__)
api = Api(blueprint, name="Tweetboard", title="Tweetboard", description="Scoreboard that automatically updates a team's twitter")

api.add_namespace(games)

for model in MODEL_LIST:
    api.models[model.name] = model