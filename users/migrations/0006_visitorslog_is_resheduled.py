# Generated by Django 4.2.5 on 2024-04-23 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_visitorslog_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorslog',
            name='is_resheduled',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]