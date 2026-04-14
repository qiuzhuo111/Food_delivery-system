from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="用户名", help_text="用于登录，请勿使用真实姓名。")
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)


class CheckoutForm(forms.Form):
    contact_phone = forms.CharField(label="联系电话", max_length=32)
    delivery_address = forms.CharField(label="配送地址", max_length=255)
    remark = forms.CharField(label="备注", max_length=200, required=False)
