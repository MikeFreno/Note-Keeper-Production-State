# Generated by Django 4.1.3 on 2022-12-05 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authAPI', '0002_user_timezone_shift_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='timezone_Shift',
            field=models.IntegerField(null=True),
        ),
    ]