from django.urls import include, path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('cities/<slug:NameSlug>/<str:sortBy>/', views.citypage, name="citypage"),
    path('random/', views.send_somewhere_random, name="random"),

]