from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=21)
    class Meta:
        get_latest_by = 'id'


    #returns the subreddits used by the user 
    user_karma = 0
    date_created = ""
    common_subreddits = {}
    Average_Likes_Per_Post = 0
    monthly_submissions = []
    monthly_comments = [] 

    def __str__(self):
        return self.user_name


class SubReddit(models.Model):
    subreddit_name = models.CharField(max_length=21)
    
    class Meta:
        get_latest_by = 'id'

    #returns the comment flairs used in this subreddit
    subreddit_post_flairs = {}
    weekly_submissions = []


    def __str__(self):
        return self.subreddit_name



