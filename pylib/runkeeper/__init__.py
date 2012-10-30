import sqlite3
import urllib
import logging

#database connection
dbconn = sqlite3.connect('auth.db')

cur = dbconn.cursor()    
#cur.execute("CREATE TABLE auth(code string)")

class User:
	def auth_url(self):
		from _config import auth_url, client_id
		url = auth_url + '?' + urllib.urlencode({
			'client_id': client_id,
			'response_type': 'code',
			'redirect_uri': 'http://br3nda.com'})
		
			
		print "Go to this url: \n"+url
		
	
		
	def save_auth_code(self, code):
		logging.info("Saving code: %s"%(code))
		cur.execute('INSERT INTO auth(code) VALUES(?)', (code,))
		
	def auth(self,code):
	#Make a POST request to the Health Graph API token endpoint.
	# nclude the following parameters in application/x-www-form-urlencoded format:

    #grant_type: The keyword 'authorization_code'
    #code: The authorization code returned in step 2
    #client_id: The unique identifier that your application received upon registration
    #client_secret: The secret that your application received upon registration
    #redirect_uri: The exact URL that you supplied when sending the user to the authorization endpoint above

		from _config import access_token_url, client_id, client_secret	
		import urllib
		import urllib2
		print access_token_url
		
		values = {'code' : code,
				  'grant_type': 'authorization_code',
				  'client_id' : client_id,
				  'client_secret' : client_secret,
				  'redirect_url': 'http://br3nda.com' }
		print values
		data = urllib.urlencode(values)
		headers = {'content-type': ' application/x-www-form-urlencoded'}
		req = urllib2.Request(access_token_url, data, headers)
		response = urllib2.urlopen(req)
		the_page = response.read()
		print the_page
