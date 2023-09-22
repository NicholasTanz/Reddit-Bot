from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from .forms import User_Form, Subreddit_Form, User_Choice_Form, Subreddit_Choice_Form
from .models import User, SubReddit
from .backend_subreddit_functions import *
from .backend_user_functions import *
from django.urls import reverse

# Create your views here.

def base(request):
    k = User.objects.all()
    l = SubReddit.objects.all()

    return render(request, "USER/home.html", {"data_user": k, "data_sub": l})

def subreddit(request):
    submitted = False

    if request.method == "POST":
        form = Subreddit_Form(request.POST)
        if form.is_valid():
            form.save()

            request.method == "GET"
            return redirect(reverse(check_box_subreddit))
    else:
        form = Subreddit_Form
        if 'submitted' in request.GET:
            submitted = True

    return render(request, "User/subreddit.html", {"form": form, "submitted": submitted})

def check_box_subreddit(request):
    current_model = str(SubReddit.objects.latest())

    if request.method == 'POST':
        form = Subreddit_Choice_Form(request.POST)
        if form.is_valid():
            
            interests = form.cleaned_data['checkbox']
            
            #calling functions for the various checkboxes
            subr_sub = None
            subr_onl = None
            subr_cmn_fl = None
            subr_wk_sb = None
            subr_100_sb = None
            subr_lg = None
            subr_dc = None
            subr_rgb1 = None 
            subr_rgb2 = None
            subreddit_logos = None
            try:
                subreddit_logos = subreddit_imgs(current_model)
                
                subr_lg = subreddit_logos['subr_lg']
                subr_rgb1 = str(subreddit_logos['subr_ha1'])
                subr_rgb2 = str(subreddit_logos['subr_ha2'])
            except:
                pass

            if 'Total Subscribers' in interests:
                subr_sub = subreddit_users(current_model)
                try:
                    subr_sub = subr_sub['total subreddit subscribers']
                except:
                    pass
            if 'Online Subscribers' in interests:
                subr_onl = subreddit_users(current_model)
                try:
                    subr_onl = subr_onl['online users']
                except:
                    pass
            if 'Most Common Post Flairs' in interests:
                subr_cmn_fl = subreddit_percentage_post_flairs(current_model)
            if 'This Weeks Submissions' in interests:
                subr_wk_sb = subreddit_submissions_for_one_week(current_model)
                try:
                    if type(subr_wk_sb) == list:
                        subr_wk_sb = len(subr_wk_sb)
                    else:
                        subr_wk_sb = "Error Generated"
                except:
                    subr_wk_sb = "Error Generated"
            if 'Date Created' in interests:
                try:
                    subr_dc = subreddit_created_utc_fn(current_model)
                except:
                    pass
            
            return render(request, "USER/sucess_sub.html", {'subr_sub': subr_sub, 'subr_onl': subr_onl, 
            'subr_cmn_fl': subr_cmn_fl, 'subr_wk_sb': subr_wk_sb,
             'subr_100_sb':subr_100_sb, 'current':current_model,
             'subr_lg': subr_lg, "subr_rgb1":  subr_rgb1 , "subr_rgb2": subr_rgb2, 'subr_dc': subr_dc})
    
        form = Subreddit_Choice_Form
        return render(request, "User/subreddit_form.html", {"form": form})
    else:
        form = Subreddit_Choice_Form
        return render(request, "User/subreddit_form.html", {"form": form})


def user(request):
    submitted = False
    
    if request.method == "POST":
        form = User_Form(request.POST)
        
        if form.is_valid():
            form.save()
            
            request.method = "GET"
            return redirect(reverse(check_box_user))
    else:
        form = User_Form
        if 'submitted' in request.GET:
            submitted = True
   
    return render(request, "User/user.html", {"form": form, "submitted": submitted})

def check_box_user(request):
    current_model = str(User.objects.latest())

    if request.method == 'POST':
        form = User_Choice_Form(request.POST)
        if form.is_valid():
            
            interests = form.cleaned_data['checkbox']
        

            #calling functions for the various checkboxes
            user_karma_val = None
            user_subreddits = None
            user_activity_level_val = None
            user_monthly_coms_val = None
            user_monthly_posts_val = None
            user_avatar_val = None
            user_coms_avg = None
            user_dc = None
            
            if 'Karma' in interests:
                user_karma_val = user_karma(current_model)
                
                if type(user_karma_val) != str:
                    user_karma_val = user_karma_val['comment_karma'] + user_karma_val['post_karma']
                else:
                    user_karma_val = "Error Generated this user may not exist"
            if 'Subreddits Used' in interests:
                user_subreddits = user_subreddits_and_likes(current_model)
                try:
                    user_subreddits = user_subreddits['common subreddits']
                except:
                    pass
            if 'Average Likes Per Comment' in interests:
                user_coms_avg = user_subreddits_and_likes(current_model)
                try:
                    user_coms_avg = round(user_coms_avg['avg_com_lk'], 2)        
                except:
                    pass
            if 'Activity Level' in interests:
                user_activity_level_val = user_activity_level(current_model)
            
            
            if 'This Months Posts' in interests:
                user_monthly_posts_val = user_monthly_stats(current_model)
                try:
                    user_monthly_posts_val = len(user_monthly_posts_val['Monthly Post Times'])
                except:
                    pass 
            if 'This Months Comments' in interests:
                user_monthly_coms_val = user_monthly_stats(current_model)
                try:
                    user_monthly_coms_val = len(user_monthly_coms_val['Monthly Comment Times'])
                except:
                    pass

            if 'Users Avatar' in interests:
                user_avatar_val = user_avatar(current_model)
            
            if 'Date Created' in interests:
                try:
                    user_dc = user_created_utc_fn(current_model)
                except:
                    pass

            return render(request, "USER/sucess.html", {"user_name": current_model, "user_k": user_karma_val, 
            "user_sbl": user_subreddits, "user_ACT": user_activity_level_val, 
            "user_mon_stat": user_monthly_posts_val, "user_ava": user_avatar_val,
            "user_com_stat": user_monthly_coms_val, "user_avg_com": user_coms_avg, 'user_dc': user_dc,
            })
    
        form = User_Choice_Form
        return render(request, "User/user_form.html", {"form": form})
    else:
        form = User_Choice_Form
        return render(request, "User/user_form.html", {"form": form})


def compare(request):
    return render(request, 'USER/compare_user.html', {})



