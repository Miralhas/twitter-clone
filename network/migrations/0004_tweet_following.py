# Generated by Django 5.0 on 2023-12-06 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_remove_tweet_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='network.tweet'),
        ),
    ]
