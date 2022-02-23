from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.customlogout, name='logout'),
    path('teams/', views.teams, name='teams'),
    path('team/<int:id>', views.view_team, name='view_team'),
    path('login/', views.customLoginRegister, name='login'),
    path('maketeam/', views.makeTeam, name='maketeam'),
    path('standings/', views.standings, name='standings'),
    path('match/', views.match, name='match'),
]