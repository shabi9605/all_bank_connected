# Generated by Django 3.1.4 on 2021-11-08 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0043_bankaccount_aadhar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
