# Generated by Django 4.1 on 2022-09-02 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='photo',
            field=models.ImageField(default='default-avatar.jpg', upload_to=''),
        ),
    ]
