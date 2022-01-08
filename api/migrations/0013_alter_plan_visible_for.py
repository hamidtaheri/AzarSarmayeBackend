# Generated by Django 3.2.9 on 2022-01-08 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0012_alter_plan_visible_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='visible_for',
            field=models.ManyToManyField(blank=True, to='auth.Group', verbose_name='گروه هایی که میتوانند طرح را ببینند'),
        ),
    ]
