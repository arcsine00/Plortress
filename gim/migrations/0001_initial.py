# Generated by Django 4.2 on 2023-04-09 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speech', models.CharField(max_length=20)),
                ('bpm', models.IntegerField()),
                ('beats', models.IntegerField()),
            ],
        ),
    ]
