from django.urls import path

from accounts import views

app_name = "auth"

urlpatterns = [
    path("signup/", views.UserSignUpView.as_view(), name="signup"), # auth:signup
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("<str:username>/", views.UserProfileView.as_view(), name="profile"),
]