# Generated by Django 2.0.3 on 2019-11-26 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branches',
            name='user_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
