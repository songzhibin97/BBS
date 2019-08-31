from django import forms
from django.core.exceptions import ValidationError

# 用form类创建登录input
from app01.models import UserInfo


class Login(forms.Form):
    username = forms.CharField(
        required=True,
        label="账号:",
        max_length=20,
        min_length=3,
        error_messages={
            "required": "不能为空",
            "max_length": "账号最大不能超过20位",
            "min_length": "账号最小不能少于3位"
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}, )

    )
    password = forms.CharField(
        required=True,
        label="密码:",
        max_length=20,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        error_messages={
            "required": "不能为空",
            "max_length": "密码最大不能超过20位",
            "min_length": "密码最小不能少于6位"
        },

    )
    # password2 = forms.CharField(
    #     required=True,
    #     label="确认密码:",
    #     max_length=20,
    #     min_length=6,
    #     widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
    #     error_messages={
    #         "required": "不能为空",
    #         "max_length": "账号最大不能超过20位",
    #         "min_length": "账号最小不能少于6位"
    #     }
    # )

    # def clean_username(self):
    #
    #     Sensitivewords = ['金瓶梅', "法轮功"]
    #     value = self.cleaned_data.get("username")
    #     for i in Sensitivewords:
    #         if i in value:
    #             raise ValidationError("包含敏感词")
    #     return value
    #
    # def clean(self):
    #     value1 = self.cleaned_data.get("password")
    #     value2 = self.cleaned_data.get("password2")
    #     if value1 != value2:
    #         self.add_error("password2", "两次密码不一致")
    #         raise ValidationError("两次密码不一致")
    #     else:
    #         return self.cleaned_data


# 用form类创建注册input
class Enrol(forms.Form):
    username = forms.CharField(
        required=True,
        label="账号:",
        max_length=20,
        min_length=3,
        error_messages={
            "required": "不能为空",
            "max_length": "账号最大不能超过20位",
            "min_length": "账号最小不能少于3位"
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}, )

    )
    password = forms.CharField(
        required=True,
        label="密码:",
        max_length=20,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        error_messages={
            "required": "不能为空",
            "max_length": "密码最大不能超过20位",
            "min_length": "密码最小不能少于6位"
        },

    )
    password2 = forms.CharField(
        required=True,
        label="确认密码:",
        max_length=20,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        error_messages={
            "required": "不能为空",
            "max_length": "密码最大不能超过20位",
            "min_length": "密码最小不能少于6位"
        }
    )

    def clean_username(self):

        # 敏感字校验 局部钩子
        Sensitivewords = ['金瓶梅', "法轮功"]
        value = self.cleaned_data.get("username")
        is_exist = UserInfo.objects.filter(username=value)
        for i in Sensitivewords:
            if i in value:
                self.add_error("username", "包含敏感词")
                raise ValidationError("包含敏感词")
        if is_exist:
            self.add_error("username", "用户名已存在")
            raise ValidationError("用户名已存在")
        return value

    def clean(self):
        # 重复密码校验 全局钩子
        value1 = self.cleaned_data.get("password")
        value2 = self.cleaned_data.get("password2")
        if value1 != value2:
            self.add_error("password2", "两次密码不一致")
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data
