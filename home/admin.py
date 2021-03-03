from django.contrib import admin
from home.models import City, Attraction, MVUser, CityRatings, AttractionReviews, ReviewLikes

admin.site.register(City)
admin.site.register(Attraction)
admin.site.register(MVUser)
admin.site.register(CityRatings)
admin.site.register(AttractionReviews)
admin.site.register(ReviewLikes)