from django.db import models


class User(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32, unique=True, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.EmailField(verbose_name='邮箱', unique=True, null=True, blank=True)
    telephone = models.CharField(verbose_name='手机号码', max_length=32, unique=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, null=True, blank=True)
    avatar = models.FileField(verbose_name='头像路径', upload_to='static/imgs/avatar/', null=True, blank=True)
    fans = models.ManyToManyField(
        verbose_name='粉丝们',
        to='User',
        through='UserFans',
        related_name='u2f',
        through_fields=('user', 'follower'),
    )
    group = models.ManyToManyField(
        verbose_name='用户组',
        to='UserGroup',
        through='User2Group',
        related_name='u2g',
        through_fields=('user', 'group'),
    )
    role = models.ManyToManyField(
        verbose_name='角色',
        to='Role',
        through='User2Role',
        related_name='u2r',
        through_fields=('user', 'role'),
    )

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客表
    """
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name="个人博客前缀",max_length=32, unique=True)
    theme = models.CharField(verbose_name="博客主题",max_length=72)
    user = models.OneToOneField(to='User', to_field='id')


class UserFans(models.Model):
    """
    粉丝关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='User', to_field='id', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='User', to_field='id', related_name='followers')

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]

    def __str__(self):
        return "%s-%s" % (self.user.username, self.follower.username)

class Category(models.Model):
    """
    博主个人文章分类表
    """
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客", to="Blog", to_field="id")

    def __str__(self):
        return '%s-%s' % (self.blog.title, self.title)


class Article(models.Model):
    title = models.CharField(verbose_name='文章标题', max_length=128)
    img = models.ImageField(verbose_name='文章图片', null=True)
    summary = models.CharField(verbose_name="文章简介", max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    blog = models.ForeignKey(verbose_name="所属博客", to="Blog", to_field="id")
    category = models.ForeignKey(verbose_name="文章类型", to="Category", to_field="id", null=True)

    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "Golang"),
    ]

    article_type_id = models.IntegerField(choices=type_choices, default=None)

    tag = models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=('article', 'tag'),
    )


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name="文章", to="Article", to_field="id")
    tag = models.ForeignKey(verbose_name="标签", to="Tag", to_field="id")

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name="所属文章", to="Article", to_field='id')


class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='id')
    user = models.ForeignKey(verbose_name='赞或踩用户', to='User', to_field='id')
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Tag(models.Model):
    """
    标签
    """
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客", to="Blog", to_field="id")


class Comment(models.Model):
    """
    评论表
    """
    content = models.CharField(verbose_name="评论内容", max_length=255)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)
    reply = models.ForeignKey(verbose_name="回复评论", to="self", related_name="back", null=True)
    article = models.ForeignKey(verbose_name="评论文章", to="Article", to_field="id")
    user = models.ForeignKey(verbose_name="评论者", to="User", to_field='id')


class UserGroup(models.Model):
    """
    用户组表
    """
    caption = models.CharField(verbose_name='组名', max_length=32, unique=True)

    def __str__(self):
        return self.caption


class User2Group(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', related_name='groups')
    group = models.ForeignKey(UserGroup, verbose_name='组', related_name='users')

    class Meta:
        unique_together = [
            ('user', 'group')
        ]

    def __str__(self):
        return "%s-%s" % (self.user.username, self.group.caption)


class Role(models.Model):
    """
    角色表
    """
    caption = models.CharField(verbose_name='角色', max_length=32, unique=True)

    def __str__(self):
        return self.caption


class User2Role(models.Model):
    """
    用户角色关系表
    """
    user = models.ForeignKey(User, verbose_name='用户', related_name='roles')
    role = models.ForeignKey(Role, verbose_name='角色', related_name='users')

    class Meta:
        unique_together = [
            ('user', 'role')
        ]

    def __str__(self):
        return '%s-%s' % (self.user.username, self.role.caption,)


class Menu(models.Model):
    """
    菜单表
    """
    caption = models.CharField(verbose_name='菜单标题', max_length=32)
    parent = models.ForeignKey('self', verbose_name='父菜单', related_name='p', null=True, blank=True)

    def __str__(self):
        prev = ""
        parent = self.parent
        while True:
            if parent:
                prev = prev + '-' + str(parent.caption)
                parent = parent.parent
            else:
                break
        return '%s-%s' % (prev, self.caption,)


class Permission(models.Model):
    """
    权限
    """
    caption = models.CharField(verbose_name='权限标题', max_length=32, unique=True)
    url = models.CharField(verbose_name='URL正则', max_length=128)
    menu = models.ForeignKey(Menu, verbose_name='所属菜单', related_name='permissions', null=True, blank=True)

    def __str__(self):
        return "%s-%s" % (self.caption, self.url,)


class Action(models.Model):
    """
    操作：增删改查
    """
    caption = models.CharField(verbose_name='操作标题', max_length=32)
    code = models.CharField(verbose_name='方法', max_length=32)

    def __str__(self):
        return self.caption


class Permission2Action2Role(models.Model):
    """
    权限操作关系表
    """
    permission = models.ForeignKey(Permission, verbose_name='权限URL', related_name='actions')
    action = models.ForeignKey(Action, verbose_name='操作', related_name='permissions')
    role = models.ForeignKey(Role, verbose_name='角色', related_name='p2as')

    class Meta:
        unique_together = (
            ('permission', 'action', 'role'),
        )

    def __str__(self):
        return "%s-%s-%s" % (self.permission, self.action, self.role,)
