from django.shortcuts import render, redirect, HttpResponse
from repository.forms import formformat
from repository import models
from utils.auth_tool import my_auth
from rbac.service import initial_permission
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.conf import settings
import os
import traceback


def sign_in(request):
    if request.method == 'GET':
        obj = formformat.LoginForm()
        return render(request, 'sign/sign-in.html', {"obj": obj})

    elif request.method == 'POST':
        obj = formformat.LoginForm(request.POST)

        if obj.is_valid():
            print('clean_data', obj.cleaned_data)
            auth_data = {}
            for i in obj.cleaned_data:
                if obj.cleaned_data[i]:
                    auth_data[i] = obj.cleaned_data[i]
            user = my_auth(**auth_data)
            print(user)

            if user:
                print(user.username)
                print(user.id)
                print(user.avatar)
                request.session['login_status'] = True
                request.session['username'] = user.username
                request.session['uid'] = user.id
                if user.avatar:
                    request.session['avatar'] = user.avatar.url
                else:
                    request.session['avatar'] = settings.DEFAULT_IMG_PATH
                initial_permission(request, user.id)
                print(request.session['rbac_permission_session_key'])
                if request.session['rbac_permission_session_key'].get('/backend.html'):
                    request.session['backend'] = True
                print(request.session.items())
                return redirect('/index.html')
            else:
                obj.add_error('password', ValidationError('密码错误'))
                print(obj.errors)
                return render(request, 'sign/sign-in.html', {'obj': obj})

        return render(request, 'sign/sign-in.html', {'obj': obj})


def sign_out(request):
    request.session['login_status'] = False
    del request.session['username']
    del request.session['uid']
    del request.session['avatar']
    print(request.session.items())
    return redirect('/index.html')


def sign_up(request):
    if request.method == 'GET':
        obj = formformat.RegisterForm()
        return render(request, 'sign/sign-up.html', {"obj": obj})

    elif request.method == 'POST':
        print(request.POST, request.FILES)
        obj = formformat.RegisterForm(request.POST, request.FILES)
        ret = {'status': True, 'errors': None}

        try:
            code = request.session['code']
            input_code = request.POST.get('code').upper()
            print('input_code', input_code, ': code', code)
            if code != input_code:
                raise ValidationError('验证码错误')
            if obj.is_valid():
                print(obj.cleaned_data)
                reg_data = {}
                for i in obj.cleaned_data:
                    if obj.cleaned_data[i]:
                        reg_data[i] = obj.cleaned_data[i]
                res = models.User.objects.create(**reg_data)
                print('res:', res)
                if res:
                    username = obj.cleaned_data['username']
                    user = models.User.objects.filter(username=username).first()
                    print('user:', user)

                    request.session['login_status'] = True
                    request.session['username'] = user.username
                    request.session['uid'] = user.id
                    print(user.avatar)
                    if user.avatar:
                        request.session['avatar'] = user.avatar.url
                    else:
                        request.session['avatar'] = settings.DEFAULT_IMG_PATH
                    initial_permission(request, user.id)
                    print(request.session['rbac_permission_session_key'])
                    if request.session['rbac_permission_session_key'].get('/backend.html'):
                        request.session['backend'] = True
                    print('session', request.session.items())
                    # return redirect('/index.html')
                    return JsonResponse(ret)

                obj.add_error('__all__', ValidationError('服务器繁忙，请稍后再试'))
        except Exception as e:
            print(traceback.format_exc())
            obj.add_error('__all__', e)

        request.session['login_status'] = False
        print('注册失败')
        ret['status'] = False
        ret['errors'] = obj.errors
        return JsonResponse(ret)


def code(request):
    from utils.code_generator import rd_check_code
    img, code = rd_check_code()
    from io import BytesIO
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['code'] = code
    print(code)
    return HttpResponse(stream.getvalue())


def upload(request):
    if request.method == 'POST':
        print(request.POST, request.FILES)
        file_obj = request.FILES.get("fafafa")
        file_path = os.path.join("static/imgs", file_obj.name)
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse(file_path)

