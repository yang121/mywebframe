from django.forms import Form, fields, widgets
from repository import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from repository.models import User

class LoginForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': '请输入用户名/手机号/邮箱', 'class': "form-control", 'id': "inputAccount"}),
        label='',
        label_suffix='',
        max_length=32,
        min_length=5,
        required=False,
        error_messages={
            'required': "请填写用户名",
            'min_length': "用户名长度必须大于5",
            'max_length': "用户名长度必须小于32",
        },

    )

    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'placeholder': '请输入帐号', 'class': "form-control", 'id': "inputAccount"}),
        label='',
        label_suffix='',
        required=False,
        error_messages={
            'required': "请填写电子邮箱",
            'invalid': '请填写正确的电子邮箱',
        }
    )

    telephone = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': '请输入帐号', 'class': "form-control", 'id': "inputAccount"}),
        label='',
        label_suffix='',
        required=False,
        error_messages={
            'required': "请填写手机号码",
            'invalid': '请填写正确的手机号码',
        },
        max_length=11,
        validators=[RegexValidator(r'^1\d{10}$', '请填写正确的手机号码'), ]
        # validators=[RegexValidator(r'^[0-9]+$', '请填写正确的手机号码'), ]
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'placeholder': '请输入密码', 'class': "form-control", 'id': "inputPassWord"}),
        label='',
        label_suffix='',
        max_length=64,
        min_length=6,
        error_messages={
            'required': "请填写密码",
            'min_length': "密码长度必须大于6",
            'max_length': "密码长度必须小于64",
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if not models.User.objects.filter(username=username).first():
                raise ValidationError('此用户名未被注册')
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not models.User.objects.filter(email=email).first():
                raise ValidationError("此邮箱未被注册")
            return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            if not models.User.objects.filter(telephone=telephone).first():
                raise ValidationError("此手机号码未被注册")
            return telephone

    def clean(self):
        username = self.cleaned_data.get('username')
        telephone = self.cleaned_data.get('telephone')
        email = self.cleaned_data.get('email')
        if username or telephone or email:
            return self.cleaned_data
        else:
            raise ValidationError('请填写你的帐号')




class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': '请填写用户名', 'class': "form-control", 'id': "inputUserName"}),
        label='',
        label_suffix='',
        max_length=32,
        min_length=5,
        required=True,
        error_messages={
            'required': "请填写用户名",
            'min_length': "用户名长度必须大于5",
            'max_length': "用户名长度必须小于32",
        }
    )

    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': '请填写昵称', 'class': "form-control", 'id': "inputNickname", 'null': 'true'}),
        label='',
        label_suffix='',
        max_length=32,
        required=False,
        error_messages={
            'required': "请填写昵称",
            'max_length': "昵称长度必须小于32",
        }
    )

    avatar = fields.FileField(
        widget=widgets.FileInput(attrs={'id': "imgSelect", 'null': 'true'}),
        required=False,
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'placeholder': '请填写密码', 'class': "form-control", 'id': "inputPassWord"}),
        label='',
        label_suffix='',
        max_length=64,
        min_length=6,
        required=True,
        error_messages={
            'required': "请填写密码",
            'min_length': "密码长度必须大于5",
            'max_length': "密码长度必须小于32",
        }
    )

    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'placeholder': '请填写电子邮箱', 'class': "form-control", 'id': "inputEmail", 'null': 'true'}),
        label='',
        label_suffix='',
        required=False,
        error_messages={
            'required': "请填写邮箱",
            'invalid': '邮箱格式错误',
        }
    )

    telephone = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': '请输入电话号码', 'class': "form-control", 'id': "inputTelephone"}),
        label='',
        label_suffix='',
        error_messages={
            'required': "请填写手机号码",
            'invalid': '请填写正确的手机号码',
        },
        required=True,
        validators=[RegexValidator(r'^1\d{10}$', '请填写正确的手机号码')],
        max_length=11,
    )

    gender = fields.ChoiceField(
        widget=widgets.RadioSelect(attrs={'class': "form-control", 'id': "inputGender", 'null': 'true'}),
        choices=User.gender_choices,
        label='',
        label_suffix='',
        required=False,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if models.User.objects.filter(username=username).first():
                raise ValidationError('此用户名已被注册')
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if models.User.objects.filter(email=email).first():
                raise ValidationError("此邮箱已被注册")
            return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            if models.User.objects.filter(telephone=telephone).first():
                raise ValidationError("此手机号码已被注册")
            return telephone



class ReplyForm(Form):
    content = fields.CharField(
        required=True,
        max_length=255,
    )

    reply = fields.IntegerField(
        required=False
    )

    article = fields.IntegerField(
        required=True
    )

    user = fields.IntegerField(
        required=True
    )


class ArticleForm(Form):
    img = fields.FileField()

    title = fields.CharField(
        max_length=64,
        widget=widgets.TextInput(
            attrs={'id': 'title-input', 'placeholder': "输入文章标题", 'class': 'form-control'}
        )
    )

    content = fields.CharField(
        widget=widgets.Textarea(
            attrs={'id': 'content-input', 'placeholder': "输入文章正文", 'class': 'form-control'}
        )
    )

    summary = fields.CharField(
        widget=widgets.Textarea(
            attrs={'id': 'summary-input', 'rows': "3", 'placeholder': "输入简介", 'class': 'form-control'}
        ))

    article_type_choice = models.Article.type_choices
    article_type_id = fields.IntegerField(
        widget=widgets.Select(
            choices=article_type_choice,
            attrs={'id': 'type-input', 'placeholder': "输入简介", 'class': 'form-control'}
        )
    )

    blog = fields.IntegerField(
        widget=widgets.NumberInput(attrs={'id': 'blog-input', 'class': 'hide'})
    )

    tag_type_choice = list(models.Tag.objects.values_list('id', 'title'))

    tag = fields.MultipleChoiceField(
        choices=tag_type_choice,
        widget=widgets.CheckboxSelectMultiple(
            attrs={'id': 'tag-input', 'placeholder': "输入简介", 'class': 'checkbox-inline'}
        )
    )

    def clean_content(self):
        old = self.cleaned_data['content']
        from utils.xss_defend import xss
        return xss(old)