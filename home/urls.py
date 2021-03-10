from django.urls import include, path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('cities/<slug:NameSlug>/', views.citypage, name="citypage"),
]