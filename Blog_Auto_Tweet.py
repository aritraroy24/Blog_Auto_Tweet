# Importing modules
import tweepy
import datetime
from decouple import config
import logging

# logging config
logging.basicConfig(level=logging.INFO, filename='data.txt',)
logger = logging.getLogger()


# Keys
CONSUMER_KEY = config('Consumer_Key')
CONSUMER_SECRET_KEY = config('Consumer_Secret_Key')
ACCESS_TOKEN = config('Access_Token')
ACCESS_TOKEN_SECRET = config('Access_Token_Secret')
# Authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
userID = "aritraroy24"


def get_date_list(tweets):
    # Getting tweet date-time
    date_list1 = []
    for tweet in (tweets):
        created_date = (str(tweet.created_at)).split("+")[0]
        created_date = datetime.datetime.strptime(
            created_date, '%Y-%m-%d %H:%M:%S')
        date_list1.append(created_date)

    # Getting date-time now
    date_now = str(datetime.datetime.now())
    date_now = date_now.split(".")
    date_now = datetime.datetime.strptime(date_now[0], '%Y-%m-%d %H:%M:%S')
    # Getting minute diff of tweet timing and now
    final_minute_list = []
    for i in date_list1:
        result = i - date_now
        result = str((round((result.total_seconds())/60)))
        first_result = result.split(" ")[0]
        final_result = first_result.split("-")[1]
        final_minute_list.append(final_result)
    return final_minute_list


def get_text_list(date_list, tweets):
    # Getting tweet text
    list1 = [
        tweet.full_text
        for minute, tweet in zip(reversed(date_list), reversed(tweets))
        if "#myblogs" in tweet.full_text.lower() and int(minute) >= 24000
    ]
    # Getting the latest tweets done by the bot
    list2 = [
        tweet.full_text
        for minute, tweet in zip(reversed(date_list), reversed(tweets))
        if "#myblogs" in tweet.full_text.lower() and int(minute) <= 24000
    ]
    # Removing the tweets same previous tweets
    for item in list2:
        if item in list1:
            list1.remove(item)
    return list1


def auto_tweet(text_list):
    # Reposting the tweet
    for text in text_list:
        try:
            api.update_status(text)
            logger.info(
                f"Tweet done at : {str(datetime.datetime.now())}\n\n\n")

        except Exception as e:
            logger.info(
                f"Tweet can't be done at : {str(datetime.datetime.now())} due to {e} error\n\n\n")


if __name__ == '__main__':
    tweets = api.user_timeline(
        screen_name=userID, count=200, tweet_mode='extended')
    minute_list = get_date_list(tweets)
    text_list = get_text_list(minute_list, tweets)
    auto_tweet(text_list)
    logger.info(
        f"Ran at : {str(datetime.datetime.now())}\n==================   *****   =================\n")