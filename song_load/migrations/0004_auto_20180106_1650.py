# Generated by Django 2.0 on 2018-01-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song_load', '0003_song_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='song',
            name='image_url',
        ),
    ]
