# Generated by Django 2.2.19 on 2021-03-23 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('image_url', models.CharField(max_length=100)),
                ('index', models.IntegerField()),
                ('related_artists', models.ManyToManyField(related_name='_artist_related_artists_+', to='artistgraph.Artist')),
            ],
        ),
    ]
