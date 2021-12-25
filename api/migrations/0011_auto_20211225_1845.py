# Generated by Django 3.2.9 on 2021-12-25 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20211224_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (('can_add_profile', 'ایجاد پروفایل'), ('view_all_profiles', ' مشاهده همه پروفایل ها'), ('can_edit_profile_for_self', 'ویرایش پروفایل خودش'), ('can_edit_profile_for_all', 'ویرایش پروفایل دیگران'), ('can_delete_profile_for_all', 'حذف پروفایل'), ('can_change_wf_state_for_all', 'میتواند مرحله گردش کار پروفایل را برای دیگران تغییر دهد'), ('WF_TRANSITION_PROFILE_START_TO_CONVERTED', '  گردش کار پروفایل از شروع به کانورت شده'), ('WF_TRANSITION_PROFILE_START_TO_STUFF_ADDED', 'گردش کار پروفایل از شروع به افزوده شده توسط کارمند'), ('WF_TRANSITION_PROFILE_START_TO_CUSTOMER_ADDED', 'گردش کار پروفایل از شروع به افزوده شده توسط مشتری'), ('WF_TRANSITION_PROFILE_CONVERTED_TO_STUFF_ADDED', 'گردش کار پروفایل از کانورت شده به افزوده شده توسط کارمند'), ('WF_TRANSITION_PROFILE_STUFF_ADDED_TO_STUFF_ADDED', 'گردش کار پروفایل از افزوده شده توسط کارمند به افزوده شده توسط کارمند (عدم تایید توسط مشتری)'), ('WF_TRANSITION_PROFILE_STUFF_ADDED_TO_COSTUMER_CONFIRMED', 'گردش کار پروفایل از افزوده شده توسط کارمند به تایید شده توسط مشتری'), ('WF_TRANSITION_PROFILE_COSTUMER_ADDED_TO_COSTUMER_ADDED', 'گردش کار پروفایل افزوده شده توسط مشتری به افزوده شده توسط مشتری(عدم تایید توسط کارمند)'), ('WF_TRANSITION_PROFILE_COSTUMER_ADDED_TO_STUFF_CONFIRMED', 'گردش کار پروفایل از افزوده شده توسط مشتری به تایید توسط کارمند')), 'verbose_name': 'پروفایل', 'verbose_name_plural': 'پروفایل'},
        ),
        migrations.AddField(
            model_name='transaction',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.pelekankind'),
        ),
    ]
