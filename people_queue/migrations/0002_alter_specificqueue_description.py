# Generated by Django 5.0.7 on 2024-07-21 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people_queue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specificqueue',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
