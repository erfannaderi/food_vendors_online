# Generated by Django 5.0 on 2024-01-21 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_userprofile_pin_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address2',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
