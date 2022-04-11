# Generated by Django 3.2.12 on 2022-04-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.TextField()),
                ('profile', models.TextField()),
                ('user_id', models.TextField()),
                ('lisk_count', models.IntegerField()),
            ],
        ),
    ]
