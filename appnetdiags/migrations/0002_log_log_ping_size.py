# Generated by Django 4.1.5 on 2023-03-02 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appnetdiags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='log_ping_size',
            field=models.IntegerField(default=0),
        ),
    ]
