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
    avatar = models.CharField(verbose_name='头像路径', max_length=128, null=True, blank=True)
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




class Column(models.Model):
    caption = models.CharField(verbose_name='专栏标题', max_length=32)
    keywords = models.ManyToManyField(
        verbose_name='关键字',
        to='Keyword',
        through='Keyword2Column',
        related_name='k2c',
        through_fields=('column', 'keyword'),
    )
    img = models.FileField(verbose_name='图片', upload_to='static/imgs/cols/')
    link = models.CharField(verbose_name='链接',max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "%s[%s]" % (self.caption, self.keywords.all())


class Keyword(models.Model):
    caption = models.CharField(verbose_name='关键字名称', max_length=32, unique=True)

    goods = models.ManyToManyField(
        verbose_name='商品',
        to='Goods',
        through='Keyword2Goods',
        related_name='g2k',
        through_fields=('keyword', 'goods'),   # 坑坑坑！此处要按顺序放置字段，要与原表一样
    )

    columns = models.ManyToManyField(
        verbose_name='专栏',
        to='Column',
        through='Keyword2Column',
        related_name='c2k',
        through_fields=('keyword', 'column'),
    )

    def __str__(self):
        return "%s" % self.caption


class Keyword2Column(models.Model):
    keyword = models.ForeignKey('Keyword', verbose_name='关键字')
    column = models.ForeignKey('Column', verbose_name='专栏',)

    class Meta:
        unique_together = (
            ('keyword', 'column'),
        )

    def __str__(self):
        return "%s-%s" % (self.column.caption, self.keyword.caption)


class Keyword2Goods(models.Model):
    keyword = models.ForeignKey('Keyword', verbose_name='关键字')
    goods = models.ForeignKey('Goods', verbose_name='商品')

    class Meta:
        unique_together = (
            ('keyword', 'goods'),
        )

    def __str__(self):
        return "%s-%s" % (self.goods.caption, self.keyword.caption)


class Goods(models.Model):
    caption = models.CharField(verbose_name='商品标题', max_length=64)
    brief = models.CharField(verbose_name='简介', max_length=128, null=True, blank=True)
    keywords = models.ManyToManyField(
        verbose_name='关键字',
        to='Keyword',
        through='Keyword2Goods',
        related_name='k2g',
        through_fields=('goods', 'keyword'),
    )
    img = models.FileField(verbose_name='图片', upload_to='static/imgs/goods/')
    price = models.FloatField(verbose_name='价格', max_length=16)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    brand = models.CharField(verbose_name='品牌', max_length=16, null=True, blank=True)
    category = models.CharField(verbose_name='类别', max_length=16, null=True)

    def __str__(self):
        return "%s-%s" % (self.id, self.caption)


class Ad(models.Model):
    caption = models.CharField(verbose_name='广告标题', max_length=64)
    link = models.CharField(verbose_name='链接', max_length=64)
    img = models.FileField(verbose_name='图片', upload_to='static/imgs/ad/')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    place_choices = (
        (1, '第一位'),
        (2, '第二位'),
        (3, '第三位'),
        (4, '第四位'),
        (5, '第五位'),
        (6, '第六位'),
    )
    place = models.IntegerField(verbose_name='位置', choices=place_choices, null=True, blank=True, unique=True)

    def __str__(self):
        return "%s[%s]" % (self.caption, self.place)