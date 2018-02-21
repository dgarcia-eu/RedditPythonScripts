from pprint import pprint
import json
import sys
import os
import csv
import subprocess
import shlex

def rateSentiment(sentiString, p):
	p.stdin.write(sentiString.replace(" ", "+").replace("\t", "+").replace("\n", "+").replace("\r", "+")+"\n")
	stdout_text = p.stdout.readline()
	stdout_text = stdout_text.rstrip()
#	print sentiString.replace(" ", " ").replace("\t", " ").replace("\n", " ") + "\t" + stdout_text
	return stdout_text

p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata  SentStrength_Data/",posix=False),
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

fields =      'id','link_id','parent_id','author','score','created_utc','body'
fieldnames =  'id','link_id','parent_id','author','score','created_utc','body','body_P','body_N'



def traverse(data, pid):
#	print data["name"] + "\t" + data['parent_id']
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
	writer.writerow(row)

	reps = data.get('replies',-1)
	if reps != -1 and len(data["replies"]) > 0:
		for c in data["replies"]["data"]["children"]:
			traverse(c["data"],thisid)



filenames = os.listdir('RedditCrawl')

with open('Comments.csv', 'wb') as csvfile:
	writer = csv.DictWriter(csvfile, delimiter='\t',quotechar='"', quoting=csv.QUOTE_MINIMAL,fieldnames=fieldnames)
	writer.writeheader()

	for filename in filenames:
		if filename.endswith('.json'):
#			print filename
			with open('RedditCrawl/'+filename) as data_file:    
				data = json.load(data_file)
				linkid = data[0]["data"]["children"][0]["data"]["id"].encode("utf8")
				for d in data[1:]:
					for c in d["data"]["children"]:
						traverse(c["data"],linkid)



