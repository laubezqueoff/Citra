# Generated by Django 3.1.4 on 2021-03-21 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210321_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
    ]
