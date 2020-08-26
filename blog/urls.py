"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.shortcuts import render
from user import urls as user_urls

def index(request):
    context= {
        #'data' : ("{}*{}={}".format(j, i, i*j) for i in range(1, 10) for j in range(1, 10))
        'data' : range(1,10)
    }
    return render(request,'t2.html', context, status=201)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^user/', include('user.urls')),
    url(r'^post/', include('post.urls')),
]
