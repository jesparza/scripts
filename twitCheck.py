#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to control friends and followers on Twitter. The inactivity of friends with protected tweets cannot be retrieved if not authenticated with the proper account.
# Updated to support Twitter API 1.1.
# 
# Required: https://github.com/tweepy/tweepy
#
# http://eternal-todo.com
# Jose Miguel Esparza
#

import sys, tweepy, shelve, datetime, itertools, traceback

def paginate(iterable, pageSize):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, pageSize, None),
            list(itertools.islice(i2, pageSize)))
        if len(page) == 0:
            break
        yield page

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

if len(sys.argv) != 2:
   sys.exit('Usage: '+sys.argv[0]+' twitter_user')

followers = {}
friendsIds = []
lostFollowers = {}
newFollowers = {}
followerIds = []
inactiveFriends = []
outputFactor = 1 #;)
followersFile = 'followers_control.twt'
user = sys.argv[1]
inactivityTime = 45 #days
today = datetime.datetime.now()


# Authentication
if CONSUMER_KEY == '' or CONSUMER_SECRET == '' or ACCESS_TOKEN == '' or ACCESS_TOKEN_SECRET == '':
	sys.exit('Warning: You should write your own Twitter application credentials within the code. Take a look here to obtain these credentials: http://www.webdevdoor.com/php/authenticating-twitter-feed-timeline-oauth/.')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Getting user info
try:
   userInfo = api.get_user(user)
except tweepy.error.TweepError, e:
   traceback.print_exc()
   if e.reason == 'Not found':
      sys.exit('Error: User not found!!')
   elif e.reason.find('Rate limit exceeded'):
      sys.exit('Error: Rate limit exceeded!!')
   else:
      sys.exit('Error: '+str(e.reason))
   
userName = userInfo.name
userLanguage = userInfo.lang
userLocation = userInfo.location
if userLocation == None:
   userLocation = '-'
userTimeZone = userInfo.time_zone
if userTimeZone == None:
   userTimeZone = '-'
if userInfo.protected:
   userActivity = '-'
else:
   try:
      userActivity = str(userInfo.status.created_at)
   except:
      try:
         timeLine = userInfo.timeline()
      except tweepy.error.TweepError, e:
         print str(sys.exc_info())
         sys.exit('Error: '+str(e.reason))
      if timeLine != []:
         userActivity = str(timeLine[0].created_at)
      else:
         userActivity = '-'
userCreation = str(userInfo.created_at)
if userCreation == None:
   userCreation = '-'
if userInfo.protected:
   print 'Warning: protected account. It\'s not possible to retrieve friends nor followers.'

try:
   ## New and lost followers
   # Getting follower ids
   followersCursor = tweepy.Cursor(api.followers_ids,id=user)
   for id in followersCursor.items():
      followerIds.append(id)

   # Comparing followers with old followers
   oldFollowers = shelve.open(followersFile)
   if oldFollowers.has_key(user):
      oldFollowersByUser = oldFollowers[user]
      followers = dict(oldFollowersByUser)
      for followerId in oldFollowersByUser:
         if followerId not in followerIds:
            lostFollowers[followerId] = oldFollowersByUser[followerId]
            followers.pop(followerId)
      for followerId in followerIds:
         if followerId not in oldFollowersByUser:
            newFollowers[followerId] = []
   else:
      print 'Warning: No data to compare followers with\n'
      
   # Getting new followers info
   newFollowersIds = newFollowers.keys()
   for newFollowersPage in paginate(newFollowersIds, 100):
	   newFollowersObjects = api.lookup_users(user_ids=newFollowersPage)
	   for newFollower in newFollowersObjects:
		   newFollowers[newFollower.id] = [newFollower.name, newFollower.screen_name]

   followers.update(newFollowers)
   oldFollowers[user] = followers
   oldFollowers.close()
   
   ## Getting friends and their activity
   # Getting friends ids
   friendsCursor = tweepy.Cursor(api.friends_ids,id=user)
   for id in friendsCursor.items():
      friendsIds.append(id)
      
   # Getting friends info
   for friendsPage in paginate(friendsIds, 100):
	   friendsObjects = api.lookup_users(user_ids=friendsPage)
	   for friend in friendsObjects:
			inactivity = None
			inactivityDate = None
			if not friend.protected:
				try:
					inactivity = today - friend.status.created_at
					inactivityDate = str(friend.status.created_at)
				except:
					timeLine = friend.timeline()
					if timeLine != []:
						inactivity =  today - timeLine[0].created_at
						inactivityDate =  str(timeLine[0].created_at)
					else:
						inactivity =  today - friend.created_at
						inactivityDate = str(friend.created_at)
				if inactivity != None and inactivity.days > inactivityTime:
					inactiveFriends.append([friend.name,friend.screen_name,inactivityDate])
   if inactiveFriends != []:
      outputFactor = 2
      
except tweepy.error.TweepError, e:
   #print str(sys.exc_info())
   if e.reason.find('Rate limit exceeded') != -1:
      sys.exit('Error: Rate limit exceeded!!')
   else:
      sys.exit('Error: '+str(e.reason))
   
## Printing data
# User
print '##########################################'*outputFactor
print 'User: '+user
print 'Name: '+userName
print 'Location: '+userLocation
print 'Language: '+userLanguage
print 'Time Zone: '+userTimeZone
print 'Creation: '+userCreation
print 'Last tweet: '+userActivity
print '##########################################'*outputFactor
print

# Friends
print '##########################################'*outputFactor
print 'Friends: '+str(len(friendsIds))
if inactiveFriends == []:
   print 'Inactive Friends: 0'
else:
   print 'Inactive Friends ('+str(len(inactiveFriends))+'):'
   inactiveFriends = sorted(inactiveFriends, key = lambda x:x[2])
   for inactive in inactiveFriends:
      print '\t['+inactive[2]+'] '+inactive[0]+' ('+inactive[1]+')'
print '##########################################'*outputFactor
print

# Followers
print '##########################################'*outputFactor
print 'Followers: '+str(len(followers))
if newFollowers == []:
   print 'New Followers: 0'
else:
   print 'New Followers ('+str(len(newFollowers))+'):'
   for newFollowerId in newFollowers:
      newFollowerName, newFollowerScreenName = newFollowers[newFollowerId]
      print '\t'+newFollowerName+' ('+newFollowerScreenName+')'
if lostFollowers == []:
   print 'Lost Followers: 0'
else:
   print 'Lost Followers ('+str(len(lostFollowers))+'):'
   for lostFollowerId in lostFollowers:
      lostFollowerName, lostFollowerScreenName = lostFollowers[lostFollowerId]
      print '\t'+lostFollowerName+' ('+lostFollowerScreenName+')'
print '##########################################'*outputFactor
print
