from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
import json


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


def home(request):
    return render(request, 'home.html')

@csrf_exempt
# def login_user(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     # stayloggedin = request.GET.get('stayloggedin')
#     # if stayloggedin == "true":
#     #  pass
#     # else:
#     #  request.session.set_expiry(0)
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
#         else:
#             return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
#     else:
#         return HttpResponse(json.dumps({"message": "invalid"}), content_type="application/json")
#     # return HttpResponse(json.dumps({"message": "denied"}), content_type="application/json")
def login_user(request):

        # گرفتن نام کاربری
        if 'username' in request.POST:
            username = request.POST.get('username')
        else:
            response_data = ({
                "detail": "لطفا نام کاربری را وارد کنید",
                "isSuccess": False
            })
            data_status = 200
            return HttpResponse(json.dumps(response_data), status=data_status)

            # گرفتن رمز عبور
        if 'password' in request.POST:
            password = request.POST.get('password')

        else:
            response_data = ({
                "detail": "لطفا رمز عبور را وارد کنید",
                "isSuccess": False
            })
            data_status = 200
            return HttpResponse(json.dumps(response_data), status=data_status)

            # چک کردن درستی یوزر پسورد
        user = authenticate(username=username, password=password)

        # if user exists
        if user is not None:
            # دریافت توکن از دیتابیس
            token, created = Token.objects.get_or_create(user=user)
            # اگر ادمین بود
            if user.type > 1:
                # اگر بار اول بود که لاگین می کرد
                if user.step == 0:
                    user.step = 1
                    user.save()

                # اگر بعد از اولین لاگین رمز خود را تغییر نداده بود
                if user.step != 2:
                    response_data = ({
                        "detail": "لطفا رمز ورود را تغییر دهید",
                        "key": token.key,
                        "step": user.step,
                        "isSuccess": True
                    })
                    data_status = status.HTTP_200_OK
                    return Response(response_data, status=data_status)

                serializer = serializers.UserSerializer(user, context={'request': request})
                response_data = ({
                    "detail": "به پزشکیتو خوش آمدید",
                    "key": token.key,
                    "results": serializer.data,
                    "isSuccess": True
                })
                data_status = status.HTTP_200_OK
                return Response(response_data, status=data_status)

            else:
                response_data = ({
                    "detail": "شما دسترسی ورود به این بخش را ندارید",
                    "isSuccess": False
                })
                data_status = status.HTTP_200_OK
                return Response(response_data, status=data_status)

        else:
            response_data = ({
                "detail": "نام کاربری یا رمز عبور اشتباه است",
                "isSuccess": False
            })
            data_status = status.HTTP_200_OK
            return Response(response_data, status=data_status)

        # logout