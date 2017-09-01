# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required(login_url='/login')
def index(request):
    return render_to_response('index.html')

@csrf_exempt
def login(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/',{"user":request.user})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user and user.is_active:
            auth.login(request,user)
            request.session['username'] = username
            return HttpResponseRedirect('/user/center/',{"user":request.user})
        else:
            if request.method == "POST":
                return render_to_response('login.html',{"login_error_info":"用户名不错存在，或者密码错误！"})
            else:
                # return render_to_response('login.html',context_instance=RequestContext(request))
                return render_to_response('login.html')

def user_center(request):
    return render_to_response('user_center.html',{"user":request.user})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')
