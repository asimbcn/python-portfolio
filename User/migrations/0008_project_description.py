# Generated by Django 3.1 on 2020-08-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20200814_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
