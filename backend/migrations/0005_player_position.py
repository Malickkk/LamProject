# Generated by Django 4.0.1 on 2022-02-20 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_team_team_group_alter_teamgroup_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(choices=[('GB', 'Gardien de but'), ('DEF', 'Defenseur'), ('MIL', 'Milieu de terrain'), ('ATK', 'Attaquant')], max_length=5, null=True),
        ),
    ]