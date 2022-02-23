from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Coach, Player


POSITION_CHOICES = (
    ('GB', 'Gardien de but'),
    ('DEF', 'Defenseur'),
    ('MIL', 'Milieu de terrain'),
    ('ATK', 'Attaquant')
)

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Coach
        fields = [
            'email', 'full_name', 'dob', 'country', 'password1', 'password2'
        ]
        widgets = {
            'dob': DateInput(),
        }
    

class LoginForm(forms.Form):
    email = forms.Field(widget=forms.TextInput(attrs={
        'class': 'form-control, form-control-user',
        'label': 'Adresse courriel',
    }))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control, form-control-user',
        'label': 'Mot de passe',
    }))
    

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = [
            'player_name', 'dob', 'position'
        ]
        widgets = {
            'dob': DateInput(),
        }
    # player_name = forms.CharField(
    #     label='Nom du Joueur', 
    #     max_length=200, 
    # )
    # dob = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # position = forms.ChoiceField(choices=POSITION_CHOICES)

