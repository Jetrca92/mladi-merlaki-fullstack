# Generated by Django 5.0.2 on 2024-03-27 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='crypto',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='stocks',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='crypto',
            field=models.ManyToManyField(to='portfolio.cryptoportfolio'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='stocks',
            field=models.ManyToManyField(to='portfolio.stockportfolio'),
        ),
    ]
