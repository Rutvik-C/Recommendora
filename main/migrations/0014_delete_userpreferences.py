# Generated by Django 3.1.2 on 2021-11-22 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_actor_director_genre_movie_userpreferences'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserPreferences',
        ),
    ]