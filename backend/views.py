from django.shortcuts import render, HttpResponse, redirect
from utils.json_time_extend import JsonCustomEncoder
from repository.forms import formformat
from repository import models
import json


def get_data_list(request,model_cls,table_config):
    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    from django.db.models import Q

    condition = request.GET.get('condition')
    condition_dict = json.loads(condition)

    con = Q()
    for name,values in condition_dict.items():
        ele = Q()    # select xx from where cabinet_num=sdf or cabinet_num='123'
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name,item))
        con.add(ele, 'AND')

    server_list = model_cls.objects.filter(con).values(*values_list)
    return server_list


def backend(request):
    if request.permission_code == 'GET':
        return render(request, 'backend/backend.html')


def userinfo(request):
    if request.permission_code == 'GET':
        return render(request, 'backend/userinfo.html')


def userinfo_json(request):
    if request.permission_code == 'GET':
        from backend.page_config import user as userConfig
        server_list = get_data_list(request,models.User,userConfig.user_config)
        ret = {
            'server_list': list(server_list),
            'table_config': userConfig.user_config,
            'global_dict':{
                # 'device_type_choices': models.User.device_type_choices,
                # 'device_status_choices': models.User.device_status_choices,
                # 'idc_choices': list(models.User.objects.values_list('id','name'))
            },
            'search_config': userConfig.search_config

        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))

    if request.permission_code == 'DELETE':
        uid = request.GET.get('nid')
        models.User.objects.filter(id=uid).delete()
        return redirect('/backend/userinfo.html')

    if request.permission_code == 'POST':
        if request.method == 'GET':
            obj = formformat.RegisterForm()
            return render(request, 'backend/add-userinfo.html', {"obj": obj})
        else:
            obj = formformat.RegisterForm(request.POST)
            return render(request, 'backend/add-userinfo.html', {"obj": obj})
