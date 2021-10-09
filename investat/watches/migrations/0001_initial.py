# Generated by Django 3.2.7 on 2021-10-08 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='etf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_time', models.DateTimeField()),
                ('ticker', models.CharField(max_length=20)),
                ('tr_ytd', models.FloatField(default=0)),
                ('tr_1m', models.FloatField(default=0)),
                ('tr_3m', models.FloatField(default=0)),
                ('tr_1y', models.FloatField(default=0)),
                ('tr_3y', models.FloatField(default=0)),
                ('tr_5y', models.FloatField(default=0)),
                ('tr_10y', models.FloatField(default=0)),
                ('tr_lbull', models.FloatField(default=0)),
                ('tr_lbear', models.FloatField(default=0)),
                ('tr_ytd_c', models.FloatField(default=0)),
                ('tr_1m_c', models.FloatField(default=0)),
                ('tr_3m_c', models.FloatField(default=0)),
                ('tr_1y_c', models.FloatField(default=0)),
                ('tr_3y_c', models.FloatField(default=0)),
                ('tr_5y_c', models.FloatField(default=0)),
                ('tr_10y_c', models.FloatField(default=0)),
                ('tr_lbull_c', models.FloatField(default=0)),
                ('tr_lbear_c', models.FloatField(default=0)),
            ],
        ),
    ]
