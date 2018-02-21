import time
import praw 

reddit = praw.Reddit(client_id='id',
                     client_secret='secret',
                     user_agent='agent')

fin = open("users.txt", "rt")
for l in fin:
	user = reddit.redditor(l.strip())
	time.sleep(15)
	print user.name + "\t" + str(user.link_karma) + "\t" + str(user.comment_karma)
fin.close()
