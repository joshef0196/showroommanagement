# Generated by Django 2.0.3 on 2019-11-29 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0010_auto_20191130_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='domain_url',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
