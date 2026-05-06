from django.urls import path
from . import views

app_name = "my_app"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard_page"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("injury/new/", views.injury_form, name="injury_form"),
    path("recommendations/<int:injury_id>/", views.recommendations, name="recommendations"),
    path("save-stretch/<int:stretch_id>/", views.save_stretch, name="save_stretch"),

    path("history/", views.injury_history, name="injury_history"),
    path("explore/", views.explore, name="explore"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings_view, name="settings"),

    path("routine/<int:routine_id>/", views.routine_detail, name="routine_detail"),
    path("routine/<int:routine_id>/save/", views.toggle_save_routine, name="toggle_save_routine"),
    ]