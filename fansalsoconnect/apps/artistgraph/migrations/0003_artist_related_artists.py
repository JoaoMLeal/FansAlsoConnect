# Generated by Django 3.1.7 on 2021-03-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistgraph', '0002_auto_20210315_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='related_artists',
            field=models.ManyToManyField(related_name='_artist_related_artists_+', to='artistgraph.Artist'),
        ),
    ]
