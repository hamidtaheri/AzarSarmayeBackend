# Generated by Django 3.2.7 on 2021-10-03 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_profileimagekind_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='last_name',
            new_name='family_name',
        ),
    ]
