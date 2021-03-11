from django.contrib import admin
from home.models import City, Attraction, MVUser, CityRatings, AttractionReviews, ReviewLikes

class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'NameSlug':('Name',)}
    
class AttractionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'NameSlug':('Name',)}

admin.site.register(City, CityAdmin)
admin.site.register(Attraction, AttractionAdmin)
admin.site.register(MVUser)
admin.site.register(CityRatings)
admin.site.register(AttractionReviews)
admin.site.register(ReviewLikes)