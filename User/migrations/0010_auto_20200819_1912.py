# Generated by Django 3.1 on 2020-08-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_auto_20200815_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='completion',
            field=models.IntegerField(default='0'),
        ),
    ]