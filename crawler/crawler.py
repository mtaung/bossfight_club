import praw, pickle
from requests_html import HTMLSession
from psaw import PushshiftAPI

class Crawler:
    def __init__(self, cid, sec, user, pwd, uage):
        """
        A crawler object based on the praw Reddit class. 
        """
        self.reddit = praw.Reddit(client_id= cid, 
                                  client_secret= sec,
                                  username= user, 
                                  password= pwd, 
                                  user_agent= uage)
        self.bfSub = self.reddit.subreddit('bossfight')
        self.session = HTMLSession()
    
    def extractImgurUrl(self, urlString):
        """
        Processes an image url to minimise links unrecognised by discord embed.
        This is to tackle an artifact returned by praw.
        """
        try:
            r = self.session.get(urlString)
        except:
            return None
        if r.status_code != 200:
            return None
        element = r.html.find('[rel=image_src]', first=True)
        if not element:
            return None
        """else:
            newUrlSearch = r.html.find('[itemprop=embedURL]', first=True)
            newUrl = newUrlSearch.attrs.get('content')
            return newUrl"""
        return element.attrs.get('href')

    def extractUrl(self, urlString):
        if urlString.startswith('http://imgur.com') or urlString.startswith('https://imgur.com'):
            return self.extractImgurUrl(urlString)
        else:
            return None
    
    def getUsableUrl(self, urlString):
        try:
            r = self.session.head(urlString)
        except:
            return None
        if r.status_code != 200:
            return None
        ctype = r.headers.get('content-type')
        if not ctype:
            return None
        if ctype == 'image/jpeg' or ctype == 'image/png' or ctype == 'image/gif':
            return urlString
        else:
            newUrl = self.extractUrl(urlString)
            if not newUrl:
                return None
            return self.getUsableUrl(newUrl)

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
            #topComment = [comment.body for comment in i.comments if (hasattr(comment, 'body') and comment.distinguished==None)][0]
            topComment = ''
            url = self.getUsableUrl(i.url)
            if not url:
                continue
            yield i.id, i.title, i.score, i.url, topComment

    def weeklyUpdate(self):
        """
        Returns a generator of the top 20 submissions from the subreddit of the past week. 
        """
        weeklyBf = self.bfSub.top(limit=20)
        for i in weeklyBf:
            topComment = [comment.body for comment in i.comments if (hasattr(comment, 'body') and comment.distinguished==None)][0]
            url = self.getUsableUrl(i.url)
            if not url:
                continue
            yield i.id, i.title, i.score, url, topComment

    def pullBoss(self, urlIn):
        """
        Returns a tuple of a boss from a specific submission url.
        """
        submission = self.reddit.submission(url=urlIn)
        url = self.getUsableUrl(submission.url)
        if not url:
            raise Exception("rip")
        return (submission.id, submission.title, submission.score, url, submission.topComment)
