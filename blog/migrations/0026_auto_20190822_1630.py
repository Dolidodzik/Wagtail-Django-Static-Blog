# Generated by Django 2.2.3 on 2019-08-22 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_auto_20190822_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='link',
            field=models.URLField(max_length=255),
        ),
    ]