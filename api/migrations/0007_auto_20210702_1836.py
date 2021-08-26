# Generated by Django 3.2.4 on 2021-07-02 18:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210702_1527'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profitcalculate',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='profitcalculate',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]