

class TwitterService:
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
        consumer_key='KhXbcsK44j0Q2hKtN2aRUIoHB',
        consumer_secret='DzTGByioKTU0WADPW3Juc79tZFccp4TsI4mv44rbqYfVCBFwYp'
    )
    
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

    def post_tweet(self, status):

        resp = twitter.post('https://api.twitter.com/1.1/statuses/update.json', data={
                'status': status 
        })

        if resp.status == 403:
            raise Exception('Too Long')
        elif resp.status == 401:
            raise Exception('Authoriztion Error')
    @twitter.tokengetter
    def get_twitter_token(token=None):
        return session.get('twitter_token')
        