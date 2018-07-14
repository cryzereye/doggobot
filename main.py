import praw, json, time, tweepy, os, requests

twitter_auth = tweepy.OAuthHandler('','') #previously static tokens
twitter_auth.set_access_token('','') #previously static tokens
twitter_api = tweepy.API(twitter_auth)

reddit = praw.Reddit(client_id='',
                     client_secret="",
                     password='',
                     user_agent='',
                     username='')
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
                twitter_api.update_with_media(filename, status=message)
                print("tweeted: " + submit.url)
                os.remove(filename)