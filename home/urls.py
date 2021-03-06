from django.urls import include, path
from home import views


app_name = 'home'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('contact/', views.contactus, name="contact"),
    path('cities/<slug:CityNameSlug>/attractions/<slug:AttractionNameSlug>/', views.attractionpage, name="attractionpage"),
    path('cities/<slug:NameSlug>/<str:sortBy>/', views.citypage, name="citypage"),
    path('cities/<slug:NameSlug>/', views.citypage_unsorted, name="citypage_unsorted"),
    path('random/', views.send_somewhere_random, name="random"),
    path('rating/', views.rating, name='rating'),
    path('save/', views.saveAttraction, name='save'),
    path('myattractions/', views.myattractions, name="myattractions"),
    path('cities/<slug:CityNameSlug>/attractions/<slug:AttractionNameSlug>/leave-a-review/', views.leave_a_review, name="leave_a_review"),
    path('myreviews/', views.myreviews, name="myreviews"),
    path('cities/<slug:CityNameSlug>/attractions/<slug:AttractionNameSlug>/remove-review/', views.remove_review, name="remove_review"),
    path('cities/<slug:CityNameSlug>/attractions/<slug:AttractionNameSlug>/reviews/<slug:ReviewIdSlug>', views.view_review, name="view_review"),
    path('cities/<slug:CityNameSlug>/attractions/<slug:AttractionNameSlug>/reviews_feed/<str:sortBy>', views.attraction_reviews_feed, name="attraction_reviews_feed"),
    path('cities/<slug:CityNameSlug>/attractions/<slug:AttractionNameSlug>/modify_review_like/<int:id>/<str:action>', views.modify_review_like, name="modify_review_like"),
]