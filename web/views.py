from django.shortcuts import render
from repository import models

def index(request):

    cols = models.Column.objects.all()
    ads = models.Ad.objects.filter(place__isnull=False).order_by('place')
    print('ads:', ads)
    for c in cols:
        print(c.c2k, c.img, c.link, c.caption)

    for a in ads:
        print(a.id, a.caption, a.img, a.link, a.create_time)

    ret = {'cols': cols, 'ads': ads}

    return render(request, 'index.html', ret)