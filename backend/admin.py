from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Coach, Team, Player, TeamGroup

myModels = [Coach, Team, Player, TeamGroup]
admin.site.register(myModels)
