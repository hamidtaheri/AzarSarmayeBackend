from kavenegar import *


class SMS:
    sms_api = KavenegarAPI('315355594D7236313361746D5A495068422B33526E3857375146366F6455364D506B5255394473362B554D3D')

    def send_sms(phone, code):
        print("---------------------------------send message to SMS.ir----------------------------- ")
        # get SMS.ir Token
        # token_url = 'http://RestfulSms.com/api/MessageSend'
        token_url = 'https://RestfulSms.com/api/UltraFastSend'
        token = SMS.get_sms_token()
        headers = {'Content-Type': 'application/json',
                   'x-sms-ir-secure-token': token}

        # data = {
        #     "Messages":[f"کد سامانه پزشکیتو: {code}"],
        #     "MobileNumbers": [f"{phone}"],
        #     "LineNumber": "10002020100",
        #     "SendDateTime": "",
        #     "CanContinueInCaseOfError": "false",
        # }
        print(phone, "   ", code)
        data = {
            "ParameterArray": [
                {"Parameter": "VerificationCode", "ParameterValue": f"{code}"}
            ],
            "Mobile": f"{phone}",
            "TemplateId": "34723"
        }

        try:
            pass
            request = requests.post(url=token_url, headers=headers, json=data)
            print(request.status_code)
            # print(request.json()['TokenKey'])
            if request.status_code == 201:
                return True
            else:
                return False
        except:
            return False

    def send_otp(self, phone, otp_code):
        try:

            params = {
                'receptor': f'{phone}',
                'template': 'otp',
                'token': f'{otp_code}',
                'token2': '',
                'token3': '',
                'type': 'sms',  # sms vs call
            }
            response = self.sms_api.verify_lookup(params)
            print(response)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)
