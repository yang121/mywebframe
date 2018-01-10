from django.shortcuts import render, redirect, HttpResponse
from repository.forms import formformat
from repository import models
from utils.auth_tool import my_auth
from utils.session_manage import SessionManage
from rbac.service import initial_permission
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.conf import settings
import os
import traceback


# class SessionManage:
#     def __init__(self, request):
#         self.request = request
#
#     def sign_in(self, user):
#         self.request.session['login_status'] = True
#         self.request.session['username'] = user.username
#         self.request.session['uid'] = user.id
#         if user.avatar:
#             self.request.session['avatar'] = user.avatar.url
#         else:
#             self.request.session['avatar'] = settings.DEFAULT_IMG_PATH
#         initial_permission(self.request, user.id)
#         print(self.request.session[settings.RBAC_PERMISSION_SESSION_KEY])
#         if self.request.session[settings.RBAC_PERMISSION_SESSION_KEY].get('/backend.html'):
#             self.request.session['backend'] = True
#
#     def sign_out(self):
#         self.request.session['login_status'] = False
#         del self.request.session['username']
#         del self.request.session['uid']
#         del self.request.session['avatar']
#         del self.request.session[settings.RBAC_MENU_PERMISSION_SESSION_KEY]
#         del self.request.session[settings.RBAC_PERMISSION_SESSION_KEY]


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
                session = SessionManage(request)
                session.sign_in(user)
                return redirect('/index.html')
            else:
                obj.add_error('password', ValidationError('密码错误'))
                print(obj.errors)
                return render(request, 'sign/sign-in.html', {'obj': obj})

        return render(request, 'sign/sign-in.html', {'obj': obj})


def sign_out(request):
    session = SessionManage(request)
    session.sign_out()
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

                    session = SessionManage(request)
                    session.sign_in(user)
                    print('session', request.session.items())
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

