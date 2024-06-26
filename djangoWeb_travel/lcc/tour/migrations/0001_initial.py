# Generated by Django 4.2.7 on 2023-11-29 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('depDate', models.CharField(max_length=30)),
                ('img', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('createDate', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tours',
            },
        ),
    ]
