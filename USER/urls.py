from . import views
from django.urls import path

urlpatterns = [

    path("", views.base, name='base_pa'),
    path("u/", views.user, name='user_pa'),
    path("s/",views.subreddit, name='subreddit_pa'),
    path("f/", views.check_box_user, name='checkbox_user_pa'),
    path("r/",views.check_box_subreddit, name='checkbox_subr_pa'),
    path("c/", views.compare, name='compare_user_pa')
]

