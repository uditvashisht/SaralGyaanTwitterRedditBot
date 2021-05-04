import tweepy
import praw
import prawcore
import time
import requests
import logging
import os
import shutil
import facebook
import requests
# pip install python-decouple
from decouple import config


# Login Credentials
REDDIT_CLIENT_ID = config('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = config('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = config('REDDIT_USERNAME')
REDDIT_PASSWORD = config('REDDIT_PASSWORD')
TWITTER_CONSUMER_KEY = config('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = config('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = config('TWITTER_ACCESS_TOKEN_SECRET')
USER_AGENT = 'python:saralgyaan_social_updates:v1.0.0 (by /u/uditvashisht)'
FACEBOOK_PAGE_ID = config('FACEBOOK_PAGE_ID')
FACEBOOK_ACCESS_TOKEN = config('FACEBOOK_ACCESS_TOKEN')

# Dictionary containing subreddits and tags
SUBREDDIT_DICT = {'programmerhumor': ['progammer', 'programmerhumor', 'humor'],
                  'programmingmemes': ['programming', 'programmingmemes', 'programmerhumor'],
                  'xkcd': ['xkcd', 'xkcdcomics']
                  }


current_dir = os.getcwd()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f'{os.path.join(current_dir, "social-update.log")}')
fmt = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s : %(message)s')
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


def auto_post_facebook(picture, message):
    """A function which auto-posts the photos with hastags on facebook.

    Requires
    --------
    facebook: module
        pip install facebook-sdk, import facebook
    page_id : str
        Page ID of the facebook page.
    access_token : str
        Access token of facebook account.

        Can be obtained from https://developers.facebook.com/tools.
        Use this tutorial
        https://pythoncircle.com/post/666/automating-facebook-page-posts-using-python-script/
    Parameters
    __________
    message : str
        title and hashtags of the photo.
    picture: str
        Complete link of the header image.

    Posts
    _____
        A post containing photo title and hashtags

    """
    graph = facebook.GraphAPI(FACEBOOK_ACCESS_TOKEN)
    facebook_page_id = FACEBOOK_PAGE_ID
    #IF you want to post a status update
    # graph.put_object(facebook_page_id, "feed", message='test message')
    graph.put_photo(image=open(picture, 'rb'),
                    message=message)


def login_to_reddit():
    """ This function log into to the reddit account and returns the Reddit Instance by interacting with Reddit's API through PRAW

    Parameters:
    -----------
    None

    Returns:
    --------
    A Reddit Instance

    """

    try:
        logger.info('* Logging into Reddit Account')
        reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                             client_secret=REDDIT_CLIENT_SECRET,
                             password=REDDIT_PASSWORD,
                             user_agent=USER_AGENT,
                             username=REDDIT_USERNAME)
        logger.info('* Login successful')
        return reddit
    except:
        logger.info('* Login failed')


def grab_new_image(url):
    """ This function grabs the image from the URL of the reddit post and save it as img.jpg

    Parameters:
    -----------
    url : str
        URL of the subreddit containing the image

    Returns:
    --------
    An Image

    """
    logger.info('* Fetching image from the Reddit')
    try:
        response = requests.get(url)
        with open('img.jpg', 'wb') as image:
            image.write(response.content)
            image.close()
        logger.info('* Image saved successfully')
    except:
        logger.info('* Something went wrong while downloading image')


def post_tweet(tweet_content):
    """ This function post the tweet update with the image

    Parameters:
    -----------
    tweet_content : str

    Execute:
    --------
    Post the tweet with the image

    """

    try:
        logger.info('* Logging into twitter')
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                   TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN,
                              TWITTER_ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)
        logger.info('* Login successful')

        tweet = tweet_content
        image_path = 'img.jpg'

        logger.info('* Posting on twitter')
        api.update_with_media(image_path, tweet)
        logger.info("* Successfully posted")
    except:
        logger.info('* Something went wrong while posting tweet')


def main(sub_reddit, tags):
    """ This main function check the sub reddit for images, download the images using grab_new_image() and then tweet it using post_tweet()

    Parameters:
    -----------
    sub_reddit : str
        Name of the sub reddit to check
    tags : list
        list of hashtags to be used

    """

    reddit = login_to_reddit()
    try:
        for submission in reddit.subreddit(sub_reddit).hot(limit=8):
            if submission.stickied == False:
                logger.info("* Fetching submission from reddit")
                post_url = f'redd.it/{str(submission)}'
                title = submission.title
                tweet_content = f'{title} posted by {str(submission.author)} {post_url} #{" #".join(tags)}'
                url = submission.url
                if 'jpg' in url:
                    grab_new_image(url)
                    post_tweet(tweet_content)
                    auto_post_facebook('img.jpg', f'{title} #{" #".join(tags)}')
                    time.sleep(20)
                elif 'png' in url:
                    grab_new_image(url)
                    post_tweet(tweet_content)
                    auto_post_facebook('img.jpg', f'{title} #{" #".join(tags)}')
                    time.sleep(20)
                else:
                    logger.info("* Not an image url")
    # exception handling
    except prawcore.exceptions.ServerError as e:
        logger.info(e)
        time.sleep(20)
        pass

    # excepts errors like rate limit
    except praw.exceptions.APIException as e:
        logger.info(e)
        time.sleep(60)

    # excepts other PRAW errors
    except praw.exceptions.PRAWException as e:
        logger.info(e)
        time.sleep(20)

    # excepts network connection errors
    except prawcore.exceptions.RequestException:
        logger.info("* Please check your network connection")
        logger.info("* Sleeping for 1 minute")
        time.sleep(60)


if __name__ == "__main__":
    for key, value in SUBREDDIT_DICT.items():
        main(key, value)
