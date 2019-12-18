# reddit-analyzer


```
usage: reddit-analyzer.py <screen_name>
```

This is really a simple little tool. It pulls data from an API to tell you:
- when an account was made
- when an account posted last
- how many times a user has posted
- how much karma they recieved for said posts
- when they are most active on reddit
- what subreddits they frequent
- if any of those subreddits correlate to a physical location


all-locations.txt is a large list of subreddits that are tied to locations in the real world (countries, states, cities, colleges.)
If you want lists for just specific reigons, i seperated the lists and they can be found under my other repo, [location-subreddits](https://github.com/sshell/location-subreddits)


### Example Output

![example output](https://i.imgur.com/qWlw82T.png)


### Special Thanks

I _really_ like [tweets_analyzer](https://github.com/x0rz/tweets_analyzer) by [@x0rz](https://twitter.com/x0rz) and this is obviously very heavily inspired by his work with that 

Also, a big part of this is that I like projects where I don't have to run around retrieving API keys and throwing them into files to get things to run. God bless [pushshift](https://pushshift.io/) for making this possible.
