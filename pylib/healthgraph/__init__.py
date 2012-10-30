import sqlite3
import urllib
import logging
import json
import urllib2
		
#database connection
dbconn = sqlite3.connect('auth.db')

cur = dbconn.cursor()    
cur.execute("CREATE TABLE IF NOT EXISTS tokens(access_token string)")

class User:
	def auth_url(self):
		from _config import auth_url, client_id
		url = auth_url + '?' + urllib.urlencode({
			'client_id': client_id,
			'response_type': 'code',
			'redirect_uri': 'http://br3nda.com'})
		
		return url
		
		
	def save_access_token(self, token):
		logging.info("Saving code: %s"%(token))
		cur.execute('INSERT INTO tokens (access_token) VALUES(?)', (token,))
		
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
		data = urllib.urlencode(values)
		headers = {'content-type': ' application/x-www-form-urlencoded'}
		req = urllib2.Request(access_token_url, data, headers)
		response = urllib2.urlopen(req)

		#read runkeeper's response
		self._auth_response = response.read()
		#parse from json
		self._auth_data = json.loads(self._auth_response)
		#get the token
		self.access_token = self._auth_data['access_token']
		#save into our db
		self.save_access_token(self.access_token)
		
		
