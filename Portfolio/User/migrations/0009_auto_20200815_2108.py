# Generated by Django 3.1 on 2020-08-15 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_project_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='description',
            field=models.TextField(null=True),
        ),
    ]