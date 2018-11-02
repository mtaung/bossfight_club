import praw, pickle
from identities import PRAWConfig
from requests_html import HTMLSession
from db import db 
from psaw import PushshiftAPI

redditId = PRAWConfig()

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
        self.htmlsession = HTMLSession()
        self.bfSub = self.reddit.subreddit('bossfight')

    def cleanUrl(self, urlString):
        """
        Processes an image url to minimise links unrecognised by discord embed.
        This is to tackle an artifact returned by praw.
        """
        if urlString.startswith('http://imgur.com') or urlString.startswith('https://imgur.com'):
            r = session.get(urlString)
            newUrlSearch = r.html.find('[rel=image_src]', first=True)
            if newUrlSearch:
                return newUrlSearch.attrs.get('href')
            else:
                newUrlSearch = r.html.find('[itemprop=embedURL]', first=True)
                newUrl = newUrlSearch.attrs.get('content')
                return newUrl

    def spawnTop(self):
        """
        Pulls the top submissions from the subreddit of all time.
        Returns a list of submission objects.
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
            yield i.id, i.title, i.score, url, topComment

    def weeklyUpdate(self):
        """
        Returns a generator of the top 20 submissions from the subreddit of the past week. 
        """
        weeklyBf = self.bfSub.top(limit=20)
        for i in weeklyBf:
            topComment = [comment.body for comment in i.comments if (hasattr(comment, 'body') and comment.distinguished==None)][0]
            url = self.cleanUrl(i.url)
            yield i.id, i.title, i.score, url, topComment

    def pullBoss(self, urlIn):
        """
        Returns a tuple of a boss from a specific submission url.
        """
        submission = self.reddit.submission(url=urlIn)
        url = self.cleanUrl(submission.url)
        return (submission.id, submission.title, submission.score, url, submission.topComment)

    def initialiseDb(self):
        crawler = RedditCrawler()
        topBf = crawler.spawnTop()
        roster = crawler.generateBoss(topBf)

        database = db.Database()
        database.initTables()

        for iid, ititle, iscore, url, topcomment in roster:
            database.registerBoss((iid, ititle, iscore, url, topcomment))

crawler=Crawler()
crawler.initialiseDb()