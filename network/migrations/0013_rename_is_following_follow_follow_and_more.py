# Generated by Django 5.0 on 2023-12-07 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='is_following',
            new_name='follow',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='being_followed',
        ),
    ]
