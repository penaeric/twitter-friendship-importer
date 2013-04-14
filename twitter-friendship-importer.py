#!/usr/bin/env python

import os
import sys
import sqlite3

import tweepy


class TwitterFrienshipImporter:
	"""" TwitterFrienshipImporter imports the users you're following in one account to another
	
	Twitter will potentially block your secondary account. This might be fine for many users as you probably want to run this script once.  This script might be also useful if you want to 'sync' the users you're following (running the script once in a while) although I don't know if Twitter counts this as aggressive following behavior. 
	For more information on Twitter following rules and best practices, visit:
		https://support.twitter.com/groups/32-something-s-not-working/topics/116-account-settings-problems/articles/15790-how-to-contest-account-suspension
		https://support.twitter.com/articles/68916
	
	Todo:
		- Documentation with instructions
		- If tokens are in the database, ask the user if she wants to use them (right now, if the user screws up, she will have to delete de database and start again)
		- Check if tokens work before continuing. If they don't work, give user option to try again
		- Improve error handling
		- Decide what to do with the friends that can't be added
		- Give better error descriptions
		- Use callbacks and Python's webbrowser library to minimize user input
		- Check if already following user before trying to follow
		- Refactor getToTokens and getFromTokens to share common code
	"""
	def __init__(self):
		self.INSTRUCTIONS = False
		self.DEBUG = True
		self.DEBUG_DELETE_DB = True
		
		showInstructions = raw_input("Do you want to get instructions as you go along? (y/n): ").strip()
		if showInstructions == 'y':
			self.INSTRUCTIONS = True
			
		self.initDatabase()
		self.getFromTokens()
		self.getToTokens()
		self.getFriendships()
		self.followUsers()
		
		self.end()
			
	
	def initDatabase(self):
		"""" Initialize the Database """
		self.dbName = 'twitter.db'
		if not os.path.exists(self.dbName):
			# create DB
			self.con = sqlite3.connect(self.dbName)
			self.con.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, userId INTEGER UNIQUE)")
			self.con.execute("CREATE TABLE tokens (id INTEGER PRIMARY KEY, tokenKey VARCHAR(20) UNIQUE, tokenValue TEXT)")
			self.con.commit()
		else:
			# use the existing DB
			self.con = sqlite3.connect(self.dbName)
	
	
	def getFromTokens(self):
		"""" Get the tokens for the FROM Account """
		# TODO Check if tokens are already stored in the DB, ask the user if she wants to use them
		if self.INSTRUCTIONS:
			print "Go to https://dev.twitter.com/apps/ and login with the Twitter account you want to copy your friends <<from>> and create a new application.  Leave the Callback URL blank.  You will need the <Consumer key> and the <Consumer secret>"
		else:
			print "Tokens for the Twitter account you want to copy your friends <<from>>"
		
		FROM_CONSUMER_KEY = raw_input('Consumer key: ').strip()
		FROM_CONSUMER_SECRET = raw_input('Consumer secret: ').strip()
		auth = tweepy.OAuthHandler(FROM_CONSUMER_KEY, FROM_CONSUMER_SECRET)
		
		if self.INSTRUCTIONS:
			print 'Go to the following URL and authorize this application, take note of the PIN given to you.'
		auth_url = auth.get_authorization_url()
		print 'Please authorize: ' + auth_url
		verifier = raw_input('PIN: ').strip()
		auth.get_access_token(verifier)
		FROM_ACCESS_KEY = auth.access_token.key
		FROM_ACCESS_SECRET = auth.access_token.secret
		
		auth = tweepy.OAuthHandler(FROM_CONSUMER_KEY, FROM_CONSUMER_SECRET)
		auth.set_access_token(FROM_ACCESS_KEY, FROM_ACCESS_SECRET)

		self.apiFrom = tweepy.API(auth)
		
		# TODO check the tokens (self.apiFrom.test())
		# if tokens don't work, ask user if he wants to try again (will need to know what to do with the stored values)
			
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('FROM_CONSUMER_KEY', '" + str(FROM_CONSUMER_KEY) + "')")
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('FROM_CONSUMER_SECRET', '" + str(FROM_CONSUMER_SECRET) + "')")
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('FROM_ACCESS_KEY', '" + str(FROM_ACCESS_KEY) + "')")
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('FROM_ACCESS_SECRET', '" + str(FROM_ACCESS_SECRET) + "')")
		self.con.commit()
		
		if self.DEBUG:
			print 'Saved <From> Tokens:'
			cur = self.con.cursor()
			cur.execute("SELECT tokenKey, tokenValue FROM tokens WHERE tokenKey LIKE 'FROM%'")
			for row in cur.fetchall():
				print row[0] + ': ' + row[1]
			print '--\n'
	
			
	def getToTokens(self):
		"""" Get the tokens for the TO Account """
		# TODO Check if tokens are already stored in the DB, ask the user if she wants to use them
		if self.INSTRUCTIONS:
			print "Go to https://dev.twitter.com/apps/ and login with the Twitter account you want to copy your friends <<to>> and create a new application.  Leave the Callback URL blank.  You will need the <Consumer key> and the <Consumer secret>\nMake sure to go to Settings and set the Access to Read and Write."
		else:
			print "Tokens for the Twitter account you want to copy your friends to"
			
		TO_CONSUMER_KEY = raw_input('Consumer key: ').strip()
		TO_CONSUMER_SECRET = raw_input('Consumer secret: ').strip()
		auth = tweepy.OAuthHandler(TO_CONSUMER_KEY, TO_CONSUMER_SECRET)
		
		if self.INSTRUCTIONS:
			print 'Go to the following URL and authorize this application, take note of the PIN given to you.'
		auth_url = auth.get_authorization_url()
		print 'Please authorize: ' + auth_url
		verifier = raw_input('PIN: ').strip()
		auth.get_access_token(verifier)
		TO_ACCESS_KEY = auth.access_token.key
		TO_ACCESS_SECRET = auth.access_token.secret
		
		auth = tweepy.OAuthHandler(TO_CONSUMER_KEY, TO_CONSUMER_SECRET)
		auth.set_access_token(TO_ACCESS_KEY, TO_ACCESS_SECRET)

		self.apiTo = tweepy.API(auth)
		
		# TODO check the tokens (self.apiFrom.test())
		# if tokens don't work, ask user if he wants to try again (will need to know what to do with the stored values)
			
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('TO_CONSUMER_KEY', '" + str(TO_CONSUMER_KEY) + "')")
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('TO_CONSUMER_SECRET', '" + str(TO_CONSUMER_SECRET) + "')")
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('TO_ACCESS_KEY', '" + str(TO_ACCESS_KEY) + "')")
		self.con.execute("INSERT INTO tokens (tokenKey, tokenValue) VALUES ('TO_ACCESS_SECRET', '" + str(TO_ACCESS_SECRET) + "')")
		self.con.commit()
		
		if self.DEBUG:
			print 'Saved <To> Tokens:'
			cur = self.con.cursor()
			cur.execute("SELECT tokenKey, tokenValue FROM tokens WHERE tokenKey LIKE 'TO%'")
			for row in cur.fetchall():
				print row[0] + ': ' + row[1]
			print '--\n'
		

	def getFriendships(self):
		"""" Get the friendships from the main account """
		count = 0
		for friendId in tweepy.Cursor(self.apiFrom.friends_ids).items():
			if self.DEBUG:
				print str(count + 1) + ' - ' + str(friendId)
			count += count
			self.con.execute("INSERT INTO users (userId) VALUES ('" + str(friendId) + "')")
			
		cur = self.con.cursor()
		
		cur.execute("SELECT COUNT(*) FROM users")
		result = cur.fetchone()[0]
		
		print "Total users found on the main account: " + str(result)
		if result == 0:
			self.end()	
	
	
	def followUsers(self):
		"""" Follow the users on the secondary account """
		cur = self.con.cursor()
		cur.execute("SELECT userId FROM users")
		
		count = 0
		errorCount = 0
		
		for row in cur.fetchall():
			try:
				self.apiTo.create_friendship(row[0])
	
				if self.DEBUG:
					print "Following user #" + str(count) + " with id: " + str(row[0])
	
				self.con.execute("DELETE FROM users WHERE userId = '" + str(row[0]) + "'")
				count += 1
	
			except tweepy.TweepError:
				# TODO Give a better Error description
				errorCount += 1
				if self.DEBUG:
					print 'Error! Failed to follow user with id: ' + str(row[0])
					
			if self.DEBUG and count == 10:
				print 'Stoping after 10 users so your account is not blocked'
				break
		
		self.con.commit()
		
		if count > 0:
			print 'Users imported: ' + str(count)
		else:
			print 'No Users were imported'
		
		if errorCount > 0:
			print 'Errors: ' + str(errorCount)
	
	
	def end(self):
		print 'Good bye'
		self.con.close()
		
		if self.DEBUG_DELETE_DB:
			try:
				os.remove(self.dbName)
			except OSError:
				pass
		
		sys.exit()
	
print "Import your Friendships from one Twitter account to another"
importer = TwitterFrienshipImporter()
print "--Done"
	