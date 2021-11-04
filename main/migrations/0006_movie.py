# Generated by Django 3.1.2 on 2021-11-04 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_delete_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image_url', models.CharField(max_length=250)),
                ('trailer_link', models.CharField(max_length=50)),
                ('year', models.CharField(max_length=15)),
                ('duration', models.CharField(max_length=20)),
                ('language', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=450)),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('production_company', models.CharField(max_length=150)),
                ('actors', models.ManyToManyField(to='main.Actor')),
                ('directors', models.ManyToManyField(to='main.Director')),
                ('genre', models.ManyToManyField(to='main.Genre')),
            ],
        ),
    ]
