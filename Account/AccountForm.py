from django import forms
class LoginForm(forms.Form):
    username=forms.CharField(
        required=True,

        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    password=forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "layui-input"})
    )
    fristname=forms.CharField(
        required=True,

        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    surname=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )

class RegisterForm(forms.Form):
    username=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    password=forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "layui-input"})
    )
    surname=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    confirmpassword = forms.CharField(required=True,  widget=forms.PasswordInput(attrs={"class": "layui-input"}))
    fristname=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    brith=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    email=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )

    def clean(self):
        password = self.cleaned_data.get("password")
        confirmpassword = self.cleaned_data.get("confirmpassword")
        if password != confirmpassword:
            return self.add_error("confirmpassword", "")
        return self.cleaned_data



class UserInfomationForm(forms.Form):
    username=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    surname=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )

    fristname=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    brith=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )
    email=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "layui-input"})
    )

