# Generated by Django 3.2.6 on 2021-08-30 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_ashkhas_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarakonesh',
            name='shakhs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarakoneshha', to='api.ashkhas'),
        ),
    ]
