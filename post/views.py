from django.shortcuts import render
from django.http import JsonResponse,HttpRequest,HttpResponseBadRequest,HttpResponseNotFound
from user.views import auth
from post.models import Post,Content
import simplejson
import datetime
import math
# Create your views here.
@auth
def pub(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        title = payload['title']
        text = payload['content']
        post = Post()
        post.title = title
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.author = request.user

        post.save()

        content = Content()
        content.post = post
        content.content = text
        content.save()
        return JsonResponse({
            'post_id': post.id
        })
    except Exception as e:
        return HttpResponseBadRequest("sb")
    return JsonResponse()
def get(request:HttpRequest, id):
    try:
        post = Post.objects.get(pk=id)
        return JsonResponse({
            'post':{
                'post_id': post.id,
                'title': post.title,
                'postdate': int(post.postdate.timestamp()),
                'author_name': post.author.name,
                'author_id': post.author_id,
                'content': post.content.content
            }
        })
    except Exception as e:
        return HttpResponseNotFound('not found')
    return JsonResponse()
def validate(d:dict, name:str, convert_fun, default, validata_fun):
    try:
        x = convert_fun(d.get(name))
        ret = validata_fun(x, default)   #ret if ret>0 else 1
    except Exception as e:
        ret = default
    return ret

def getall(request:HttpRequest):
    # try:
    #     page = int(request.GET.get('page'))
    #     page = page if page>0 else 1
    # except Exception as e:
    #     page = 1
    page = validate(request.GET, 'page', int, 1, lambda x,y: x if x>0 else y)
    # try:
    #     size = int(request.GET.get('size'))
    #     size = size if size>0 and size <3 else 2
    # except Exception as e:
    #     size = 2
    size = validate(request.GET, 'size', int, 20, lambda x,y: x if x>0 and x < 101 else y)
    start = (page-1)*size
    posts = Post.objects.order_by('-pk')
    count = posts.count()
    posts = posts[start:start+size]

    if posts:

        return JsonResponse({
            'posts': [
                {
                    'post_id': post.id,
                    'title': post.title,
                    'postdate': int(post.postdate.timestamp()),
                    'author_name': post.author.name,
                    'author_id': post.author_id,
                    'content': post.content.content
                }for post in posts
            ], 'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': math.ceil(count/size)
            }
        })
    else:
        return HttpResponseNotFound()
