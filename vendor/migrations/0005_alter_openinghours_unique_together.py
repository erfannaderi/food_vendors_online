# Generated by Django 5.0 on 2024-01-24 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_openinghours'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='openinghours',
            unique_together={('vendor', 'day', 'from_hours', 'to_hours')},
        ),
    ]