# Generated by Django 4.2.5 on 2023-09-18 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_attendance_eid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='timein',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='timeout',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
