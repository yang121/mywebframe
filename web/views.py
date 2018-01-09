from django.shortcuts import render, HttpResponse
from repository import models
from django.db.models import Count
from django.core.serializers import serialize
from django.http.response import JsonResponse
from django.conf import settings


def index(request):

    artis = models.Article.objects.all()
    print(artis[0].img)
    print(artis[0].blog.user.avatar)
    ret = {'artis': artis}

    return render(request, 'index.html', ret)


def search(request):
    # keywords = request.GET.get('keywords').strip().split(' ')
    print('GET.values:', request.GET.dict())

    #获取request中的键值对
    request_dict = request.GET.dict()
    if not request_dict['keywords']:
        most_keyword = models.Keyword2Goods.objects.values_list('keyword__caption').annotate(count=Count(1)).order_by('-count').first()[0]
        request_dict['keywords'] = most_keyword
        print('most_keyword:', most_keyword)
    condition_dict = {}
    search_key = {}

    # 去重并重新构造
    for k in request_dict:
        v = request_dict[k].strip().split(' ')
        i_list = []
        for i in v:
            if i not in i_list:
                i_list.append(i)
            else:
                if k == 'keywords':
                    continue
                i_list.remove(i)
        condition_dict[k] = i_list
        new_v = ' '.join(i_list)
        search_key[k] = new_v

    print('condition_dict:', condition_dict)
    print('search_key:', search_key)


    # 创建查询语句
    from django.db.models import Q

    con = Q()
    for k, v in condition_dict.items():
        # print(k, v)
        q = Q()
        q.connector = 'OR'
        if k == 'keywords':
            k = 'keywords__caption'
        # v = v.strip().split(' ')
        print(v)
        for i in v:
            q.children.append((k, i))
        con.add(q, 'AND')

    # 增加标题查找
    print(con)
    caption_q = Q()
    caption_q.connector = 'AND'
    for j in condition_dict['keywords']:
        caption_q.children.append(('caption__contains', j))
    con.add(caption_q, 'OR')

    # 查找对象
    goods_obj = models.Goods.objects.filter(con).distinct()
    print(goods_obj.query)

    # 查找商品
    goods = goods_obj.all()
    print(goods)

    # 查找关键字
    keywords = models.Keyword2Goods.objects.filter(goods__in=goods).values_list('keyword__caption').annotate(count=Count(1))
    print('keywords：', keywords)
    keywords_list = [x[0] for x in keywords]
    for k in keywords_list:
        if search_key.get('keywords') and k in search_key.get('keywords'):
            keywords_list.remove(k)
    print('keywords_list:', keywords_list)

    # 查找品牌
    brand = goods_obj.values('brand').annotate(count=Count(1)).order_by('-count')
    brand_list = []
    for b in brand:
        v = b.get('brand')
        if search_key.get('brand') and v in search_key.get('brand'):
            continue
        brand_list.append(v)

    print('brand_list:', brand_list)

    # 查找类别
    category = goods_obj.values('category').annotate(count=Count(1)).order_by('-count')
    category_list = []
    for c in category:
        v = c.get('category')
        if search_key.get('category') and v in search_key.get('category'):
            continue

        category_list.append(v)
    print('category_list:', category_list)

    # 构造返回值

    ret = {
        'search_info': {
            'goods': goods,
            'brand_list': brand_list,
            'category_list': category_list,
            'keyword_list': keywords_list
        },
        'search_key': search_key
    }

    return render(request, 'search.html', ret)


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
