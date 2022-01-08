import graphene
import graphql_jwt
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils import timezone
from django.utils.timezone import now
from graphene import String, ID
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import permission_required, user_passes_test
from graphql_jwt.exceptions import PermissionDenied
from graphql_jwt.shortcuts import get_token

from api.OTP import OTP
from api.schema.query import *

# from settings import HAVE_NOT_PERMISSION
HAVE_NOT_PERMISSION = 'you have not permission !!'


class Login(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise PermissionDenied()
        else:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            token = get_token(user)
        return Login(user=user, token=token)


class LoginOTP(graphene.Mutation):
    """
    نام کاربری و کلمه عبور را میگیرد و در صورت صحیح بودن یک پیامک به شماره موبایل کاربر ارسال میکند
    برای تایید پیامک باید نام کاربری و کد ارسال شده از طریق متد ValidateOTP احراز شوند
    """

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        # otp = graphene.String(required=False)

    # user = graphene.Field(UserType)
    # token = graphene.String()
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)
    messages = graphene.List(graphene.String, required=False)

    def mutate(self, info, username, password, ):
        errors = []
        messages = []

        user = authenticate(username=username, password=password)
        if user is None:
            errors.append('نام کاربری یا کله عبور نادرست است.')
        else:
            try:
                phone = user.profile.mobile1
            except:
                errors.append('اشکال در کاربر( احتمالا کاربر شماره موبایل ندارد{mobile1})')

            otp_creator = OTP()
            if otp_creator.generate_otp_code(phone=phone):
                messages.append(' رمز یکبار مصرف 5 رقمی از طریق پیامک برای شما ارسال شد.')
            else:
                messages.append('حداقل فاصله بین ارسال رمز یکبار مصرف ۱۲۰ ثانیه است.')

        if errors:
            return LoginOTP(ok=False, errors=errors)
        else:
            return LoginOTP(ok=True, errors=errors, messages=messages)


class ValidateOTP(graphene.Mutation):
    """
    بررسی کد یکبار رمز ارسال شده توسط کاربر
    """

    class Arguments:
        username = graphene.String(required=True)
        otp = graphene.String(required=True)

    user = graphene.Field(UserType)
    token = graphene.String()
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    def mutate(self, info, username, password, otp=None):
        errors = []

        user = authenticate(username=username, password=password)
        if user is None:
            errors.append('نام کاربری یا کله عبور نادرست است.')
        else:
            try:
                phone = user.profile.mobile1
            except:
                errors.append('اشکال در کاربر')

            otp_creator = OTP()
            if otp_creator.validate_otp_code(phone=phone, code=otp):
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                token = get_token(user)
            else:
                errors.append('کد ارسال شده نادرست است')

        if errors:
            return LoginOTP(ok=False, errors=errors)
        else:
            return LoginOTP(user=user, token=token, ok=True, errors=errors)


class ChangePassword(graphene.Mutation):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)
    token = graphene.String(required=False)

    class Arguments:
        # input_data = ChangePasswordInput(required=True, name="input")
        password1 = String(required=True, description='کلمه عبور جدید')
        password2 = String(required=True, description='تکرار کلمه عبور جدید')
        old_password = String(required=True, description='کلمه عبور قدیمی')

    def mutate(self, info, password1, password2, old_password):
        errors = []
        current_user: User = info.context.user

        if password1 is None:
            errors.append("رمز عبور جدید را وارد کنید")
        if password2 is None:
            errors.append("تکرار رمز عبور را وارد کنید")
        if old_password is None:
            errors.append("رمز عبور قبلی را وارد کنید")
        if password1 != password2:
            errors.append("رمز عبور و تکرار آن یکسان نیستند")
        if password1 == old_password:
            errors.append("رمز جدید نباید مشابه قبلی باشد")

        # چک کردن درستی یوزر پسورد
        user = authenticate(username=current_user.username, password=old_password)

        # if user exists
        if user is not None:
            # اگر یوزر فعال بود
            if user.is_active:
                current_user.set_password(password1)  # تغییر پسورد
                current_user.save()
            else:
                errors.append("کاربر غیر فعال شده است")
        else:
            errors.append("رمز عبور قبلی اشتباه است")

        if errors:
            return ChangePassword(ok=False, errors=errors)
        else:
            # ایجاد توکن
            token = get_token(user)
            return ChangePassword(token=token, ok=True, errors=errors)


class CreateImageInput(graphene.InputObjectType):
    image = Upload(required=True)
    object_id = graphene.Int(required=False, descripion='id چیزی که این تصویر مربوط به آن است')
    model = graphene.String(required=False,
                            description='نام چیزی مه این تصویر مربوط به آن است مانند profile , transaction')
    kind_id = graphene.Int()
    description = graphene.String()


class CreateImagePayload(graphene.ObjectType):
    image = graphene.Field(ImageType, required=True)


class CreateImage(graphene.Mutation):
    """
    افزودن تصویر
    """

    class Arguments:
        input_data = CreateImageInput(required=True, name="input")

    Output = CreateImagePayload

    def mutate(self, info, input_data: CreateImageInput):
        object_id = input_data.object_id
        model = input_data.model
        content_type = ContentType.objects.get(app_label='api', model=model)
        image = input_data.image
        kind_id = input_data.kind_id
        description = input_data.description
        new_image = Image.objects.create(object_id=object_id, content_type=content_type,
                                         image=image, description=description, kind_id=kind_id)

        return CreateImagePayload(new_image)


class UpdateImageInput(CreateImageInput):
    image = Upload(required=False)
    id = graphene.ID(required=True)


class UpdateImagePayload(CreateImageInput):
    pass


# class UpdateImage(graphene.Mutation):
#     class Arguments:
#         input_data = UpdateImageInput(required=True, name="input")


class CreateTransactionInput(graphene.InputObjectType):
    """
        ورودی های لازم برای ایجاد تراکنش
    """
    profile_id = graphene.Int(required=True, description='کاربر تراکنش')
    effective_date = graphene.Date(required=True, description='تاریخ موثر')
    expire_date = graphene.Date(required=False, description='تاریخ انقضا')
    amount = graphene.Float(required=True, description='مبلغ')
    kind_id = graphene.Int(required=True, description='id نوع تراکنش')
    description = String(description='توضیحات')
    alias = String(description='نام دیگر')
    receipt_number = String(description='شماره پیگیری')
    contract_term = String(required=False, description='مدت قرارداد')
    plan_id = graphene.Int(required=True, description='کد طرح')
    images = graphene.List(CreateImageInput, required=False, description='پیوست ها')


class CreateTransactionPayload(graphene.ObjectType):
    transaction = graphene.Field(TransactionType, required=True)


class CreateTransaction(graphene.Mutation):
    """
    ایجاد تراکنش
    """

    class Arguments:
        input_data = CreateTransactionInput(required=True, name="input")

    Output = CreateTransactionPayload

    @login_required
    def mutate(self, info, input_data: CreateTransactionInput):
        current_user: User = info.context.user
        profile = Profile.objects.get(id=input_data.profile_id)
        if not current_user.has_perm('api.add_transaction_for_all'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            if current_user != profile.user:
                raise Exception('عدم دسترسی, دسترسی لازم: (ایجاد تراکنش برای دیگران)add_transaction_for_all ')
        # tr = Transaction.objects.create(profile=profile, amount=input_data.amount,
        #                                 effective_date=input_data.effective_date,
        #                                 kind_id=input_data.kind_id, description=input_data.description,
        #                                 created_by=current_user, date_time=now(), percent=0)

        # input_dict = input_data.__dict__
        # img = input_data.images
        # # input_dict.__delitem__('images')
        # tr = Transaction.objects.create(**input_dict, percent=0, date_time=now(), created_by=current_user)  #
        new_transaction: Transaction = Transaction()
        for k, v in input_data.items():
            if k != 'images':
                setattr(new_transaction, k, v)

        # محاسبه زمان پایان قرارداد بر اساس طرح انتخاب شده
        selected_paln = Plan.objects.get(id=input_data.plan_id)
        new_transaction.expire_date = input_data.effective_date + relativedelta(months=selected_paln.duration)
        new_transaction.contract_term = selected_paln.duration

        new_transaction.date_time = now()
        new_transaction.created_by = current_user
        # محاسبه درصد سود بر اساس مجموع واریزی های قبلی و مبلغ این واریزی و طرح انتخاب شده
        new_transaction.percent = new_transaction.percent_calculator()

        new_transaction.save()
        if input_data.images:
            transaction_type = ContentType.objects.get(app_label='api', model='transaction')
            for img in input_data.images:
                img: CreateImageInput = img
                Image.objects.create(object_id=new_transaction.id, content_type=transaction_type,
                                     image=img.image, description=img.description, kind_id=img.kind_id)

        if current_user.has_perm('api.WF_TRANSITION_TRANSACTION_START_TO_STUFF_ADDED'):
            new_transaction.to_stuff_add(by=current_user, description=input_data.description)
        elif current_user.has_perm('api.WF_TRANSITION_TRANSACTION_START_TO_CUSTOMER_ADDED'):
            new_transaction.to_customer_add(by=current_user, description=input_data.description)

        new_transaction.save()
        return CreateTransactionPayload(transaction=new_transaction)


class UpdateTransactionInput(graphene.InputObjectType):
    """
    مبلغ را نمیتوان به روز کرد
    """
    id = graphene.ID(required=True)

    profile_id = graphene.Int(required=True, description='کاربر تراکنش')
    effective_date = graphene.Date(required=True, description='تاریخ موثر')
    # amount = graphene.Int(required=True, description='مبلغ')
    kind_id = graphene.Int(required=True, description='id نوع تراکنش')
    description = String(description='توضیحات')


class UpdateTransactionPayload(CreateTransactionPayload):
    pass


class UpdateTransaction(graphene.Mutation):
    class Arguments:
        input_data = UpdateTransactionInput(required=True, name="input")

    Output = UpdateTransactionPayload

    def mutate(self, info, input_data: UpdateTransactionInput):
        current_user: User = info.context.user
        profile = Profile.objects.get(id=input_data.profile_id)
        if not current_user.has_perm('api.add_transaction_for_all'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            if profile.user != current_user:
                raise MyException(HAVE_NOT_PERMISSION)
            profile = Profile.objects.get(user=current_user)
        transaction = Transaction.objects.get(id=input_data.id, profile=profile)
        transaction.profile = profile
        transaction.effective_date = input_data.effective_date
        transaction.kind_id = input_data.kind_id
        transaction.description = input_data.description
        transaction.modified_by = current_user
        transaction.modified = now()
        transaction.save()

        return UpdateTransactionPayload(transaction=transaction)


class CreateTransactionRequestImput(graphene.InputObjectType):
    transaction_id = Int(required=True)
    kind_id = graphene.Int(required=True)
    description = String()
    images = graphene.List(CreateImageInput, required=False, )


class CreateTransactionRequest(graphene.Mutation):
    class Arguments:
        input_data = CreateTransactionRequestImput(required=True, name="input")

    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)
    transaction_request = graphene.Field(type=TransactionRequestType)

    @login_required
    def mutate(self, info, input_data: CreateTransactionRequestImput):
        transaction_id = input_data.transaction_id
        kind_id = input_data.kind_id
        description = input_data.description
        images = input_data.images
        errors = []
        current_user: User = info.context.user
        try:
            tr = Transaction.objects.get(id=transaction_id)
        except ObjectDoesNotExist:
            errors.append('transaction dos not exist')
            return CreateTransactionRequest(ok=False, errors=errors)
        if not current_user.has_perm("api.add_TransactionRequests_for_others") and tr.profile.user != current_user:
            raise Exception(
                'عدم دسترسی, دسترسی لازم: (ایجاد درخواست مربوط به تراکنش برای دیگران)add_TransactionRequests_for_others')

        new_tr = TransactionRequest.objects.create(transaction_id=transaction_id, kind_id=kind_id,
                                                   description=description)

        if images:
            tr_type = ContentType.objects.get(app_label='api', model='transactionrequest')
            for img in images:
                img: CreateImageInput = img
                Image.objects.create(object_id=new_tr.id, content_type=tr_type,
                                     image=img.image, description=img.description, kind_id=img.kind_id)

        new_tr.to_customer_add(by=current_user, description=description)

        new_tr.save()
        if errors:
            return CreateTransactionRequest(ok=False, errors=errors)
        else:
            return CreateTransactionRequest(ok=True, errors=errors, transaction_request=new_tr)


class UserInput(graphene.InputObjectType):
    id = ID()
    username = String(required=True)
    password = String(required=True)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        input = UserInput(required=True)

    def mutate(self, info, input):
        try:
            new_user: User = User(username=input.username)
            new_user.set_password(input.password)
            new_user.save()
            new_user.last_login = timezone.now()
            new_user.save(update_fields=['last_login'])
            token = get_token(new_user)
            customer_group_name = 'customer_group'
            customer_group: Group = Group.objects.get(name=customer_group_name)
            customer_group.user_set.add(new_user)
        except IntegrityError as e:
            raise MyException('نام کاربری تکراری است')

        return CreateUser(user=new_user, token=token)


class CreateProfileInput(graphene.InputObjectType):
    # id = graphene.ID()
    user_id = Int(required=True, description='کاربر متناظر')
    # user = UserInput(required=True).Field()
    first_name = String()
    last_name = String()
    father_name = String()
    birth_place_id = Int(required=False, )
    national_code = String()
    id_number = String()
    birth_date = String()
    account_number = String()
    sheba = String()
    card_number = String()
    bank_id = Int(required=False, )

    address = String()
    city_id = Int(required=False, )
    postal_code = String()

    tel = String()
    home_phone = String()
    office_phone = String()
    mobile1 = String()
    mobile2 = String()
    email = String()
    images = graphene.List(CreateImageInput, required=False, )
    description = String()

    # file = Upload(required=True)


class CreateProfilePayload(graphene.ObjectType):
    profile = graphene.Field(ProfileType, required=True)


class CreateProfile(graphene.Mutation):
    """
    نام کاربری و کلمه عبور معرفی شده برای ساخت کاربر جدید و اتصال آن به پروفایل درحال ساخت استفاده میشود
    """

    class Arguments:
        input_data = CreateProfileInput(required=True, name="input")

    Output = CreateProfilePayload

    @login_required
    def mutate(self, info, input_data: CreateProfileInput):
        current_user: User = info.context.user
        new_profile: Profile = Profile()
        if (not current_user.has_perm('api.can_add_profile_for_all')) and input_data.user_id != current_user.id:
            # درخواست کاربر برای ایجاد پروفایل برای دیگری در حالی که دسترسی این کار راندارد
            raise Exception('عدم دسترسی, دسترسی لازم: (ایجاد پروفایل برای دیگران)can_add_profile_for_all ')
        # حلقه برای ست کردن مقادیر به جز مقادیر خاص که لازم است کنترل شوند

        for k, v in input_data.items():
            if k == 'presenter_id':
                try:
                    presenter: Profile = Profile.objects.get(id=input_data.presenter_id)
                    # new_profile.presenter = presenter
                except Profile.DoesNotExist:
                    raise MyException('معرف پیدا نشد')
            elif k == 'images':
                continue
            # elif k == 'city':
            #     setattr(new_profile, 'city_id', v)
            #     continue

            setattr(new_profile, k, v)

        # new_profile.save()
        try:
            new_profile.save()
        except:  # خطا در ثبت پروفایل
            raise MyException('خطایی در ثبت پروفایل رخ داده')

        if input_data.images:
            profile_type = ContentType.objects.get(app_label='api', model='profile')
            for img in input_data.images:
                img: CreateImageInput = img
                Image.objects.create(object_id=new_profile.id, content_type=profile_type,
                                     image=img.image, description=img.description, kind_id=img.kind_id)

        if current_user.has_perm('api.WF_TRANSITION_PROFILE_START_TO_STUFF_ADDED'):
            new_profile.to_stuff_add(by=current_user, description=input_data.description)
        elif current_user.has_perm('api.WF_TRANSITION_PROFILE_START_TO_CUSTOMER_ADDED'):
            new_profile.to_customer_add(by=current_user, description=input_data.description)

        new_profile.save()

        return CreateProfilePayload(profile=new_profile)


class UpdateProfileInput(CreateProfileInput):
    id = graphene.ID(required=True)
    user = UserInput(required=False).Field()  # در به روزرسانی کابر اجباری نیست
    images = graphene.List(UpdateImageInput)


class UpdateProfilePayload(CreateProfilePayload):
    pass


class UpdateProfile(graphene.Mutation):
    """
    بنابه دلایلی از اینجا نام کاربری و کلمه عبور را نمیتوان تغییر داد
    """

    class Arguments:
        input_data = UpdateProfileInput(required=True, name="input")

    Output = UpdateProfilePayload

    @login_required
    def mutate(self, info, input_data: UpdateProfileInput):
        current_user: User = info.context.user
        if not current_user.has_perm('api.can_edit_profile_for_all'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            new_profile = Profile.objects.get(user=current_user)
        else:
            try:
                new_profile: Profile = Profile.objects.get(id=input_data.id)
            except Profile.DoesNotExist:
                raise MyException('پروفایل وچود ندارد')

        # حلقه برای ست کردن مقادیر به جز مقادیر خاص که لازم است کنترل شوند
        for k, v in input_data.items():
            if k == 'user':
                try:
                    new_user: User = User.objects.get(username=new_profile.user)
                    # new_user.username = input_data.user.username
                    # new_user.set_password(raw_password=input_data.user.password)
                    # new_user.save()
                    # new_profile.user = new_user
                except IntegrityError as e:
                    raise MyException('نام کاربری تکراری است')
                except User.DoesNotExist:
                    raise MyException('کاربر وجود ندارد')
                continue
            if k == 'presenter_id':
                try:
                    presenter: Profile = Profile.objects.get(id=input_data.presenter_id)
                    # new_profile.presenter=presenter
                except Profile.DoesNotExist:
                    raise MyException('معرف پیدا نشد')
            if k == 'images':
                for img in input_data.images:
                    new_img = Image.objects.get_or_create(id=img.id, object_id=new_profile.id, content_type_id=4)[0]
                    for ki, vi in img.items():
                        setattr(new_img, ki, vi)
                    new_img.save()

                continue
            setattr(new_profile, k, v)

        # new_user.save()
        if new_profile.state == "START" and current_user.has_perm("api.WF_STUFF_ROLE"):
            new_profile.to_stuff_add(by=current_user)
        new_profile.save()
        return UpdateProfilePayload(profile=new_profile)


class ConfirmInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    confirmed = graphene.Boolean(required=True, description='درصورت تایید true در غیرآن false')
    description = graphene.String(required=False, description='توضیحات')


class ConfirmPayload(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)


class StuffConfirmProfile(graphene.Mutation):
    """
    تایید کابران ثبت نام کرده
    """
    # Output = ConfirmPayload
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    class Arguments:
        input_data = ConfirmInput(required=True, name="input")

    # @permission_required('WF_STUFF_ROLE')
    def mutate(self, info, input_data: ConfirmInput):
        errors = []
        current_user: User = info.context.user
        try:
            profile: Profile = Profile.objects.get(id=input_data.id)

            if input_data.confirmed:
                # کارمند صحت اطاعات را تایید کرد
                profile.to_stuff_confirm(by=current_user, description=input_data.description)
            else:
                # کارمند صحت اطلاعات را تایید نکرد
                profile.to_customer_add(by=current_user, description=input_data.description)
            profile.save()
        except ObjectDoesNotExist:
            errors.append('وجود ندارد')
        if errors:
            return StuffConfirmProfile(ok=False, errors=errors)
        else:
            return StuffConfirmProfile(ok=True, errors=errors)


class CustomerConfirmProfile(graphene.Mutation):
    """
    تایید اطلاعات مشتری که توسط کارمند ثبت شده اند توسط مشتری
    """
    Output = ConfirmPayload

    class Arguments:
        input_data = ConfirmInput(required=True, name="input")

    def mutate(self, info, input_data: ConfirmInput):
        errors = []
        current_user: User = info.context.user

        try:
            profile: Profile = Profile.objects.get(input_data.id)
            if not profile.user == current_user:
                errors.append('عدم دسترسی')
            if input_data.confirmed:
                # مشتری صحت اطلاعات را تایید کرد
                profile.to_customer_confirm(by=current_user, description=input_data.description)
            else:
                # مشتری صحت اطلاعات را تایید نکرد برگشت به کارمند
                profile.to_stuff_add(by=current_user, description=input_data.description)
            profile.save()

        except ObjectDoesNotExist:
            errors.append('وجود ندارد')
        if errors:
            return CustomerConfirmProfile(ok=False, errors=errors)
        else:
            return CustomerConfirmProfile(ok=True, errors=errors)


class ProfileWorkFlowTransition(graphene.Mutation):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    class Arguments:
        id = graphene.Int(required=True)
        transition = graphene.String(required=True, description='transition')
        description = graphene.String(required=False, description='description')

    # @permission_required('WF_STUFF_ROLE')
    def mutate(self, info, id, transition, description):
        errors = []
        current_user: User = info.context.user
        profile: Profile = Profile.objects.get(id=id)

        if not current_user.has_perm("api.can_change_profile_wf_state_for_all"):
            # عدم دسترسی به تغییر مرحله گردش کار برای دیگران
            if profile != current_user.profile:
                # errors.append("perm: (api.can_change_wf_state_for_all)  - عدم دسترسی برای تغییر گردش کار دیگران")
                # return ProfileWorkFlowTransition(ok=False, errors=errors)
                raise Exception(
                    "perm: (api.can_change_profile_wf_state_for_all)  - عدم دسترسی برای تغییر گردش کار پروفایل دیگران")

        avail_user_trans = list(profile.get_available_user_state_transitions(user=current_user))
        attr = list(o.name for o in avail_user_trans)
        if transition in attr:
            getattr(profile, transition)(by=current_user, description=description)
            profile.save()
        else:
            errors.append(f'transition error permission denied for {transition} .')

        if errors:
            return ProfileWorkFlowTransition(ok=False, errors=errors)
        else:
            return ProfileWorkFlowTransition(ok=True, errors=errors)


class TransactionWorkFlowTransition(graphene.Mutation):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    class Arguments:
        id = graphene.Int(required=True)
        transition = graphene.String(required=True, description='transition')
        description = graphene.String(required=False, description='description')

    # @permission_required('WF_STUFF_ROLE')
    def mutate(self, info, id, transition, description):
        errors = []
        current_user: User = info.context.user
        transaction: Transaction = Transaction.objects.get(id=id)

        if not current_user.has_perm("api.can_change_transaction_wf_state_for_all"):
            # عدم دسترسی به تغییر مرحله گردش کار برای دیگران
            if transaction.profile != current_user.profile:
                # errors.append("perm: (api.can_change_wf_state_for_all)  - عدم دسترسی برای تغییر گردش کار دیگران")
                # return ProfileWorkFlowTransition(ok=False, errors=errors)
                raise Exception(
                    "perm: (api.can_change_wf_transactionـstate_for_all)- عدم دسترسی برای تغییر گردش کار تراکنش دیگران")

        avail_user_trans = list(transaction.get_available_user_state_transitions(user=current_user))
        attr = list(o.name for o in avail_user_trans)
        if transition in attr:
            getattr(transaction, transition)(by=current_user, description=description)
            transaction.save()
        else:
            errors.append('transition ثrror')

        if errors:
            return TransactionWorkFlowTransition(ok=False, errors=errors)
        else:
            return TransactionWorkFlowTransition(ok=True, errors=errors)


class CreatePlanInput(graphene.InputObjectType):
    title = String(required=True, description='توضیحات')
    start_date = graphene.Date(required=False)
    end_date = graphene.Date(required=False)
    duration = graphene.Int(required=True, default=6, description='مدت زمان قرارداد بر اساس ماه')
    description = String(description='توضیحات')
    every_n_months = graphene.Int(required=True, default=1, description='پرداخت سود هر چند ماه یکبار')
    max_amount = graphene.Float(required=False,
                                description='سقف جذب یعنی حداکثر مبلغی که شرکت مایل است در این طرح جذب شود')
    min_point = graphene.Float(required=False, description='نقطه فرآخوان')
    visible_for = graphene.List(of_type=Int, description=' id گروه هایی که میتوانند طرح را ببینند')
    aggregate = graphene.Boolean(description='آیا تجمعی است؟')


class CreatePlanPayload(graphene.ObjectType):
    plan = graphene.Field(PlanType, required=True)
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=False)


class CreatePlan(graphene.Mutation):
    class Arguments:
        input_data = CreatePlanInput(required=True, name="input")

    Output = CreatePlanPayload

    @permission_required('api.can_add_plan')
    def mutate(self, info, input_data: CreatePlanInput):
        errors = []
        try:
            input_dict = input_data.__dict__
            vis_for = input_dict.pop('visible_for', None)
            new_plan = Plan.objects.create(**input_dict)

            if vis_for is not None:
                groups = Group.objects.filter(id__in=vis_for)
                new_plan.visible_for.set(groups)

        except MyException as e:
            errors.append(e)
        if errors:
            return CreatePlanPayload(ok=False, errors=errors)
        else:
            return CreatePlanPayload(ok=True, plan=new_plan)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    login_otp = LoginOTP.Field()
    validate_otp = ValidateOTP.Field()
    change_password = ChangePassword.Field()
    create_transaction = CreateTransaction.Field()
    create_transaction_request = CreateTransactionRequest.Field()
    update_transaction = UpdateTransaction.Field()
    create_user = CreateUser.Field(description='ایجاد کاربر')
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()
    create_image = CreateImage.Field()
    stuff_confirm_profile = StuffConfirmProfile.Field(description='')
    profile_workflow_transition = ProfileWorkFlowTransition.Field(description='مرحله بعد در گردش کار پروفایل')
    transaction_workflow_transition = TransactionWorkFlowTransition.Field(description='مرحله بعد در گردش کار تراکنش')
    create_plan = CreatePlan.Field(description='ایجاد طرح')
    # create_tarakonesh = CreateTarakonesh.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    delete_token = graphql_jwt.Revoke.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
