from flask_restplus import fields, Model

_new_game_request = {"team1": fields.String(required=True),
                     "team2": fields.String(required=True),
                     "team1_score": fields.Integer(required=False),
                     "team2_score": fields.Integer(required=False),
                     }

new_game_request = Model("NewGameRequest", _new_game_request)

MODEL_LIST = [new_game_request]