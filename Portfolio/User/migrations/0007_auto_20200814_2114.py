# Generated by Django 3.1 on 2020-08-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_auto_20200814_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_no',
            field=models.IntegerField(default='000000'),
        ),
    ]
