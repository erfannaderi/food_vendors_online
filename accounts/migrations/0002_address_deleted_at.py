# Generated by Django 5.0 on 2024-02-01 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
