# Generated by Django 4.0.1 on 2022-02-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='teams',
            field=models.ManyToManyField(to='backend.Team'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(choices=[('0', '-'), ('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D'), ('5', 'E'), ('6', 'F')], max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_group',
            field=models.CharField(choices=[('0', '-'), ('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D'), ('5', 'E'), ('6', 'F')], max_length=2, null=True, unique=True),
        ),
    ]
