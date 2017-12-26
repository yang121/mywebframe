
user_config = [
    {
        'q': None,         # 数据查询字段
        'title': '选择',     # 显示标题
        'display': True,   # 是否显示
        'text': {
            'tpl': "<input type='checkbox' value='{n1}' />",
            'kwargs': {'n1': '@id'}
        },
        'attrs':{'nid':'@id'}

    },
    {
        'q': 'id',
        'title': 'ID',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@id'}
        },
        'attrs':{'k1':'v1','k2':'@id'}
    },
    {
        'q': 'username',
        'title': '用户名',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@username'}
        },
        'attrs':{'k1':'v1','origin':'@username','edit-enable':'true','edit-type':'input','name':'username'}
    },

    {
        'q': 'email',
        'title': '电子邮箱',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@email'}
        },
        'attrs': {'k1': 'v1', 'origin': '@email', 'edit-enable': 'true', 'edit-type': 'input',
                  'name': 'email'}
    },

    {
        'q': 'password',
        'title': '密码',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@password'}
        },
        'attrs': {'k1': 'v1', 'origin': '@password', 'edit-enable': 'true', 'edit-type': 'input',
                  'name': 'password'}
    },

    # 页面显示：标题：操作；删除，编辑：a标签
    {
        'q': None,
        'title': '操作',
        'display': True,
        'text': {
            'tpl': "<a href='/backend/userinfo_json.html?md=delete&nid={nid}'>删除</a>",
            'kwargs': {'nid': '@id'}
        },
        'attrs':{'k1':'v1','k2':'@id'}
    },
]

search_config =  [
    {'name': 'id', 'text': '用户ID', 'search_type': 'input'},
    {'name': 'username', 'text': '用户名', 'search_type': 'input'},
    {'name': 'email', 'text': '电子邮箱', 'search_type': 'input'},
]