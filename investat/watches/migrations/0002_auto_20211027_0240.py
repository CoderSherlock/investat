# Generated by Django 3.2.7 on 2021-10-27 06:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('watches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etf',
            name='market_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='etf',
            name='nav_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='etf',
            name='quote_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]