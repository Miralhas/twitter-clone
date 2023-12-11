import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView
from django.views.generic.base import View

from accounts.models import User
from network.forms import NewCommentForm, NewTweetForm
from network.models import Follow, Tweet

# Create your views here.

class IndexView(View):
    model = Tweet
    form_class = NewTweetForm
    template_name = "network/index.html"
    
    def get_queryset(self):
        return Tweet.objects.all()[:5]

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={
            "tweets": self.get_queryset(),
            "form": self.form_class()
        })


class NewTweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = NewTweetForm
    template_name = "network/new_tweet.html"
    success_url = "/"

    def form_valid(self, form):
        new_tweet = form.save(commit=False)
        new_tweet.user = self.request.user
        new_tweet.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        path = self.request.POST.get("path")
        if path is not None:
            return path
        return "/"
    

class AllTweetsView(ListView):
    model = Tweet
    template_name = "network/all_tweets.html"
    context_object_name = "tweets"
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = NewTweetForm()
        context["form"] = form
        return context


class FollowingTweetsView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "network/following_tweets.html"
    context_object_name = "tweets"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = NewTweetForm()
        context["form"] = form
        return context
    
    def get_queryset(self, **kwargs):
        user = self.request.user
        following_users_ids = user.following.values_list('following_user_id', flat=True)
        posts = Tweet.objects.filter(user__id__in=following_users_ids)

        return posts


class DeleteTweetView(LoginRequiredMixin, DeleteView):
    model = Tweet
    
    def get_success_url(self):
        return self.request.user.get_absolute_path()


def tweet_like(request, pk, action):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    try:
        user_liking = User.objects.get(pk=data.get("userLiking"))
    except User.DoesNotExist:
        return JsonResponse({
                "error": f"User {data.get('userLiking')} does not exist."
            }, status=400)
    
    tweet = Tweet.objects.filter(pk=pk).first()
    
    if action == "like":
        tweet.likes.add(user_liking)
    elif action == "unlike":
        tweet.likes.remove(user_liking)
    return JsonResponse({"message": "Ok"}, status=200)


def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    status = data.get("status")
    request_user = data.get("request_user")
    user_profile = data.get("user_profile")
    try:
        request_user = User.objects.get(pk=request_user)
        user_profile = User.objects.get(pk=user_profile)
    except User.DoesNotExist:
        return JsonResponse({"message": "User does not Exist!"}, status=400)

    if status == "follow":
        Follow.objects.create(user=request_user, following_user=user_profile)
    else:
        request_user.following.get(following_user=user_profile).delete()
        request_user.save()

    return JsonResponse({"message": "Ok"}, status=200)


def delete_tweet(request, tweet_pk):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    request_user_pk = int(data.get("request_user"))
    
    try:
        tweet = Tweet.objects.get(pk=tweet_pk)
    except Tweet.DoesNotExist:
        return JsonResponse({"message": "Tweet does not exist!"}, status=404)

    if tweet.user.pk != request_user_pk:
        return JsonResponse({"message": "User provided is not the tweet owner!"}, status=403)

    tweet.delete()
    return JsonResponse({"message": "Ok"}, status=200)


def edit_tweet(request, tweet_pk):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    data = json.loads(request.body)
    tweet_owner_pk = data.get("tweet_owner")
    tweet_pk = data.get("tweet_pk")
    new_tweet_content = data.get("new_tweet_content")

    try:
        tweet = Tweet.objects.get(pk=tweet_pk)
    except Tweet.DoesNotExist:
        return JsonResponse({"message": "Tweet does not exist!"}, status=404)

    if tweet.user.pk != tweet_owner_pk:
        print(tweet.user.pk)
        print(tweet_owner_pk)
        return JsonResponse({"message": "User provided is not the tweet owner!"}, status=403)
    
    tweet.content = new_tweet_content
    tweet.save()
    return JsonResponse({"message": "Ok"}, status=200)


class TweetDetailView(View):
    template_name = "network/tweet_detail.html"
    context_object_name = "tweet"
    form_class = NewCommentForm

    def get(self, request, username, tweet_pk, **kwargs):
        form = self.form_class()
        tweet = get_object_or_404(Tweet, pk=tweet_pk)
        comments = tweet.comments.all()
        if tweet.user.username != username:
            return HttpResponseRedirect(reverse("network:index"))
        
        return render(request, self.template_name, context={
            "form": form,
            "tweet": tweet,
            "comments": comments
        }) 

        
    def post(self, request, username, tweet_pk, **kwargs):
        user = request.user
        tweet = get_object_or_404(Tweet, pk=tweet_pk)
        path = request.POST.get("path")
        if user.is_authenticated:
            form = self.form_class(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = user
                comment.tweet = tweet
                comment.save()
            else:
                print(f"Error: {form.errors}")

        return HttpResponseRedirect(path)


class SearchView(ListView):
    model = Tweet
    template_name = "network/all_tweets.html"
    context_object_name = "tweets"
    form_class = NewTweetForm

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if q:
            return Tweet.objects.filter(content__icontains=q)
        
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context