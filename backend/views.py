from django.views.decorators.csrf import csrf_exempt 
from django.contrib import messages 
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.forms import formset_factory
from itertools import combinations
from random import shuffle

from .forms import RegistrationForm, LoginForm, PlayerForm
from .decorators import unauthenticated_user
from .models import Player, Team, TeamGroup


@csrf_exempt
def home(request):
    teams = Team.objects.all().order_by('-points').order_by('-goal_diff').order_by('-goal_for').order_by('-won')
    team_groups = TeamGroup.objects.all()
    matches = matchSetUp()
    context = { 'teams' : teams, 'team_groups' : team_groups, 'matches' : matches}
    return render(request, 'index.html', context)

@csrf_exempt
@login_required
def teams(request):
    teams = Team.objects.all()
    players = Player.objects.all()
    team_groups = TeamGroup.objects.all()
    context = {'teams': teams, 'players': players, 'team_groups' : team_groups }
    return render(request, 'teams.html', context)

@csrf_exempt
@login_required
def view_team(request, id):
    team = Team.objects.filter(id=id) #obtain exact country object selected in a query list
    players = Player.objects.all().filter(country=team[0].get_country_code()).order_by('-position')
    #obtain all players from selected country using the country code which matches DB
    context = {'team': team, 'players': players}
    return render(request, 'view_team.html', context)

@csrf_exempt
@unauthenticated_user # cannot reach the login/register page if already authenticated
def customLoginRegister(request):
    login_form = LoginForm(request.POST)
    register_form = RegistrationForm(request.POST)
    if login_form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
    if register_form.is_valid():
        user = register_form.save()
        auth_login(request, user)
        return redirect('home')
    login_form = LoginForm()
    register_form = RegistrationForm()
    context = {'login_form': login_form, 'register_form': register_form}
    return render(request, 'login.html', context)

@csrf_exempt
@login_required
def makeTeam(request):
    PlayerFormSet = formset_factory(PlayerForm, extra=25)
    formset = PlayerFormSet(request.POST or None)
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
    }
    if formset.is_valid():
        for form in formset:
            player_name = form.cleaned_data.get('player_name')
            dob = form.cleaned_data.get('dob')
            position = form.cleaned_data.get('position')
            if player_name and dob and position:
                team, _ = Team.objects.get_or_create(country=request.user.country)
                _, created = Player.objects.get_or_create(
                    player_name=player_name, 
                    dob=dob,
                    country=request.user.country,
                    position=position,
                    team_id=team.id,
                )
                if created:
                    messages.info(
                        request, 
                        f'{form.cleaned_data["player_name"]} a été ajouté avec succés.'
                    )
                else:
                    messages.info(
                        request, 
                        f'{form.cleaned_data["player_name"]} existe déjà.'
                    )
        return redirect('home')
    form = PlayerForm()
    context = {'formset': formset}
    return render(request, 'makeTeam.html', context)

@csrf_exempt
@login_required
def match(request):
    groups=[]
    for group in TeamGroup.objects.all():
        groups.append(list(group.teams.all()))
    matches=matchSetUp()
    context = {}
    return render(request, 'match.html', context)

@csrf_exempt
@login_required
def standings(request):
    team_groups = TeamGroup.objects.all()
    context = { 'team_groups' : team_groups }
    return render(request, 'standings.html', context)

def customlogout(request):
    logout(request)
    return redirect('home')



# Set up matches function
def matchSetUp():
    groups=[]
    for group in TeamGroup.objects.all():
        groups.append(list(group.teams.all()))
    matches=[]
    for group in groups:
        matches.append([i for i in combinations(group,2)])
 
    return matches