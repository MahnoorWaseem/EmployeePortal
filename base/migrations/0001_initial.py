# Generated by Django 4.2.5 on 2023-09-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmpInfo',
            fields=[
                ('eid', models.BigAutoField(primary_key=True, serialize=False)),
                ('ename', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=30)),
                ('salary', models.CharField(max_length=30)),
                ('dept', models.CharField(max_length=30)),
                ('pic', models.FileField(upload_to='')),
            ],
            options={
                'db_table': 'empInfo',
            },
        ),
    ]
