# Generated by Django 4.0.2 on 2022-04-11 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eotyapp', '0004_rename_e_id_user_points_e_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_points',
            name='e_no',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
