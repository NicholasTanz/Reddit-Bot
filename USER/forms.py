from django import forms
from django.forms import ModelForm
from .models import User, SubReddit


class User_Form(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class Subreddit_Form(ModelForm):
    class Meta:
        model = SubReddit
        fields = "__all__"


class User_Choice_Form(forms.Form):
    choices_user = [
    
        ('Karma', 'Karma'),
        ('Subreddits Used', 'Subreddits Used'),
        ('Activity Level', 'Activity Level'),
        ('This Months Posts', 'This Months Posts'),
        ('This Months Comments', 'This Months Comments'),
        ('Average Likes Per Comment', 'Average Likes Per Comment'),
        ('Users Avatar', 'Users Avatar'),
        ('Date Created', 'Date Created')

    ]
    checkbox = forms.MultipleChoiceField(choices=choices_user,
    widget=forms.CheckboxSelectMultiple
    )

class Subreddit_Choice_Form(forms.Form):
    choices_subreddit = [
    
        ('Total Subscribers', 'Total Subscribers'),
        ('Online Subscribers', 'Online Subscribers'),
        ('Most Common Post Flairs', 'Most Common Post Flairs'),
        ('This Weeks Submissions', 'This Weeks Submissions'),
        ('Date Created', 'Date Created'),
    ]

    checkbox = forms.MultipleChoiceField(choices=choices_subreddit,
    widget=forms.CheckboxSelectMultiple)








