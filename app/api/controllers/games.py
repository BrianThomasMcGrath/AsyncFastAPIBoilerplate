from flask import request
from flask_restplus import Resource, Namespace

from app.api.models import new_game_request
from app.core.services.scoreboard import ScoreBoardService

games = Namespace('games', description="Games that have been played")

scoreboard_service = ScoreBoardService()

@games.route('/')
class Games(Resource):
    def get(self):
        """
        Gets all time games that have been played on the system
        
        Arguments:
            Resource {Games} -- Instance of Games Resource
        """
        raise NotImplementedError

    @games.expect(new_game_request)
    def post(self):
        """
        Starts a new game for tweetboard to report
        
        Returns:
            int -- id of game that has been created
        """

        kwargs = {
            "team1": request.body.get('team1'),
            "team2": request.body.get('team2'),
            "team1_score": request.body.get('team1_score', 0),
            "team2_score": request.body.get('team2_score', 0)
        }
        

        game_id = scoreboard_service.new_game(**kwargs)

        return {"game_id": game_id}, 201

@games.route('/<game_id>')
class SingleGame(Resource):

    def get(self, game_id):
        raise NotImplementedError

@games.route('/<game_id>/team/<team_name>')
class SingleGameTeam(Resource):

    def get(self, game_id, team_name):
        """
        Gets the score of a specific team
        
        Arguments:
            game_id {int} -- Game id of game in question
            team_name {string} -- Name of team to get the score of
        
        Raises:
            NotImplemented: Not Implemented Currently
        """
        raise NotImplementedError

    def post(self, game_id, team_name):

        score = request.body('score')

        if score is None:
            scoreboard_service.add_one(game_id, team_name)
        else:
            scoreboard_service.set_score(game_id, team_name, score)
    
        return {"message": "Score Changed"}, 201
    
    def delete(self, game_id, team_name):

        scoreboard_service.delete_one(game_id, team_name)

        return 200
    


