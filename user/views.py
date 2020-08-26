from django.shortcuts import render
from django.http import JsonResponse,HttpRequest,HttpResponseBadRequest
import simplejson
from django.db.models import Q
from .models import User
import bcrypt
import jwt
import datetime
from django.conf import settings
# Create your views here.

def gen_token(user_id):
    key = settings.SECRET_KEY
    return jwt.encode({
        'user_id':user_id,
        'exp':int(datetime.datetime.now().timestamp() + 30*60)
    }, key, 'HS256').decode()
def reg(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        query = User.objects.filter(email=email)
        if query.first():
            return HttpResponseBadRequest('用户存在')
        name = payload['name']
        password = payload['password']
        user = User()
        user.email = email
        user.name = name
        key = settings.SECRET_KEY
        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            user.save()
            token = gen_token(user.id)
            res = JsonResponse({
                'user': {
                    'user_id': user.id,
                    'name': user.name,
                    'emial': user.email
                }, 'token': token
            })
            res.set_cookie('jwt', token, secure=True)
            return res

            # return JsonResponse({'user_id':user.id})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('参数错误')
    except Exception as e:

       return HttpResponseBadRequest('参数错误')
    # return JsonResponse({'user_id': user.id})
    # return JsonResponse(jwt.encode({'user_id': user.id}, key, 'HS256'))

def login(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password']
        user = User.objects.filter(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                token = gen_token(user.id)
                res = JsonResponse({
                    'user':{
                        'user_id':user.id,
                        'name':user.name,
                        'emial':user.email
                    }, 'token':token
                })
                res.set_cookie('jwt', token,secure=True)
                return res
            else:
                return HttpResponseBadRequest('wrong1')
        else:
            return HttpResponseBadRequest('wrong2')

    except Exception as e:
        return HttpResponseBadRequest('wrong3')
def auth(view_function):
    def wrapper(request:HttpRequest):
        token = request.META.get('HTTP_JWT', None)
        print(token, '~~~~~~~~~~~~~~~~~~~~')
        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(token, key,algorithms=['HS256'])
            user = User.objects.filter(pk=payload['user_id']).first()
            if user:
                request.user = user
                ret = view_function(request)
                return ret
            else:
                return HttpResponseBadRequest('wrong token')
        except jwt.ExpiredSignatureError as e:
            return HttpResponseBadRequest('expires')

        except Exception as e:
            return HttpResponseBadRequest('wrong token')

    return wrapper
# @auth
def show(requst):
    # users = User.objects.all()
    # users = User.objects.filter(Q(pk=1) | Q(pk=3))
    # print(users)
    # meta = requst.META
    # j = list(filter(lambda x: x.lower().endswith('jwt'), meta))
    # print(j)

    # print(j)
    print(requst.user)
    print(requst.GET)
    print(requst.POST)
    print(requst.body)
    res = JsonResponse({'status':'ok'})
    res['Access-Control-Allow-Origin'] = '*'
    return res