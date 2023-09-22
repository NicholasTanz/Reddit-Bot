import praw
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
from PIL import Image
from io import BytesIO
import requests 
from copy import deepcopy
reddit = praw.Reddit(

    client_id="", #<-- from creating script bot on reddit.com/prefs/apips
    client_secret="", #<-- same as above
    password="", #actual user of our bot
    username="", #actual pass of our bot
    user_agent="T", #can be anything; identifier for you

)
#returns the weekly submissions, and all of its data
def subreddit_submissions_for_one_week(subreddit_name):
        try:
            subreddit = reddit.subreddit(subreddit_name)
            weekly_submissions = []
        
            j = str((datetime.today()))
            for submission in subreddit.new(limit=None):
                k = str(datetime.fromtimestamp(submission.created_utc))
                if (k[0:4] != j[0:4]) or (k[5:7] != j[5:7]) or (int(k[8:10]) + 7 < int(j[8:10])):
                    break
                weekly_submissions.append(submission)
            return weekly_submissions
        except:
            return "Error Incorrect Subreddit Name Entered or Not Enough Information on this Subreddit"


#returns a dictonary where the keys are the different post flairs for that subreddit and the value is the number of times
#that flair was used
def subreddit_percentage_post_flairs(subreddit_name):
    try:
        weekly_submissions = subreddit_submissions_for_one_week(subreddit_name)
        subreddit_post_flairs = {}
        
        for submission in weekly_submissions:
            k = str(submission.link_flair_text)
            if k not in subreddit_post_flairs:
                subreddit_post_flairs[k] = 1
            else:
                subreddit_post_flairs[k]+=1
        
        total_flairs = 0
        other_val = 0
        copy__dict = deepcopy(subreddit_post_flairs)
        for val in subreddit_post_flairs.values():
            total_flairs+=val
        for key, val in copy__dict.items():
            if (key == "Other" and val != 0) or (key == "other" and val != 0) or ((val / total_flairs) < .05):
                    other_val+=val
                    del subreddit_post_flairs[key]
                    
        colors = ['#66CCFF', '#0000FF', '#000080', '#003399', '#0066CC', '#00FFFF', '#3366FF', '#3399FF', '#33CCCC']
        subreddit_post_flairs.update({'Other': other_val})
        values = list(subreddit_post_flairs.values())
        labels = list(subreddit_post_flairs.keys())
        print(subreddit_post_flairs)
        
        return subreddit_post_flairs
    except:
        print("didn't work")
        return "Error Incorrect Subreddit Name Entered or Not Enough Information on this Subreddit"

#gets active and total number of users subscribed to a subreddit
def subreddit_users(subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit_subscribers = subreddit.subscribers
        subreddit_online_users = subreddit.accounts_active
        return {"online users": subreddit_online_users, "total subreddit subscribers": subreddit_subscribers}
    except:
        return "Error Incorrect Subreddit Name Entered or Not Enough Information on this Subreddit"


def subreddit_imgs(subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit_logo = subreddit.icon_img
        subreddit_logo_2 = subreddit.header_img
                
        def subreddit_rgb_fn(subreddit_logo):    
            response = requests.get(subreddit_logo)
            subreddit_logo_image = Image.open(BytesIO(response.content))
            width, height = subreddit_logo_image.size
            r_sum=0
            g_sum=0
            b_sum=0
            subreddit_logo_image = subreddit_logo_image.convert("RGB")
            for x in range(width):
                for y in range(height):
                    r,g,b = subreddit_logo_image.getpixel((x,y))
                    if r == 0 and g == 0 and b == 0:
                        continue
                    else:
                        r_sum+=r
                        g_sum+=g
                        b_sum+=b
            
            r_avg= r_sum // (width * height)
            g_avg = g_sum // (width * height)
            b_avg = b_sum // (width * height)
        
            return "#{:02x}{:02x}{:02x}".format(r_avg,g_avg,b_avg)
                    

        subreddit_rgb_1 = subreddit_rgb_fn(subreddit_logo)
        subreddit_rgb_2 = subreddit_rgb_fn(subreddit_logo_2)

        
        return {'subr_ha1': subreddit_rgb_1, 'subr_lg': subreddit_logo, 'subr_ha2': subreddit_rgb_2}
    except:
        return "Error Incorrect Subreddit Name Entered or Not Enough Information on this Subreddit"

def subreddit_created_utc_fn(subreddit_name):
    try:
        subreddit_name = reddit.subreddit(subreddit_name)
        subreddit_time_utc = subreddit_name.created_utc
        return datetime.fromtimestamp(subreddit_time_utc)
    except:
        return "Error Generated"

