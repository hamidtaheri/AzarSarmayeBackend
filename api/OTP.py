import api.models
from api.models import OtpCode
from api.SMS import SMS
from random import randint
from datetime import datetime
from django.utils import timezone


class OTP:
    def generate_otp_code(self, phone):
        # check time is more than 120s or not
        def check_time_diff():
            # get now time with time zone
            # now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            now = timezone.now()
            # cal different time
            time_diff = now - user_otp.created
            # check if time passed more than 1 day
            if time_diff.days > 0:
                # print('time_diff', time_diff.total_seconds())
                return True
            else:
                # check if time is passed more than 60s
                if time_diff.total_seconds() > 120:
                    return True
                else:
                    return False

        try:
            # get previous user otp code if exist
            user_otp = OtpCode.objects.get(phone=phone)
            print()
        except:
            # if user havent any otp code
            user_otp = None
        code = randint(10000, 99999)

        sms = SMS()

        # if user had any otp code previous
        if user_otp is not None:
            # check if previous code generated more than 120s ago
            if check_time_diff():
                # replace generated code in otp object that previous created
                user_otp.code = code
                # send code by message to user
                # send = SMS.send_otp(phone=phone, otp_code=code)
                send = sms.send_otp(phone=phone, otp_code=code)

                # print(send)

                # get now time 
                creationDate = datetime.now()
                creationDate = timezone.now()  # get now time zone
                # replace now time in created field in user_otp
                user_otp.created = creationDate
                # user_otp.created = datetime(2013, 11, 20, 20, 9, 26, 423063)
                # save user_otp object
                user_otp.save()
                return True

            else:
                return False

        else:

            OtpCode.objects.create(phone=phone, code=code, is_verified=False)
            # send code by message to user
            # send = SMS_request.send_sms(phone, code)
            send = sms.send_otp(phone=phone, otp_code=code)
            # print(send)
            return True

    # validate input otp code 
    def validate_otp_code(self, phone, code):
        def check_time():
            # get now time with time zone
            # now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            now = timezone.now()
            # cal diffrent time 
            timediff = now - otp.created
            # check if time passed more than 1 day
            if timediff.days > 0:
                # print('timediff', timediff.total_seconds())
                return False
            else:
                # check if time is passed more than 60s
                if timediff.total_seconds() > 120:
                    return False
                else:
                    return True

        # get genrated code
        try:
            otp = OtpCode.objects.get(phone=phone)
        except:
            return False

        if check_time():
            if code == otp.code:
                otp.is_verified = True
                otp.save()
                return True
            else:
                return False
        else:
            return False
        # print("generated2", otp.code)

    # validate input otp code
    def verify_otp_code(self, phone, code):
        def check_time():
            # get now time with time zone
            # now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            now = timezone.now()
            # cal diffrent time 
            timediff = now - otp.created
            # check if time passed more than 1 day
            if timediff.days > 0:
                # print('timediff', timediff.total_seconds())
                return False
            else:
                # check if time is passed more than 60s
                if timediff.total_seconds() > 300:
                    return False
                else:
                    return True

        # get genrated code
        try:
            otp = OtpCode.objects.get(phone=phone)
        except:
            return False

        if check_time():
            if code == otp.code and otp.is_verified == True:
                return True
            else:
                return False
        else:
            return False
