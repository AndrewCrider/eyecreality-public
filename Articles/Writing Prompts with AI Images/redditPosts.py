import praw
from requests import Session
import csv
import os

locationPath = 'myLocation'
# register Reddit Application here: https://www.reddit.com/prefs/apps/
myClientId = 'get client Id here'
myClientSecret = 'clientSecret'
redditPassword = 'your password'

#replace this with your information per: https://praw.readthedocs.io/en/stable/getting_started/configuration.html
redditInfo = praw.Reddit(
                client_id= myClientId,
                client_secret= myClientSecret,
                password= redditPassword,
                requestor_kwargs={"session": session},  # pass the custom Session instance
                user_agent="testscript by u/fakebot3",
                username="fakebot3",
            )

def getRedditPosts(subredditName):
    wpcsv_columns = ['summary','style', 'genre' ,'title', 'url', 'id', 'author']
    writing_prompts_dict = []
    wpCSV = locationPath+ "/wprompts500.csv"

    session = Session()
    reddit = redditInfo
    
    subreddit = reddit.subreddit(subredditName)
    top_subredditlist = subreddit.top(limit=500)

    for submission in top_subredditlist:
        #Adding Columns for User Summarization and Decisions
        array = ['','','',submission.title, submission.url, submission.id, submission.author]
        writing_prompts_dict.append(dict(zip(wpcsv_columns, array)))

    print(len(writing_prompts_dict))

    with open(wpCSV, "w") as csv_file:
        writer = csv.DictWriter(csv_file, wpcsv_columns)
        writer.writeheader()
        writer.writerows(writing_prompts_dict)
    csv_file.close()

if __name__ == "__main__":
    getRedditPosts('writingprompts')