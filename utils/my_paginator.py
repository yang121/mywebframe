"""
分页时需要做三件事：

- 创建处理分页数据的类
- 根据分页数据获取数据
- 输出分页HTML，即：［上一页］［1］［2］［3］［4］［5］［下一页］
"""


from django.utils.safestring import mark_safe
from django.conf import settings


class PageInfo(object):
    def __init__(self, current, totalItem, perItems=settings.PER_PAGE_ITEM_AMOUNT_DEFAULT):
        self.__current = current
        self.__perItems = perItems
        self.__totalItem = totalItem

    def From(self):
        return (self.__current - 1) * self.__perItems

    def To(self):
        return self.__current * self.__perItems

    def TotalPage(self):  # 总页数
        result = divmod(self.__totalItem, self.__perItems)
        if result[1] == 0:
            return result[0]
        else:
            return result[0] + 1


def Custompager(baseurl, currentPage, totalpage):# 基础页，当前页，总页数
    perPager = 11
    # 总页数<11
    # 0 -- totalpage
    # 总页数>11
    # 当前页大于5 currentPage-5 -- currentPage+5
    # currentPage+5是否超过总页数,超过总页数，end就是总页数
    # 当前页小于5 0 -- 11
    begin = 0
    end = 0

    if totalpage <= settings.PAGE_NUM_AMOUNT:
        begin = 0
        end = totalpage
    else:
        if currentPage > settings.PREV_OR_NEXT_PAGE_AMOUNT:
            begin = currentPage - settings.PREV_OR_NEXT_PAGE_AMOUNT
            end = currentPage + settings.PREV_OR_NEXT_PAGE_AMOUNT
            if end > totalpage:
                end = totalpage
        else:
            begin = 0
            end = settings.PAGE_NUM_AMOUNT
    pager_list = []
    if currentPage <= 1:
        first = "<li class='disabled'><span>首页</span></li>"
    else:
        first = "<li><a href='%s%d'>首页</a></li>" % (baseurl, 1)
    pager_list.append(first)

    if currentPage <= 1:
        prev = "<li class='disabled'><span href=''>«</span></li>"
    else:
        prev = "<li><a href='%s%d'>«</a></li>" % (baseurl, currentPage - 1)
    pager_list.append(prev)

    for i in range(begin + 1, end + 1):
        if i == currentPage:
            temp = "<li class='active'><a href='%s%d' class='selected'>%d</a></li>" % (baseurl, i, i)
        else:
            temp = "<li><a href='%s%d'>%d</a></li>" % (baseurl, i, i)
        pager_list.append(temp)
    if currentPage >= totalpage:
        next = "<li class='disabled'><span aria-hidden='true'>»</span></li>"
    else:
        next = "<li><a href='%s%d'><span aria-hidden='true'>»</span></a></li>" % (baseurl, currentPage + 1)
    pager_list.append(next)
    if currentPage >= totalpage:
        last = "<li class='disabled'><span aria-hidden='true'>尾页</span></li>"
    else:
        last = "<li><a href='%s%d'><span aria-hidden='true'>尾页</span></a></li>" % (baseurl, totalpage)
    pager_list.append(last)
    result = ''.join(pager_list)
    return mark_safe(result)  # 把字符串转成html语言

"""
<nav aria-label="...">
  <ul class="pagination">
    <li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
    <li class="active"><a href="#">1 <span class="sr-only">(current)</span></a></li>
    ...
  </ul>
</nav>
"""