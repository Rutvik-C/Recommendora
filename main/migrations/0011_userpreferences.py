# Generated by Django 3.1.2 on 2021-11-04 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0010_delete_userpreferences'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('feature_preference', models.TextField()),
                ('actor_preference', models.TextField()),
                ('director_preference', models.TextField()),
                ('studio_preference', models.TextField()),
            ],
        ),
    ]