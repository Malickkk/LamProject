from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django_countries.fields import CountryField

GROUP_CHOICES = (
    ('A', '1'),
    ('B', '2'),
    ('C', '3'),
    ('D', '4'),
)

POSITION_CHOICES = (
    ('GB', 'Gardien de but'),
    ('DEF', 'Defenseur'),
    ('MIL', 'Milieu de terrain'),
    ('ATK', 'Attaquant')
)
class MyUserManager(BaseUserManager):
    def create_user(self, email,  password=None):

        if not email:
            raise ValueError('Users must have a valid email address')

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            email, 
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Coach(AbstractBaseUser):
    email = models.EmailField('Adresse Courriel', max_length=100, unique=True)
    full_name = models.CharField('Nom complet', max_length=150)
    dob = models.DateField('Date de naissance', default='2000-01-01', null=True)
    country = CountryField('Pays')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['first_name', 'last_name', 'country']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_admin

class Player(models.Model):
    player_name = models.CharField('Nom du Joueur', max_length=200)
    dob = models.DateField('Date de naissance', null=True)
    country = CountryField('Pays')
    position = models.CharField(max_length=5, choices=POSITION_CHOICES, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    added_at = models.DateTimeField('Date de Création', auto_now_add=True)

    def __str__(self):
        return self.player_name


class Team(models.Model):
    country = CountryField('Pays',unique=True)
    team_group = models.CharField(max_length=2, choices=GROUP_CHOICES, null=True)
    match_played = models.IntegerField(default=0, blank=True)
    won = models.IntegerField(default=0, blank=True)
    draw = models.IntegerField(default=0, blank=True)
    lost = models.IntegerField(default=0, blank=True)
    goal_for = models.IntegerField(default=0, blank=True)
    goal_against = models.IntegerField(default=0, blank=True)
    goal_diff = models.IntegerField(default=0, blank=True)
    points = models.IntegerField(default=0, blank=True)
    group_position = models.IntegerField(default=0, blank=True)
    # champion = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.country.name)

    def get_country_code(self):
        return self.country.code
    
    def get_id(self):
        return self.id

    def get_absolute_url(self):
        return reverse('view_team', args=(str(self.id)))
    
    def get_flag(self):
        return self.country.flag


class TeamGroup(models.Model):
    name = models.CharField(max_length=2, choices=GROUP_CHOICES, unique=True)
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return str('Group ' + self.name)

