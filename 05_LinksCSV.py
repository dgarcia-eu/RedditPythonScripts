from pprint import pprint
import json
import sys
import os
import csv
import subprocess
import shlex


def rateSentiment(sentiString, p):
	p.stdin.write(sentiString.replace(" ", "+").replace("\t", "+").replace("\n", "+")+"\n")
	stdout_text = p.stdout.readline()
	stdout_text = stdout_text.rstrip()
	return stdout_text



p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata  SentStrength_Data/",posix=False),
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)    

filenames = os.listdir('RedditCrawl')

fields =  'id','subreddit_id','subreddit','author','url','upvote_ratio','score','created_utc','num_comments','title','selftext'
fieldnames =  'id','subreddit_id','subreddit','author','url','upvote_ratio','score','created_utc','num_comments','title','title_P','title_N','selftext','selftext_P','selftext_N'

with open('Posts.csv', 'wb') as csvfile:
	writer = csv.DictWriter(csvfile, delimiter='\t',quotechar='"', quoting=csv.QUOTE_MINIMAL,fieldnames=fieldnames)
	writer.writeheader()

	for filename in filenames:
	#	print filename
		if filename.endswith('.json'):
			with open('RedditCrawl/'+filename) as data_file:    
				data = json.load(data_file)
				row = dict()
				for field in fields :
					if field == 'created_utc' or field == 'score' or field == 'num_comments':
						content = str(int(data[0]["data"]["children"][0]["data"][field]))
					elif field == 'upvote_ratio' :
						content =  str(data[0]["data"]["children"][0]["data"][field])
					else:
						content = data[0]["data"]["children"][0]["data"][field].encode("utf8")
					cleancontent = content.replace("\n", " ").replace('"', "'")
					row[field] = cleancontent

					if field ==  'title' or field == 'selftext':
						sentiment = rateSentiment(cleancontent, p)
						parts = sentiment.split("\t")
						row[field+"_P"] = parts[0]
						row[field+"_N"] = parts[1]
				writer.writerow(row)

#pprint(data)
