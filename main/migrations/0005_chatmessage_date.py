# Generated by Django 3.1.4 on 2021-03-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210321_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='date',
            field=models.DateField(null=True),
        ),
    ]