# Generated by Django 3.2.8 on 2021-10-07 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_status_account_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneytransfer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='status',
            name='user',
        ),
    ]