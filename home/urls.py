from django.urls import include, path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('contact/', views.contactus, name="contact"),
    path('cities/<slug:NameSlug>/<str:sortBy>/', views.citypage, name="citypage"),

]