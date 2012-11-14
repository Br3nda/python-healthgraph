import sqlite3
import urllib
import logging
import json
import urllib2

logger = logging.getLogger('healthgraph')
		
#database connection
dbconn = sqlite3.connect('healthgraphauth.db')

cur = dbconn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tokens(access_token string)")
dbconn.commit()


def auth_url():
	from _config import auth_url, client_id
	url = auth_url + '?' + urllib.urlencode({
		'client_id': client_id,
		'response_type': 'code',
		'redirect_uri': 'http://br3nda.com'})
	return url
	
class User:
	def __init__(self):
		self._token = None
		self.user_data = None
		
	def save_access_token(self, token):
		print "Saving code: %s"%(token)
		cur.execute('INSERT INTO tokens (access_token) VALUES(?)', (token, ))
		dbconn.commit()
		
		
		
	def auth(self,code):
		#Make a POST request to the Health Graph API token endpoint.
		# nclude the following parameters in application/x-www-form-urlencoded format:

		#grant_type: The keyword 'authorization_code'
		#code: The authorization code returned in step 2
		#client_id: The unique identifier that your application received upon registration
		#client_secret: The secret that your application received upon registration
		#redirect_uri: The exact URL that you supplied when sending the user to the authorization endpoint above

		from _config import access_token_url, client_id, client_secret			
		values = {'code' : code,
				  'grant_type': 'authorization_code',
				  'client_id' : client_id,
				  'client_secret' : client_secret,
				  'redirect_uri': 'http://br3nda.com' }
		logger.info("Auth request = %s"%(values))
		data = urllib.urlencode(values)
		headers = {'content-type': ' application/x-www-form-urlencoded'}
		req = urllib2.Request(access_token_url, data, headers)
		response = urllib2.urlopen(req)

		#read runkeeper's response
		self._auth_response = response.read()
		#parse from json
		self._auth_data = json.loads(self._auth_response)
		#get the token
		self._token = self._auth_data['access_token']
		#save into our db
		self.save_access_token(self._token)
	
	@property
	def token(self):
		if not self._token:
			cur = dbconn.cursor()    
			cur.execute("SELECT * FROM tokens")

			rows = cur.fetchall()

			self._token = rows[0][0]
			
		assert self._token
		return self._token
			
	_url = 'https://api.runkeeper.com'

		
	def request(self, datatype, path='', ):
		headers = {
			'Authorization': 'Bearer %s'%(self.token),
			'Accept': datatype,
			}
		print "\tRequest = %s"%(headers)
		
		url = self._url + path
		print "\tURL = %s"%(url)
		req = urllib2.Request(url, headers=headers)
		response = urllib2.urlopen(req)

		#parse from json
		return json.loads(response.read())

	def user_details(self):
		#if we already have this, don't refetch
		if self.user_data:
			return self.user_data
			
		self.user_data = self.request(datatype='application/vnd.com.runkeeper.User+json', path='/user')
		return self.user_data
		
	def profile(self):
		pass
	def nutrition(self):
		pass
		
	def weight(self):
		path = self.user_details()['weight']
		return self.request(path)
		
	def fitness_activities(self):
		path = self.user_details()['fitness_activities']
		datatype='application/vnd.com.runkeeper.FitnessActivityFeed+json'
		return self.request(path=path, datatype=datatype)
		

class Activity:
	pass
