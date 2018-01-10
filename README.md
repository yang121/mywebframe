```
作者: YANG
版本: v0.7
程序介绍:
    第八模块Django框架第三次作业。使用了jquery, Bootstrap, kindeditor等前端插件，使用rbac应用做权限管理，自带sqlite3做数据库。
    1、用户登录模块
        （1）登录：实现手机，邮箱，用户名自动直接登录。
        （2）注册：实现Django form表单验证，验证码验证，可上传头像并预览。
    2、博客首页
        （1）帖子列表：实现帖子的图片+文字展示。
        （2）分页：实现自定义能指定显示页码的分页功能。
        （3）点赞：实现点赞后数据库后台记录的数字变化及按钮状态变化。
        （4）评论：可指定回复对象，并在评论内容中显示回复对象
    3、文章编辑器
        （1）富文本编辑器：使用kindedit插件实现富文本输入
        （2）分类及标签：可选择分类及选择多个标签与文章关联
    4、权限系统
        实现权限管理，未登录者可查看首页，但不能使用点赞，评论，发帖等功能

程序结构:

    第三次作业/                      #主程目录
    ├── MyBlog                         #执行文件
    │   ├── __init__.py
    │   ├── settings.py             # 自定义配置文件
    │   ├── url.py                  # 路由配置文件
    │   └── wsgi.py
    ├── rbac                        # rbac权限管理app
    │   ├── __init__.py
    │   ├── middleware/             # 中间件目录
    │   ├── templatetags/           # 后台目录模板simple_tag
    │   ├── theme/                  # 后台主题控制文件
    │   ├── service.py              # 权限初始化工具
    │   ├── urls.py                 # rbac分路由
    │   ├── app.py
    │   └── view.py                 # rbac视图函数(包含注册、登录等)
    ├── repository                  # 数据库管理app
    │   ├── __init__.py
    │   ├── form                    # 数据验证工具
    │   │   └─formformat.py         # form验证
    │   ├── migrations              # 数据表更改记录
    │   ├── admin.py                # admin后台配置
    │   ├── app.py
    │   └── model.py                # 数据表对象
    ├── static                      # 静态文件目录
    │   ├── admin                   # 管理员下载目录
    │   └── user                    # 用户下载目录（目录名为用户名）
    ├── templates                   # 模板目录
    │   ├── sign                    # 登录模块模板
    │   │   ├── sign-in.html        # 登录
    │   │   └── sign-up.html        # 注册
    │   ├── index.html              # 首页
    │   ├── index-layout.html       # 首页母版
    │   └── wirte.html              # 文章编辑页
    ├── utils                       # 小工具
    │   ├── auth_tool.py            # 登录信息验证
    │   ├── code_generator.py       # 验证码生成器
    │   ├── json_time_extend.py     # json时间格式扩展
    │   ├── my_paginator.py         # 分页工具（页码数量限制）
    │   ├── session_manage.py       # session登录管理工具
    │   └── xss_defend.py           # 编辑器xss工具防御工具
    ├── web                         # 程序核心app
    │   ├── __init__.py
    │   ├── app.py                  
    │   └── view.py                 # 首页视图函数
    ├── .gitignore
    ├── db.sqlite3
    ├── manage.py
    └── README.md

测试帐号：
    可自行注册
    普通用户 ——— lzyang121、密码：123456
```