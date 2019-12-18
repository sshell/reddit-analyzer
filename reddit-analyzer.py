import sys
import requests
from ascii_graph import Pyasciigraph
from datetime import datetime
from collections import Counter
import time

if len(sys.argv) == 2:
	username = str(sys.argv[1])
else:
	print('-----')
	print('usage: reddit-analyzer.py USERNAME')
	print('-----')
	sys.exit()
	
# initialize variables
# username = 'spez'
lastaction = 0
headers = {'User-Agent': 'testbot'}
curts = int(time.time())
commentdata = []
linkdata = []
timelist = []
hourseconds = 3600
houroffset = -7
offset = hourseconds*houroffset

# let people know that it's working
print(' --- fetching data for user: '+username+' ---')
print(' ')

# fetch profile data
r3 = requests.get('https://www.reddit.com/user/'+username+'/about.json', headers=headers)
userdata = r3.json()['data']
    
# fetch comments
while True:
    comurl = 'https://api.pushshift.io/reddit/search/comment/?author='+username+'&size=500&before='+str(curts)
    r1 = requests.get(comurl, headers=headers)
    tempdata = r1.json()['data']
    commentdata += tempdata
    try:
        if tempdata[499]:
            curts = tempdata[499]['created_utc']
    except: break

# re-establish current time
curts = int(time.time())

# fetch posts/submissions
while True:
    linkurl = 'https://api.pushshift.io/reddit/search/submission/?author='+username+'&size=500&before='+str(curts)
    r2 = requests.get(linkurl, headers=headers)
    postdata = r2.json()['data']
    linkdata += postdata
    try:
        if postdata[499]:
            curts = postdata[499]['created_utc']
    except: break


# set last active time
lastcomment = commentdata[0]['created_utc']
lastpost = postdata[0]['created_utc']

if lastcomment > lastpost:
    lastaction = lastcomment
else: lastaction = lastpost


# add all subreddits to a list
# add all timed activities to a list
subList = []
for x in commentdata:
    subList.append(x['subreddit'].lower())
    timelist.append(x['created_utc'])

for x in postdata:
    subList.append(x['subreddit'].lower())
    timelist.append(x['created_utc'])

# adjust time for offset
timelist = [x + offset for x in timelist]

# and create a set for comparison purposes
sublistset = set(subList)

# load subreddits from file and check them against comments
locList = [line.rstrip('\n').lower() for line in open('all-locations.txt')]
loclistset = set(locList)


def getProfile():
    print('[+] username        : '+str(userdata['name']))
    print('[+] creation date   : '+str(datetime.fromtimestamp(userdata['created_utc'])))
    print('[+] last action     : '+str(datetime.fromtimestamp(lastaction)))
    print('[+] verified email  : '+str(userdata['has_verified_email']))
    print('---')
    print('[+] total comments  : '+str(len(commentdata)))
    print('[+] comment karma   : '+str(userdata['comment_karma']))
    print('---')
    print('[+] total links     : '+str(len(linkdata)))
    print('[+] link karma      : '+str(userdata['link_karma']))
    print('---')
    print('[+] location based reddit(s): '+ str(sublistset.intersection(loclistset)))


def getComments():

    # draw and print ascii graph
    counter = Counter(subList)
    gdata = counter.most_common()
    
    graph = Pyasciigraph(
        separator_length=4,
        multivalue=False,
        human_readable='si',
    )
    for line in graph.graph('Comment Activity', gdata):
        print(line)

def timeGraph(timelist):
    newtl = []  # hour list
    wdlist = [] # weekday list

    # fill newtl with HOURs 
    for x in timelist:
        newtl.append(datetime.fromtimestamp(int(x)).hour)

    # create hour name list
    hournames = '00:00 01:00 02:00 03:00 04:00 05:00 06:00 07:00 08:00 09:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00 17:00 18:00 19:00 20:00 21:00 22:00 23:00'.split()
    
    # deal with HOUR counting
    tgCounter = Counter(newtl)
    tgdata = tgCounter.most_common()
    # sort by HOUR not popularity
    tgdata = sorted(tgdata)

    d = []
    e = 0
    for g in hournames:
        d.append(tuple([g, tgdata[e][1]]))
        e+=1
    tgdata = d

    # draw HOUR graph
    graph = Pyasciigraph(
        separator_length=4,
        multivalue=False,
        human_readable='si',
    )
    for line in graph.graph('Time Activity', tgdata):
        print(line)    


    print(' ')

    # estabish weekday list (0 is Monday in Python-land)
    weekdays = 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split()
    for x in timelist:
        wdlist.append(datetime.fromtimestamp(int(x)).weekday())
        
    wdCounter = Counter(wdlist)
    wddata = wdCounter.most_common()
    wddata = sorted(wddata)

    # change tuple weekday numbers to weekday names
    y = []
    c = 0
    for z in weekdays:
      y.append(tuple([z, wddata[c][1]]))
      c+=1
    wddata = y
    
    # draw WEEKDAY graph
    graph = Pyasciigraph(
        separator_length=4,
        multivalue=False,
        human_readable='si',
    )
    for line in graph.graph('Day of the Week Activity', wddata):
        print(line)
        
### PRINT INFO ###

getProfile()
print(' ')
getComments()
print(' ')
timeGraph(timelist)