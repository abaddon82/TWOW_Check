#! /usr/bin/python

import twitter, re, urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS

def twitter_check():
	ck = 'ENTER CONSUMER KEY HERE'
	cs = 'ENTER CONSUMER SECRET HERE'

	at = 'ENTER ACCESS TOKEN HERE'
	ats = 'ENTER ACCESS TOKEN SECRET HERE'

	checkregex = '(^ye[sp])|finally|done'

	api = twitter.Api(consumer_key=ck, consumer_secret=cs, access_token_key=at, access_token_secret=ats)

	twow_status = api.GetUserTimeline(screen_name='IsTWoWOutYet', count=1, include_rts=False, exclude_replies=True)

	statustext = twow_status[0].text

	regex = re.compile(checkregex, re.IGNORECASE)

	result = regex.search(statustext)

	if (result == None):
		return 0
	else:
		return 0.50

def livejournal_check():
	url = 'http://grrm.livejournal.com/data/rss'
	checkregex = r"(?:(winds of winter|son of kong)(?: is (done|released|finished))?)|(^(?:I'm|It's) (?:done|finished)\.$)|(winter has come)"
	regex = re.compile(checkregex, re.IGNORECASE|re.MULTILINE)
	postvalue = 0
	valuedict = {   0.2: (('winds of winter', 'done', '', ''),('winds of winter', 'finished','','')),
                	0.5: (('son of kong', 'done', '', ''), ('son of kong','finished','','')),
	                0.1: (('winds of winter', '', '', ''),),
        	        0.3: (('son of kong', '', '', ''),),
                	0.3: (('winds of winter', 'released', '', ''), ('son of kong', 'released', '', '')),
	                0.4: (('', '', 'I\'m finished.', ''), ('', '', 'It\'s done.', ''), ('', '', 'It\'s finished.', ''), ('', '', 'I\'m done.', '')),
        	        0.5: (('', '', '', 'winter has come'),)
	}


	response = urllib2.urlopen(url)
	xml = ET.fromstring(response.read())
	
	george_feed = xml[0]

	item = george_feed.find('item')
	title = item.find('title').text
	soup = BS(item.find('description').text, 'html.parser')
	blogtext = soup.get_text()
	textmatches = regex.findall(blogtext)

	if (textmatches == None):
		postvalue = 0
	else:
		for match in textmatches:
			for v in valuedict:
				if match in valuedict[v]:
					postvalue = postvalue + v
	titlematch = regex.match(title)
	
	if (titlematch != None):
		postvalue = postvalue * 2
	
	return postvalue

print twitter_check() + livejournal_check()
