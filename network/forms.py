from django import forms
# from django.utils.translation import gettext_lazy as _

from network.models import Comment, Tweet


class NewTweetForm(forms.ModelForm):
    
    class Meta:
        model = Tweet
        fields = ["content"]

class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]