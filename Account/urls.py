from django.urls import include, path,re_path
from Account import views

app_name = 'Account'

urlpatterns = [
    path('sign-up/', views.register, name="sign-up"),
    path('login/', views.login, name="login"),
    re_path(r'^$', views.account, name="account"),
    path('setting/', views.upload_avatar, name="setting"),
    path('loginout/', views.loginout, name="loginout")
]