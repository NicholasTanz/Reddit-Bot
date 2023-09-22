import praw
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from matplotlib import pyplot
import io
import urllib, base64
import sys

reddit = praw.Reddit(

    client_id="", #<-- from creating script bot on reddit.com/prefs/aps
    client_secret="", #<-- same as above
    password="", #actual user of our bot
    username="", #actual pass of our bot
    user_agent="", #can be anything; identifier for you
)


#Generates the users comment karma and post karma
def user_karma(username):
    try:
        user = reddit.redditor(username)
        comment_karma = user.comment_karma
        post_karma = user.link_karma
        
        return {'comment_karma': comment_karma, 'post_karma': post_karma}
    except:
        return "Username was Incorrectly Entered or not enough activity from the User"


def user_monthly_stats(username):
    try:
        user = reddit.redditor(username)
        comment = user.comments

        monthly_submissions = []
        monthly_comments = []
        activity_level = None
        
        for submission in user.submissions.top(time_filter="month"):
            
            #getting time of comments and their times
            ts = (int((submission.created_utc)))
            utc_to_readable = (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            monthly_submissions.append(utc_to_readable[0:9])
        
        for comment in user.comments.top(time_filter="month"):
            
            #getting time of comments and their times
            ts = (int((comment.created_utc)))
            utc_to_readable = (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            monthly_comments.append(utc_to_readable[0:9])

        return {'Monthly Post Times': monthly_submissions, 'Monthly Comment Times': monthly_comments}
    except:
        return "Username was Incorrectly Entered or not enough activity from the User"


#Generates the Subreddits this user Was on for the Month and their average post likes
def user_subreddits_and_likes(username):
    try:
        user = reddit.redditor(username)
        
        comments = user.comments #sublisting instance

        common_subreddits = {} #generates a hashmap of common subreddits for the user
        common_comment_likes = 0 #generates the average number of likes from recent comments
        counter_comments = 0
        
        for comment in comments.new():
            comment_subreddit = comment.subreddit
            counter_comments+=1
            common_comment_likes = (common_comment_likes + comment.score) / counter_comments
            try:
                common_subreddits[str(comment_subreddit)] += 1
            except:
                common_subreddits[str(comment_subreddit)] = 1

        total_flairs = 0
        other_val = 0
        copy__dict = deepcopy(common_subreddits)
        for val in common_subreddits.values():
            total_flairs+=val
        for key, val in copy__dict.items():
            if ((val / total_flairs) < .045):
                    other_val+=val
                    del common_subreddits[key]
                    
        colors = ['#66CCFF', '#0000FF', '#000080', '#003399', '#0066CC', '#00FFFF', '#3366FF', '#3399FF', '#33CCCC']
        common_subreddits.update({'Other Subreddits': other_val})
        values = list(common_subreddits.values())
        labels = list(common_subreddits.keys())

        return {'common subreddits': common_subreddits, 'avg_com_lk': common_comment_likes}
    except:
        return "Username was Incorrectly Entered or not enough activity from the User"

#Calculates how active a user is
def user_activity_level(username):
    try:
        dictonary_use = user_monthly_stats(username)
        monthly_submissions = dictonary_use['Monthly Post Times']
        monthly_comments = dictonary_use['Monthly Comment Times']
        activity_level = None

        if(len(monthly_submissions) / 30 >= 1 or len(monthly_comments) / 30 >= 1):
            activity_level = "Daily"
        elif (len(monthly_submissions) / 30 >= .75 or len(monthly_comments / 30) >= .4):
            activity_level = "Every few Days"

        elif(len(monthly_submissions) / 30 >= .25 or len(monthly_comments / 30) >= .25):
            activity_level = "Weekly"
        elif(len(monthly_submissions / 30 >= .1) or len(monthly_comments) / 30 >= .12):
            activity_level = "Monthly"
        else:
            activity_level = "Less than Monthly Activity"

        return activity_level
    except:
        return "Username was Incorrectly Entered or not enough activity from the User"


def user_avatar(user_name):
    try:
        user = reddit.redditor(user_name)
        user_avatar = user.icon_img
        return user_avatar
    except:
        return "Username was Incorrectly Entered or not enough activity from the User"

def user_created_utc_fn(user_name):
    try:
        user = reddit.redditor(user_name)
        user_created_utc = user.created_utc
        return datetime.fromtimestamp(user_created_utc)
    except:
        return 'Error Generated'

#Make a function that can determine user position (banned / not / time created / employee / mod /etc.)




