# Generated by Django 4.2.16 on 2024-11-21 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='data_nascimento',
        ),
    ]