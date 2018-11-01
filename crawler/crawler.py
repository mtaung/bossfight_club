import praw, pickle, identities
from db import db 
from psaw import PushshiftAPI

redditId = identities.PRAWConfig()

class Crawler:
    def __init__(self, cid= redditId.cid, 
                 sec= redditId.sec, 
                 user= redditId.user, 
                 pwd= redditId.pwd, 
                 uage= redditId.uage):
        """
        A crawler object based on the praw Reddit class. 
        """
        self.reddit = praw.Reddit(client_id= cid, 
                                  client_secret= sec,
                                  username= user, 
                                  password= pwd, 
                                  user_agent= uage)

        self.bfSub = self.reddit.subreddit('bossfight')

    def cleanUrl(self, urlString):
        """
        Processes an image url to minimise links unrecognised by discord embed.
        This is to tackle an artifact returned by praw.
        """
        if urlString[-1] == '.':
            urlString = urlString[:-1]
            return urlString
        else:
            return urlString

    def spawnTop(self):
        """
        Pulls the top submissions from the subreddit of all time.
        """
        self.topBf = self.bfSub.top(limit=1000)
        return self.topBf

    def generateBoss(self, roster):
        """
        Returns a generator containing bosses from a list of submissions.
        Parameters:
            roster = a list of submission objects
        """
        for i in roster:
            topComment = [comment.body for comment in i.comments if (hasattr(comment, 'body') and comment.distinguished==None)][0]
            url = self.cleanUrl(i.url)
            yield i.id, i.title, url, topComment

    def weeklyUpdate(self):
        """
        Returns a generator of the top 20 submissions from the subreddit of the past week. 
        """
        weeklyBf = self.bfSub.top(limit=20)
        for i in weeklyBf:
            topComment = [comment.body for comment in i.comments if (hasattr(comment, 'body') and comment.distinguished==None)][0]
            url = self.cleanUrl(i.url)
            yield i.id, i.title, url, topComment

    def pullBoss(self, urlIn):
        """
        Returns a tuple of a boss from a specific submission url.
        """
        submission = self.reddit.submission(url=urlIn)
        url = self.cleanUrl(submission.url)
        return (submission.id, submission.title, submission.score, url, submission.topComment)


"""
crawler = RedditCrawler()
topBf = crawler.spawnTop()
roster = crawler.generateBoss(topBf)
database = db.Database()

boss = database.randomBoss()
for i in boss:
    print(i)"""