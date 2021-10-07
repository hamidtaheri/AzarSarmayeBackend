# Generated by Django 3.2.8 on 2021-10-07 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_auto_20211007_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfitKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profitcalculate',
            name='Profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='profiteCalculates', to='api.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profitcalculate',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profitcalculate',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profitcalculate',
            name='kind',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='api.profitkind'),
            preserve_default=False,
        ),
    ]
