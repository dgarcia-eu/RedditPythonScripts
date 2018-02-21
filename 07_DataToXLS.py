from pprint import pprint
import json
import sys
import os
import subprocess
import shlex
import xlwt

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

subredditDict = dict()
book = xlwt.Workbook(encoding="utf-8")
postsSheet = book.add_sheet("Posts")

i = 0
for f in fieldnames:
	postsSheet.write(0, i, f)
	i = i+1

pos = 1
for filename in filenames:
#	print filename
	if filename.endswith('.json'):
		with open('RedditCrawl/'+filename) as data_file:    
			data = json.load(data_file)
			
			i = 0
			for field in fields :
				if field == 'created_utc' or field == 'score' or field == 'num_comments':
					content = str(int(data[0]["data"]["children"][0]["data"][field]))
				elif field == 'upvote_ratio' :
					content =  str(data[0]["data"]["children"][0]["data"][field])
				else:
					content = data[0]["data"]["children"][0]["data"][field].encode("utf8")
				cleancontent = content.replace("\n", " ").replace('"', "'")
				
				postsSheet.write(pos, i, cleancontent)	
				i = i+1
				if field ==  'title' or field == 'selftext':
					sentiment = rateSentiment(cleancontent, p)
					parts = sentiment.split("\t")
					postsSheet.write(pos, i, parts[0])
					i = i+1
					postsSheet.write(pos, i, parts[1])
					i = i+1
				if field == "id":
					id = data[0]["data"]["children"][0]["data"][field].encode("utf8")
				if field == "subreddit_id":
					subredditid = data[0]["data"]["children"][0]["data"][field].encode("utf8")
				if field == "subreddit":
					subreddit = data[0]["data"]["children"][0]["data"][field].encode("utf8")

			subredditDict[id] = subredditid, subreddit
			pos = pos +1


commentsSheet = book.add_sheet("Comments")
fields =      'id','link_id','parent_id','author','score','created_utc','body'
fieldnames =  'id','link_id','parent_id','author','score','created_utc','body','body_P','body_N', 'subreddit','subreddit_id'

i = 0
for f in fieldnames:
	commentsSheet.write(0, i, f)
	i = i+1



def traverse(data, pid, pos):
	thisid = data['parent_id']
	row = dict()
	for field in fields :
		if field == 'created_utc' or field == 'score':
			content = str(int(data.get(field,0)))
			row[field] = content
		elif field == 'link_id' and data.get(field,-1) == -1:
			row[field] = linkid
		elif field == 'parent_id' and data.get(field,-1) == -1:
			row[field] = pid
		else:
			content = data.get(field, "").encode("utf8")
			cleancontent = content.replace("\n", " ").replace('"', "'")
			row[field] = cleancontent
			if field ==  'body' or field == 'selftext':
				sentiment = rateSentiment(cleancontent, p)
				parts = sentiment.split("\t")
				row[field+"_P"] = parts[0]
				row[field+"_N"] = parts[1]
	subreddit, subredditid = subredditDict[row["link_id"].replace("t3_","")]
	row['subreddit'] = subreddit
	row['subreddit_id'] = subredditid
	i = 0
	for f in fieldnames:
		commentsSheet.write(pos, i, row[f])
		i = i+1

	pos = pos+1

	reps = data.get('replies',-1)
	if reps != -1 and len(data["replies"]) > 0:
		for c in data["replies"]["data"]["children"]:
			pos = traverse(c["data"],thisid,pos)
	return(pos)

filenames = os.listdir('RedditCrawl')

pos = 1

for filename in filenames:
	if filename.endswith('.json'):
#			print filename
		with open('RedditCrawl/'+filename) as data_file:    
			data = json.load(data_file)
			linkid = data[0]["data"]["children"][0]["data"]["id"].encode("utf8")
			for d in data[1:]:
				for c in d["data"]["children"]:
					pos = traverse(c["data"],linkid,pos)

book.save("RedditAna.xls")
