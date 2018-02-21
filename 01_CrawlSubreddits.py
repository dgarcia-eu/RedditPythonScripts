import praw
from pprint import pprint
import time

reddit = praw.Reddit(client_id='id',
                     client_secret='secret',
                     user_agent='agent')

fin = open('SubredditList.txt', "rt")

for l in fin:

	subreddit = reddit.subreddit(l.strip())
	for submission in subreddit.hot(limit=10000):
		print vars(submission)['permalink'].encode('utf-8')
	time.sleep(30)

fin.close()