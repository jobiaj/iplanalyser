# Generated by Django 3.2.6 on 2021-08-31 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl', 'Iplmodels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='toss_decision',
            field=models.CharField(max_length=100),
        ),
    ]