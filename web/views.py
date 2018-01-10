from django.shortcuts import render, HttpResponse, redirect
from repository import models
from django.http.response import JsonResponse
from django.conf import settings


def index(request, *args):
    if not args:
        current = 1
    else:
        current = int(args[0])
    print('current:',current)
    from utils.my_paginator import PageInfo, Custompager
    artis_objs = models.Article.objects.all()
    total_item_count = artis_objs.count()
    paginator = PageInfo(current, total_item_count, 2)
    start = paginator.From()
    end = paginator.To()
    total_page = paginator.TotalPage()
    artis = artis_objs[start:end]
    paginator_html = Custompager('/index.html/', current, total_page)
    ret = {'artis': artis, 'paginator_html': paginator_html}
    return render(request, 'index.html', ret)


def comment(request, article_id, *args):
    try:
        permission_code = request.permission_code
    except Exception:
        permission_code = settings.RBAC_DEFAULT_QUERY_VALUE.upper()

    print('permission_code', permission_code)

    if permission_code == 'POST':
        print('POSTING....')
        from repository.forms.formformat import ReplyForm
        obj = ReplyForm(request.POST)
        print('POST:',request.POST)
        ret = {'status': True, 'errors': None}
        if not obj.is_valid():
            ret['errors'] = obj.errors
            ret['status'] = False
            print(1, ret)
            return JsonResponse(ret)

        print('clean_data:', obj.cleaned_data)

        query_dict = obj.cleaned_data

        query_dict['user_id'] = query_dict.pop('user')
        query_dict['article_id'] = query_dict.pop('article')
        if query_dict.get('reply'):
            query_dict['reply_id'] = query_dict.pop('reply')

        res = models.Comment.objects.create(**query_dict)
        print(res)
        if not res:
            ret['status'] = False
        from django.db.models import F
        models.Article.objects.filter(id=article_id).update(comment_count=F('comment_count')+1)
        print(ret)
        return JsonResponse(ret)

    elif permission_code == 'DELETE':
        query_dict = request.POST.dict()
        print('POST:', request.POST)
        ret = {'status': True, 'errors': None}
        if not query_dict:
            ret['status'] = False
            ret['errors'] = '删除错误，请稍后再试'
            return JsonResponse(ret)

        res = models.Comment.objects.filter(**query_dict).delete()
        from django.db.models import F
        article_id = query_dict['article_id']
        res2 = models.Article.objects.filter(id=article_id).update(comment_count=F('comment_count')-1)
        if not res or not res2:
            ret['status'] = False
            ret['errors'] = '服务器繁忙，请稍后再试'

        print('DELETED!', ret)
        return JsonResponse(ret)

    else:
        ret = {'status':True, 'data': None}
        data = models.Comment.objects.filter(article_id=article_id).order_by('create_time').values(
            'reply__user__username',
            'user__blog__site',
            'id',
            'user_id',
            'user__avatar',
            'reply__user__blog__site',
            'content',
            'user__username',
            'article_id'
        )
        ret['data'] = list(data)
        print(ret)
        return JsonResponse(ret, safe=False)


def like(request, article_id, uid):
    ret = {'status': True, 'up_stat':None, 'up_count': None}
    from django.db.models import F
    updown_objs = models.UpDown.objects.filter(article_id=article_id, user_id=uid)
    article_objs = models.Article.objects.filter(id=article_id)
    up_count = article_objs.first().up_count
    if updown_objs:
        up_stat = updown_objs.first().up
        if up_stat:
            print(updown_objs)
            updown_objs.update(up=False)
            up_stat = False
            article_objs.update(up_count=F('up_count')-1)
            up_count -= 1
        else:
            updown_objs.update(up=True)
            up_stat = True
            article_objs.update(up_count=F('up_count')+1)
            up_count += 1

        ret['up_count'] = up_count
        ret['up_stat'] = up_stat
    else:
        models.UpDown.objects.create(article_id=article_id, user_id=uid, up=True)
        models.Article.objects.filter(id=article_id).update(up_count=F('up_count') + 1)
        up_count += 1
        ret['up_stat'] = True
        ret['up_count'] = up_count

    print(ret)
    return JsonResponse(ret)


def write(request):
    print('session:',request.session.items())
    print('permission_code:',request.permission_code)
    from repository.forms.formformat import ArticleForm
    if request.method == 'GET':
        site = request.session['site']
        blog_id = models.Blog.objects.filter(site=site).values_list('id').first()[0]
        print('blog_id', blog_id)
        obj = ArticleForm({'blog': blog_id})
        return render(request, 'write.html', {'obj': obj})
    else:
        obj = ArticleForm(request.POST, request.FILES)
        print('is valid:', obj.is_valid())
        print('errors:', obj.errors.items())
        if obj.is_valid():
            data = obj.cleaned_data
            data['blog_id'] = data.pop('blog')
            content = data.pop('content')
            tags = data.pop('tag')
            print('tags:', tags)
            art_res = models.Article.objects.create(**data)
            data.pop('img')
            aid = models.Article.objects.filter(**data).values_list('id').first()[0]
            tag_obj_list = []
            for i in tags:

                tag_obj_list.append(models.Article2Tag(article_id=aid, tag_id=int(i)))

            print('aid', aid)

            print(tag_obj_list)

            models.Article2Tag.objects.bulk_create(tag_obj_list)

            detail_res = models.ArticleDetail.objects.create(content=content, article_id=aid)
            if art_res and detail_res:
                return redirect('/index.html')
            else:
                return HttpResponse('fail')
        else:
            return render(request, 'write.html', {'obj': obj})

def upload_img(request):
    import os
    file_obj = request.FILES.get('imgFile')
    file_path = os.path.join('static/imgs/upload',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    dic = {
        'error': 0,
        'url': '/' + file_path,
        'message': '上传图片失败，请稍后再试'
    }
    import json
    return HttpResponse(json.dumps(dic))