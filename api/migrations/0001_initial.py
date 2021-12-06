# Generated by Django 3.2.9 on 2021-12-04 15:24

import api.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(blank=True, help_text='شماره موبایل', max_length=11, null=True, verbose_name='تلفن همراه')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ImageKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['phone'],
            },
        ),
        migrations.CreateModel(
            name='PelekanKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('national_code', models.CharField(blank=True, max_length=10, null=True)),
                ('shomare_kart', models.CharField(blank=True, max_length=100, null=True)),
                ('account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('percent', models.IntegerField(blank=True, null=True)),
                ('presenter_percent', models.IntegerField(blank=True, null=True)),
                ('get_profit', models.BooleanField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('charge_to_presenter', models.BooleanField(blank=True, null=True)),
                ('self_presenter', models.BooleanField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile1', models.CharField(blank=True, max_length=11, null=True)),
                ('mobile2', models.CharField(blank=True, max_length=11, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('presenter_2', models.IntegerField(blank=True, null=True)),
                ('presenter_percent_2', models.IntegerField(blank=True, null=True)),
                ('self_presenter_2', models.BooleanField(blank=True, null=True)),
                ('two_step_verification', models.BooleanField(default=False, verbose_name='ورود دو مرحله ای با استفاده از پیامک')),
                ('state', django_fsm.FSMField(choices=[('start', 'start'), ('converted', 'converted'), ('staff_added', 'staff_added'), ('customer_added', 'customer_added'), ('stuff_checked', 'stuff_checked'), ('stuff_confirmed', 'stuff_confirmed'), ('customer_confirmed', 'customer_confirmed'), ('boss_confirmed', 'boss_confirmed')], default='START', max_length=50, verbose_name='مرحله در گردش کار')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.city')),
                ('presenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moarefi_shode_ha', to='api.profile', verbose_name='معرف')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل',
                'permissions': (('can_add_profile', 'ایجاد پروفایل'), ('view_all_profiles', ' مشاهده همه پروفایل ها'), ('can_edit_profile_for_self', 'ویرایش پروفایل خودش'), ('can_edit_profile_for_all', 'ویرایش پروفایل دیگران'), ('can_delete_profile_for_all', 'حذف پروفایل')),
            },
        ),
        migrations.CreateModel(
            name='ProfitKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='نوع تراکنش')),
                ('description', models.TextField(verbose_name='توضیح')),
            ],
        ),
        migrations.CreateModel(
            name='WorkFlowStates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'مراحل گردش کار',
                'verbose_name_plural': 'مراحل گردش کار',
                'permissions': (('WF_STUFF_ROLE', 'نقش کارمند در گردش کار'), ('WF_CUSTOMER_ROLE', 'نقش مشتری در گردش کار'), ('WF_BOSS_RULE', 'نقش مدیر عامل در گردش کار')),
            },
        ),
        migrations.CreateModel(
            name='Transaction_old',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='تاریخ')),
                ('amount', models.PositiveBigIntegerField(verbose_name='مبلغ')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transactionkind', verbose_name='نوع')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'عملیات مالی(واریز/برداشت)',
                'verbose_name_plural': 'عملیات مالی(واریز/برداشت)',
                'permissions': (('can_add_transaction_for_self', 'میتواند برای خودش تراکنش ثبت کند'), ('can_add_transaction_for_all', 'میتواند برای دیگران تراکنش ثبت کند'), ('can_view_transaction_for_all', 'میتواند تراکنش دیگران را مشاهده کند')),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarikh', models.CharField(max_length=10)),
                ('date', models.DateField(blank=True, null=True)),
                ('Tarikh_Moaser', models.CharField(max_length=10)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='تاریخ انتهای قرارداد')),
                ('Tarikh_Moaser_Moaref', models.CharField(max_length=10)),
                ('presenter_effective_date', models.DateField(blank=True, null=True)),
                ('date_time', models.DateTimeField()),
                ('amount', models.BigIntegerField()),
                ('NahveyePardakht', models.CharField(blank=True, max_length=40, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('Tbl_Pardakht_List_id', models.IntegerField(blank=True, null=True)),
                ('percent', models.IntegerField()),
                ('DarMelyoon_Moaref', models.IntegerField(blank=True, null=True)),
                ('state', django_fsm.FSMField(choices=[('start', 'start'), ('converted', 'converted'), ('staff_added', 'staff_added'), ('customer_added', 'customer_added'), ('stuff_checked', 'stuff_checked'), ('stuff_confirmed', 'stuff_confirmed'), ('customer_confirmed', 'customer_confirmed'), ('boss_confirmed', 'boss_confirmed')], max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions_create_by', to=settings.AUTH_USER_MODEL)),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.transactionkind')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions_modified_by', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.profile')),
            ],
            options={
                'ordering': ['effective_date'],
                'permissions': (('view_all_transactions', 'مشاهده همه تراکنش ها '), ('add_transaction_for_all', 'میتواند برای دیگران تراکنش ثبت کند')),
            },
        ),
        migrations.CreateModel(
            name='ProfitCalculate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(verbose_name='از تاریخ')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='تا تاریخ')),
                ('days', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد روز')),
                ('amount', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='مبلغ')),
                ('percent', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='درصد')),
                ('calculated_amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='مبلغ سود محاسبه شده')),
                ('balance', models.BooleanField(default=False, verbose_name='تسویه شده است')),
                ('description', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profiteCalculates', to='api.profile')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.profitkind')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ProfitCalculates', to='api.transaction', verbose_name='تراکنش متناظر')),
                ('transaction_balance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ProfitCalculate', to='api.transaction', verbose_name='تسویه شده با تراکنش')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ProfileImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_kind', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.imagekind')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_images', to='api.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.province'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('body', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('is_public', models.BooleanField(default=True, verbose_name='عمومی؟')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pelekan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('az', models.PositiveBigIntegerField()),
                ('ta', models.PositiveBigIntegerField()),
                ('percent', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('kind', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='kinds', to='api.pelekankind')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(upload_to=api.models.get_storage_path)),
                ('object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='image_create_by', to=settings.AUTH_USER_MODEL)),
                ('kind', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.imagekind')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='image_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصویر ها',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.province'),
        ),
    ]
