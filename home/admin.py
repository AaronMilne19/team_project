from django.contrib import admin
from home.models import City, Attraction, MVUser, CityRatings, AttractionReviews, ReviewLikes
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'NameSlug':('Name',)}
    
class AttractionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'NameSlug':('Name',)}

# class MVuserAdmin(admin.ModelAdmin):
#     list_display = ['Surname']




admin.site.register(City, CityAdmin)
admin.site.register(Attraction, AttractionAdmin)

admin.site.register(CityRatings)
admin.site.register(AttractionReviews)
admin.site.register(ReviewLikes)