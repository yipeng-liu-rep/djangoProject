from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache

from djangoProject import settings
import requests
import hashlib, time
from api_index.models import UserInfo


def get_login_info(code):
    # 获取code
    code_url = settings.code2Session.format(settings.AppId, settings.AppSecret, code)
    response = requests.get(code_url)
    json_response = response.json() # 把它变成json的字典
    if json_response.get("session_key"):
        return json_response
    else:
        return False


class Login(APIView):
    def post(self, request):
        param = request.data
        userdata = param.get('userdata')
        print(userdata)
        if not param.get('code'):
             return Response({'status': 1, "msg": "缺少参数"})
        else:
            code = param.get('code')
            user_data = get_login_info(code)
            if user_data:
                val = user_data['session_key'] + "&" + user_data['openid']
                md5 = hashlib.md5()
                md5.update(str(time.clock()).encode('utf-8'))
                md5.update(user_data['session_key'].encode('utf-8'))
                key = md5.hexdigest()
                print(key)
                print(val)
                cache.set(key, val, timeout=None)
                print(cache.keys('*'))
                print('key='+cache.get(key))
                has_user = UserInfo.objects.filter(openid=user_data['openid']).first()
                if not has_user:
                    UserInfo.objects.create(username=userdata['nickName'], avatar=userdata['avatarUrl'],
                                            city=userdata['city'], language=userdata['language'],
                                            province=userdata['province'], openid=user_data['openid'])
                UserInfo.objects.update()
                userinfo = UserInfo.objects.get(openid=user_data['openid'])

                return Response({
                    'status': 0,
                    'msg': 'ok',
                    'data': {'token': key,
                             'user_id': userinfo.id}
                })
            else:
                return Response({'status': 2, 'msg': "无效的code"})

