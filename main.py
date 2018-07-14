import praw, json, time, tweepy, os, requests

def get_twitter_api(file):
    twitter_auth = tweepy.OAuthHandler(file['twitter']['cons_token'],file['twitter']['cons_token_secret'])
    twitter_auth.set_access_token(file['twitter']['acc_token'],file['twitter']['acc_token_secret'])
    twitter_api = tweepy.API(twitter_auth)
    return twitter_api

def get_reddit_api(file):
    reddit_api = praw.Reddit(client_id=file['reddit']['client_id'],
                        client_secret=file['reddit']['client_secret'],
                        password=file['reddit']['password'],
                        user_agent=file['reddit']['user_agent'],
                        username=file['reddit']['username'])
    return reddit_api

def __init__(config_file):
    with open(config_file) as f:
        config_data = json.load(f)

    twitter = get_twitter_api(config_data)
    reddit = get_reddit_api(config_data)

    doggo_multi = reddit.multireddit('cryzereye', 'dog').stream.submissions()
    allowed_media = ['.jpg', '.gif', '.jpeg', '.png']
    start_time = time.time()
    while(True):
        for submit in doggo_multi:
            if submit.created_utc > start_time and any(x in submit.url for x in allowed_media):
                # below: https://stackoverflow.com/questions/31748444/how-to-update-twitter-status-with-image-using-image-url-in-tweepy
                request = requests.get(submit.url, stream=True)
                filename = 'temp.jpg'
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)
                    message = submit.title[:100] + "\n\nfrom: " + submit.url
                    twitter.update_with_media(filename, status=message)
                    print("tweeted: " + submit.url)
                    os.remove(filename)

__init__('config.json')