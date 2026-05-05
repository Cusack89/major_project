from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q 
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import Injury, Stretch, StretchMapping, SavedStretch, Profile, Routine, RoutineLabel, SavedRoutine
from .forms import InjuryForm

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("my_app/dashboard")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("my_app/dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "my_app/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    latest_injury = Injury.objects.filter(user=request.user).order_by("-created_at").first()
    saved_count = SavedStretch.objects.filter(user=request.user).count()
    injury_count = Injury.objects.filter(user=request.user).count()

    recommended_stretches = Stretch.objects.all()[:3]

    ## simple PLACEHOLDER streak (CHANGE LATER)
    stretch_streak = 0

    return render(request, "my_app/dashboard.html", {
        "latest_injury": latest_injury,
        "saved_count": saved_count,
        "injury_count": injury_count,
        "recommended_stretches": recommended_stretches,
        "stretch_streak": stretch_streak,
    })


@login_required
def injury_form(request):
    if request.method == "POST":
        form = InjuryForm(request.POST)

        if form.is_valid():
            injury = form.save(commit=False)
            injury.user = request.user
            injury.save()
            return redirect(f"/my_app/recommendations/{injury.id}/")
    else:
        form = InjuryForm()

    return render(request, "my_app/injury_form.html", {"form": form})


@login_required
def recommendations(request, injury_id):
    injury = get_object_or_404(Injury, id=injury_id, user=request.user)

    mappings = StretchMapping.objects.filter(
        body_area=injury.body_area,
        pain_type=injury.pain_type
    )

    stretches = [mapping.stretch for mapping in mappings]

    return render(request, "my_app/recommendations.html", {
        "injury": injury,
        "stretches": stretches,
    })


@login_required
def save_stretch(request, stretch_id):
    stretch = get_object_or_404(Stretch, id=stretch_id)

    SavedStretch.objects.get_or_create(
        user=request.user,
        stretch=stretch
    )

    return redirect("my_app/profile")


@login_required
def injury_history(request):
    injuries = Injury.objects.filter(user=request.user).order_by("-date_occurred")

    return render(request, "my_app/injury_history.html", {
        "injuries": injuries,
    })


@login_required
def explore(request):
    selected_filter = request.GET.get("filter")
    search_query = request.GET.get("q")

    labels = RoutineLabel.objects.all().order_by("name")

    routines = Routine.objects.prefetch_related(
        "labels",
        "routinestretch_set__stretch"
    )

    ## SEARCH feature
    if search_query:
        routines = routines.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    ## FILTER feature
    if selected_filter:
        routines = routines.filter(labels__name=selected_filter).distinct()

    return render(request, "my_app/explore.html", {
        "labels": labels,
        "routines": routines,
        "selected_filter": selected_filter,
        "search_query": search_query,
    })


@login_required
def profile(request):
    injuries = Injury.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "my_app/profile.html", {
        "injuries": injuries,
        "health_status": 7,
        "stretch_streak": 0,
        "saved_stretches": [],
    })

@login_required
def settings_view(request):
    return render(request, "my_app/settings.html")

@login_required
def routine_detail(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)

    saved = SavedRoutine.objects.filter(
        user=request.user,
        routine=routine
    ).exists()

    return render(request, "my_app/routine_detail.html", {
        "routine": routine,
        "saved": saved,
    })


@login_required
def toggle_save_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)

    saved_obj, created = SavedRoutine.objects.get_or_create(
        user=request.user,
        routine=routine
    )

    if not created:
        saved_obj.delete()
        saved = False
    else:
        saved = True

    return JsonResponse({"saved": saved})