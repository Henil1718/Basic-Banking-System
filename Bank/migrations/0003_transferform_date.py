# Generated by Django 3.0.3 on 2021-02-08 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0002_transferform'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferform',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
