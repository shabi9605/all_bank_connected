# Generated by Django 3.1.4 on 2021-10-29 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_reminder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='reminder_date',
            field=models.DateTimeField(),
        ),
    ]
