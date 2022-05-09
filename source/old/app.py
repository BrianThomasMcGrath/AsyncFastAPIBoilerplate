from flask import Flask, request, redirect, url_for, session, g, flash, \
     render_template, jsonify, json
from flask_oauth import OAuth
from flaskext.mysql import MySQL
import flask.ext.login as flask_login
from datetime import datetime
import operator
 
# configuration
SECRET_KEY = '*******'
DEBUG = True
 
# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()


mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '******'
app.config['MYSQL_DATABASE_DB'] = 'tweetboard'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

 
# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authorize',
    # the consumer keys from the twitter application registry.
    consumer_key='**',
    consumer_secret='**'
)
 
 
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')
 
@app.route('/')
def index():
	if hasattr(flask_login.current_user, 'id'):
		return redirect(url_for('user'))
	else:
		return redirect(url_for('register_user'))

@app.route('/tweetboard/<gameID>')
def tweetboard(gameID):
	global players
	cursor.execute("SELECT team1, team2, tournament, t1_score, t2_score FROM games WHERE gameID={0}".format(int(gameID)))
	data = cursor.fetchone()
	team1 = data[0]
	team2 = data[1]
	tournament = data[2]
	score1=data[3]
	score2=data[4]

	cursor.execute("SELECT first_name, last_name FROM Players WHERE last_game={0}".format(int(gameID)))
	players = cursor.fetchall()

	return render_template('index.html', gameID=gameID, team1=team1, team2=team2, score1=score1, score2=score2, tournament=tournament, screen_name=session['screen_name'], players=players, name=flask_login.current_user.id)
 
@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))
 
 
@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('logout_user'))
 
 
@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('tweetboard')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
 
    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']
 
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
 
 
    return redirect(url_for('index'))


@app.route('/team1/<gameID>')
@twitter.authorized_handler
def scoreTeam1(arg, gameID):

	if request.method == 'GET':
		cursor.execute("UPDATE games SET t1_score= t1_score + 1 WHERE gameID={0}".format(int(gameID)))
		conn.commit()

		cursor.execute("SELECT team1, team2, tournament, t1_score, t2_score FROM games WHERE gameID={0}".format(int(gameID)))
		data = cursor.fetchone()
		team1 = data[0]
		team2 = data[1]
		tournament = data[2]
		score1=data[3]
		score2=data[4]

		if request.args.get('score') != None:
			scorer = request.args.get('score')
		if request.args.get('assist') != None:
			assist = request.args.get('assist')

		if (request.args.get('home'))!= team1 or (request.args.get('away')) != team2:
			return redirect(url_for('start_game'))
		#tweetScore(request.message)
		winner = ''
		if score1 > score2:
			winner = team1
		elif score2 > score1:
			winner = team2
		if request.args.get('message')!= '':
			message = request.args.get('message')
			status = message + ' ' + str(score1) + "-" + str(score2) + ' '+ winner + " #" + tournament.replace(' ','')
		else:
			status = str(score1) + "-" + str(score2) + ' '+ winner + " #" + tournament.replace(' ','')

		if request.args.get('score') != None and request.args.get('assist') != None:
			scorer = request.args.get('score')
			assist = request.args.get('assist')
			updatePlayerStats(scorer, team1, 1, 0)
			updatePlayerStats(assist, team1, 0,1)
			status = scorer + " to " + assist + ", " + status
			

		resp = twitter.post('https://api.twitter.com/1.1/statuses/update.json', data={
			'status': status 
		})
		print('response')
		print(resp.status)
		if resp.status == 403:
			flash('Your tweet was too long.')
		elif resp.status == 401:
			flash('Authorization error with Twitter.')
		elif resp.status == 405:
			flash('figure this ish out')
		else:
			flash('swag')
	return redirect('/tweetboard/' + gameID)

@app.route('/team2/<gameID>')
@twitter.authorized_handler
def scoreTeam2(arg,gameID):
	if request.method == 'GET':
		cursor.execute("SELECT team1, team2, tournament FROM games WHERE gameID={0}".format(int(gameID)))
		data = cursor.fetchone()
		team1 = data[0]
		team2 = data[1]
		tournament = data[2]
		


		
		if request.args.get('score1') != None:
			score1= int(request.args.get('score1'))
		if request.args.get('score2') != None:
			score2 = int(request.args.get('score2'))
		if (request.args.get('home'))!= team1 or (request.args.get('away')) != team2:
			return redirect(url_for('start_game'))
		#tweetScore(request.message)
		cursor.execute("UPDATE games SET t2_score= t2_score + 1 WHERE gameID={0}".format(int(gameID)))
		conn.commit()
		#tweetScore(request.message)
		cursor.execute("SELECT t1_score, t2_score FROM games WHERE gameID={0}".format(int(gameID)))
		d= cursor.fetchone()
		score1=d[0]
		score2=d[1]
		winner = ''
		if score1 > score2:
			winner = team1
		elif score2 > score1:
			winner = team2
		if request.args.get('message')!= '':
			message = request.args.get('message')
			status = message + ' ' + str(score1) + "-" + str(score2) + ' '+ winner + " #" + tournament.replace(' ','')
		else:
			status = str(score1) + "-" + str(score2) + ' '+ winner+ " #" + tournament.replace(' ','')
		resp = twitter.post('https://api.twitter.com/1.1/statuses/update.json', data={
			'status': status
		})
		print('response')
		print(resp.status)
		if resp.status == 403:
			flash('Your tweet was too long.')
		elif resp.status == 401:
			flash('Authorization error with Twitter.')
		elif resp.status == 405:
			flash('figure this ish out')
		else:
			flash('swag')
	return redirect('/tweetboard/' + gameID)

@app.route('/tweetScore/<gameID>')
@twitter.authorized_handler
def tweetScore(arg,gameID):
	if request.method == 'GET':
		cursor.execute("SELECT team1, team2, tournament, t1_score, t2_score FROM games WHERE gameID={0}".format(int(gameID)))
		data = cursor.fetchone()
		team1 = data[0]
		team2 = data[1]
		tournament = data[2]
		score1=data[3]
		score2=data[4]

		
		if request.args.get('score1') != None:
			score1= int(request.args.get('score1'))
		if request.args.get('score2') != None:
			score2 = int(request.args.get('score2'))
		if (request.args.get('home'))!= team1 or (request.args.get('away')) != team2:
			return redirect(url_for('start_game'))
		#tweetScore(request.message)
		#tweetScore(request.message)
		winner = ''
		if score1 > score2:
			winner = team1
		elif score2 > score1:
			winner = team2
		if request.args.get('message')!= '':
			message = request.args.get('message')
			status = message + ' ' + str(score1) + "-" + str(score2) + ' '+ winner + " #" + tournament.replace(' ', '')
		else:
			status = str(score1) + "-" + str(score2) + ' '+ winner+ " #" + tournament.replace(' ','')
		resp = twitter.post('https://api.twitter.com/1.1/statuses/update.json', data={
			'status': status
		})
		print('response')
		print(resp.status)
		if resp.status == 403:
			flash('Your tweet was too long.')
		elif resp.status == 401:
			flash('Authorization error with Twitter.')
		elif resp.status == 405:
			flash('figure this ish out')
		else:
			flash('swag')
	return redirect('/tweetboard/' + gameID)

def updatePlayerStats(name, team, score, assist):
	n = name.split(" ")
	cursor.execute("UPDATE Players SET scores = scores + {0}, assists = assists + {1} WHERE team = '{2}' AND first_name = '{3}' AND last_name ='{4}'".format(score,assist,team,n[0],n[1]))
	conn.commit()
	return

@app.route('/submit/<gameID>')
@twitter.authorized_handler
def submit(args,gameID):
	cursor.execute("SELECT team1, team2, tournament, t1_score, t2_score FROM games WHERE gameID={0}".format(int(gameID)))
	data = cursor.fetchone()
	team1 = data[0]
	team2 = data[1]
	tournament = data[2]
	score1=data[3]
	score2=data[4]
	global cursor
	global conn

	if request.args.get('score1') != None:
		score1= int(request.args.get('score1'))
	if request.args.get('score2') != None:
		score2 = int(request.args.get('score2'))
	if (request.args.get('home'))!= team1 or (request.args.get('away')) != team2:
			return redirect(url_for('start_game'))

	tournament = tournament.lower()

	if score2 > score1:
		winner = team2
		loser = team1 
		w_score = score2
		l_score = score1
	else:
		winner = team1
		loser = team2
		w_score = score1
		l_score = score2

	dt = datetime.now().replace(microsecond=0)

	#report score
	cursor.execute("INSERT INTO tournament ( winner , loser , w_score, l_score, tournament, dt ) VALUES ('{0}','{1}',{2},{3},'{4}','{5}');".format(winner, loser, w_score,l_score,tournament, dt))
	conn.commit()
	print(winner)
	cursor.execute("UPDATE Teams SET wins = wins + 1 WHERE team_name = '{0}';".format(winner))
	conn.commit()
	cursor.execute("UPDATE Teams SET losses = losses + 1 WHERE team_name = '{0}';".format(loser))
	conn.commit()
	score1 = 0
	score2 = 0
	team1 = ''
	team2 = ''

	return redirect(url_for("start_game"))


@app.route('/table')
def scores():
	global cursor
	global conn
	cursor.execute("SELECT winner , loser , w_score, l_score, tournament, dt from tournament LIMIT 20;")
	data = cursor.fetchall()
	d = list(data)
	d.sort(key=operator.itemgetter(5), reverse=True)
	return render_template("table.html", data=d,  name=flask_login.current_user.id)

@app.route('/search')
def search():
	global cursor
	term = request.args.get('search')
	cursor.execute("SELECT winner , loser , w_score, l_score, tournament, dt from tournament where '{0}' = winner OR '{0}' = loser or '{0}' = tournament".format(term))
	data = cursor.fetchall()
	d = list(data)
	d.sort(key=operator.itemgetter(5), reverse=True)
	return render_template("table.html", data=d,  name=flask_login.current_user.id)

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = ("SELECT email FROM Users WHERE email ='{0}'".format(email))
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	global cursor
	cursor.execute("SELECT email FROM Users")
	users = cursor.fetchall()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd 
	return user


@app.route('/login_user', methods=['GET', 'POST'])
def loginUser():
	if flask.request.method == 'GET':
		return render_template('login.html')
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0])
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect('/user/' + email)  #protected is a function defined in this file

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register_user'>or make an account</a>"

@app.route('/logout_user')
def logoutUser():
	if access_token is not None:
		return redirect(url_for('logout'))
	flask_login.logout_user()
	return redirect('/register_user')

@app.route("/register_user", methods=['GET'])
def register():
	return render_template('register.html', supress='True')  

@app.route("/register_user", methods=['POST'])
def register_user():
	try:
		email=request.form.get('email')
		password=request.form.get('password')
		firstName=request.form.get('firstName')
		lastName=request.form.get('lastName')
		team=request.form.get('team')
		print(firstName + lastName + email + team + password)
	except:
		print("couldn't find all tokens1") #this prints to shell, end users will not see this (all print statements go to shell)
		return redirect(url_for('register_user'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print cursor.execute("INSERT INTO Users (first_name, last_name, email, team, password) VALUES ('{0}', '{1}','{2}','{3}','{4}')".format(firstName, lastName, email, team, password))
		conn.commit()
		cursor.execute("INSERT INTO Teams(team_name,wins,losses) VALUES ('{0}',0,0)".format(team))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return redirect(url_for('login'))
	else:
		print("couldn't find all tokens")
		return redirect(url_for('register_user'))

def isEmailUnique(email):
	cursor.execute("SELECT email FROM Users")
	users = cursor.fetchall()
	if email in list(users):
		return False
	else:
		return True


@app.route("/start_game", methods=['GET'])
@flask_login.login_required
def start_game():
	email = flask_login.current_user.id
	cursor.execute("SELECT team FROM Users WHERE email = '{0}'".format(email))
	team = cursor.fetchone()
	print(team[0])
	cursor.execute("SELECT player_id, first_name, last_name FROM players WHERE team = '{0}'".format(team[0]))
	players = cursor.fetchall()
	return render_template('start_game.html', players=players,  name=flask_login.current_user.id)  

@app.route("/start_game", methods=['POST'])
@flask_login.login_required
def startGame():

	email = flask_login.current_user.id

	
	cursor.execute("SELECT team FROM Users WHERE email = '{0}'".format(email))
	team1 = cursor.fetchone()[0]
		#log user in
	team2 = request.form.get('team2')
	tournament = request.form.get('tournament')
	
	cursor.execute("INSERT INTO games (team1,team2,tournament) VALUES ('{0}','{1}','{2}')".format(team1, team2, tournament))
	conn.commit()

	cursor.execute("SELECT gameID FROM games WHERE team1 = '{0}' AND team2 ='{1}'AND tournament='{2}'".format(team1, team2, tournament))
	gameID = int(cursor.fetchone()[0])
	print(gameID)
	players = request.form.getlist('players')
	print(players)
	for p in players:
		name = p.split(' ')
		fname = name[0]
		lname = name[1]
		cursor.execute("UPDATE Players SET last_game = {0} WHERE first_name= '{1}' AND last_name ='{2}';".format( gameID, fname,lname))
		conn.commit()


	return redirect('/tweetboard/'+ str(gameID))

@app.route("/user", methods=['GET'])
@flask_login.login_required
def user():
	access_token = session.get('access_token')
	print(access_token)
	if access_token is None:
		return redirect(url_for('login'))

	access_token = access_token[0]
	email = flask_login.current_user.id
	cursor.execute("SELECT team FROM Users WHERE email = '{0}'".format(email))
	team = cursor.fetchone()
	cursor.execute("SELECT player_id, first_name, last_name, scores, assists FROM players WHERE team = '{0}'".format(team[0]))
	players = cursor.fetchall()

	return render_template("user.html", team=team[0], players=players, name=flask_login.current_user.id)

@app.route("/addPlayer", methods=['GET','POST'])
@flask_login.login_required
def newPlayer():
	email = flask_login.current_user.id
	first_name = request.args.get('first_name')
	last_name = request.args.get('last_name')
	print(first_name)
	cursor.execute("SELECT team FROM Users WHERE email = '{0}'".format(email))
	team = cursor.fetchone()
	cursor.execute("INSERT INTO Players (first_name, last_name, team) VALUES ('{0}', '{1}','{2}')".format(first_name, last_name, team[0]))
	conn.commit();
	return redirect(url_for('user'))


@app.route("/removePlayer", methods=['GET','POST'])
@flask_login.login_required
def deletePlayer():
	name = request.args.get('name').split(" ") #get first and last name
	first_name = name[0]
	second_name = name[1]
	email = flask_login.current_user.id
	cursor.execute("SELECT team FROM Users WHERE email = '{0}'".format(email))
	team = cursor.fetchone()
	cursor.execute("DELETE FROM Users WHERE first_name = '{0}' AND last_name ='{1}' AND team ='{2}'".format(first_name,last_name,team))
	conn.commit()
	return redirect(url_for('user'))

@app.route('/player_stats')
def players():
	global cursor
	global conn
	cursor.execute("SELECT first_name, last_name, scores, assists, scores+assists from Players LIMIT 20;")
	data = cursor.fetchall()
	d = list(data)
	d.sort(key=operator.itemgetter(4), reverse=True)
	return render_template("player_stats.html", data=d,  name=flask_login.current_user.id)


@app.route('/team_stats')
def teams():
	global cursor
	global conn
	cursor.execute("SELECT team_name, wins, losses, wins/(wins+losses) from Teams LIMIT 20;")
	data = cursor.fetchall()
	d = list(data)
	d.sort(key=operator.itemgetter(3), reverse=True)
	return render_template("team_stats.html", data=d,  name=flask_login.current_user.id)

