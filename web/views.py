from django.shortcuts import render
from repository import models
from django.db.models import Count

def index(request):

    cols = models.Column.objects.all()
    ads = models.Ad.objects.filter(place__isnull=False).order_by('place')
    print('ads:', ads)
    for c in cols:
        print(c.keyword2column_set, c.img, c.link, c.caption)

    for a in ads:
        print(a.id, a.caption, a.img, a.link, a.create_time)

    keywords = models.Keyword2Goods.objects.values('keyword__caption').annotate(count=Count(1)).order_by(
        '-count').first()['keyword__caption']

    ret = {'cols': cols, 'ads': ads, 'keywords': keywords}

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