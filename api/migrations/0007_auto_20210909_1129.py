# Generated by Django 3.2.6 on 2021-09-09 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210909_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarakonesh',
            name='g_Tarikh_Moaser',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tarakonesh',
            name='g_Tarikh_Moaser_Moaref',
            field=models.DateField(blank=True, null=True),
        ),
    ]