# Generated by Django 4.1.3 on 2022-12-04 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='timezone_Shift',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
