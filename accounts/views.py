from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from accounts.forms import AuthForm, RegisterForm
from accounts.models import User

# Create your views here.


class UserLoginView(LoginView):
    form_class = AuthForm
    template_name = "accounts/login.html"

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return reverse(self.next_page)
        else:
            return reverse("network:index")


class UserProfileView(View):
    template_name = "accounts/profile.html"
    context_object_name = "user_profile"

    def get(self, request, username):
        try:
            user_requested = self.kwargs.get("username")
            username = User.objects.get(username=username)
        except User.DoesNotExist:
            username = None
        if request.user.is_authenticated:
            user=request.user
            try:
                request_user_follows = bool(username.followers.filter(user=user))
            except AttributeError:
                request_user_follows = False
        else:
            request_user_follows = False

        page_obj = {}
        if username is not None:
            tweets = username.tweets.all()
            paginator = Paginator(tweets, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

        return render(request, "accounts/profile.html", context={
            "username":username,
            "user_requested": user_requested,
            "request_user_follows": request_user_follows,
            "page_obj": page_obj,
        })


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("network:index"))


class UserSignUpView(View):
    form_class = RegisterForm
    template_name = "accounts/signup.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            while (len(form.errors)) != 1:
                form.errors.popitem()
            return render(request, self.template_name, context={"form": form})
