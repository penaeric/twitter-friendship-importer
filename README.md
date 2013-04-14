Import your Twitter friends from one account to another - twitter-friendship-importer
===========================



*Go to the [source code](http://github.com/penaeric/twitter-friendship-importer/blob/master/twitter-friendship-importer.py).*

Dependency: [Tweepy](http://tweepy.github.io/)

[Tweepy Documentation](http://pythonhosted.org/tweepy/html/index.html)




Instructions
-------------------------------


* Install Tweepy via easy_install

	$ easy_install tweepy


* For each account go to [https://dev.twitter.com/apps/](https://dev.twitter.com/apps/)
	* Login. 
	* Create a new application leaving the **Callback URL** blank.
	* After you're done, go to **Settings** and give **Read and Write** access to your new app. Update your application's settings.
* Run the Python script.  
* For each account 
	* Enter the **Consumer key** and the **Consumer secret**.  
	* Go to the URL given by the script and authorize the script. 
	* Twitter will give you a *PIN* number which you'll need for the script.


Note
-------------------------------


**Twitter will potentially block your secondary account** if you follow a lot of users in a short ammount of time. This might be fine for many users as you probably want to run this script once.

This script might be also useful if you want to 'sync' the users you're following (running the script every once in a while) although I don't know if Twitter counts this as *aggressive following behavior*. 
For more information on Twitter following rules and best practices, visit:

* [https://support.twitter.com/groups/32-something-s-not-working/topics/116-account-settings-problems/articles/15790-how-to-contest-account-suspension](https://support.twitter.com/groups/32-something-s-not-working/topics/116-account-settings-problems/articles/15790-how-to-contest-account-suspension)
* [https://support.twitter.com/articles/68916](https://support.twitter.com/articles/68916)
	
	
Todo
--------------------------------

- [ ] Documentation with instructions (and pictures?)

- [ ] If tokens are in the database, ask the user if she wants to use them (right now, if the user screws up, she will have to delete de database and start again)

- [ ] Check if tokens work before continuing. If they don't work, give user option to try again

- [ ] Improve error handling

- [ ] Decide what to do with the friends that can't be added

- [ ] Give better error descriptions

- [ ] Use callbacks and Python's webbrowser library to minimize user input

- [ ] Check if already following user before trying to follow

- [ ] Refactor getToTokens and getFromTokens to share common code