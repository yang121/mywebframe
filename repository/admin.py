from django.contrib import admin
from repository import models

admin.site.register(models.User)
admin.site.register(models.Menu)
admin.site.register(models.Action)
admin.site.register(models.Permission)
admin.site.register(models.Permission2Action2Role)
admin.site.register(models.Role)
admin.site.register(models.User2Role)
admin.site.register(models.UserGroup)
admin.site.register(models.User2Group)
admin.site.register(models.UserFans)
admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Article2Tag)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Blog)
admin.site.register(models.UpDown)
