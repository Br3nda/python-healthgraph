from healthgraph import User

#set up logging
#import logging
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)

#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)

#logger = logging.getLogger()
#logger.addHandler(ch)
#logger.info('adfds')

user = User()

#print user.user_details()

#print user.user_details()['userID']
for a in user.fitness_activities()['items']:
	print "{ttype}".format(
		ttype=a['type']
	)
	
print user.weight()

