# Generated by Django 3.2.6 on 2021-11-27 04:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0047_register_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='upi',
            field=models.IntegerField(default=123456),
            preserve_default=False,
        ),
    ]