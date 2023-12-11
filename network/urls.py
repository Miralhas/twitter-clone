from django.urls import path

from network import views

app_name = "network"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("new", views.NewTweetView.as_view(), name="new_tweet"),
    path("delete/<int:pk>", views.DeleteTweetView.as_view(), name="delete"),
    path("tweets", views.AllTweetsView.as_view(), name="tweets"),
    path("following", views.FollowingTweetsView.as_view(), name="following_tweets"),
    path("<str:username>/tweets/<int:tweet_pk>/", views.TweetDetailView.as_view(), name="tweet_detail"),
    path("tweets/<int:tweet_pk>/delete", views.delete_tweet, name="delete_tweet"),
    path("tweets/<int:tweet_pk>/edit", views.edit_tweet, name="edit_tweet"),
    path("tweets/<int:pk>/<str:action>", views.tweet_like, name="tweet_like"),
    path("follow", views.follow, name="follow"),
    path("search/", views.SearchView.as_view(), name="search"),
]