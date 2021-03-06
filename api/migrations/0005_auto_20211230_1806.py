# Generated by Django 3.2.9 on 2021-12-30 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_profile_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={'permissions': (('view_all_plans_active', 'مشاهده همه طرح ها [فعال و غیر فعال]'), ('view_all_plans_date', 'مشاهده همه طرح ها [در بازه و خارج از بازه]'))},
        ),
        migrations.AddField(
            model_name='plan',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
