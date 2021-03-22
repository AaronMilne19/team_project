from django.urls import include, path
from home import views


app_name = 'home'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('contact/', views.contactus, name="contact"),
    path('cities/<slug:NameSlug>/<str:sortBy>/', views.citypage, name="citypage"),
    path('random/', views.send_somewhere_random, name="random"),
    path('rating/', views.rating, name='rating'),
    path('myattractions/', views.myattractions, name="myattractions"),
    path('leave-a-review/', views.leave_a_review, name="leave_a_review"),

]