# Generated by Django 3.1.4 on 2021-10-28 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_auto_20211028_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneytransfer',
            name='receiver_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
