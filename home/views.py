from django.shortcuts import render
from home.models import City, Attraction

from home.models import City, Attraction, AttractionReviews

# Create your views here.
def homepage(request):
    ctx = {}
    ctx['cities'] = City.objects.order_by('-Views')[:10]
    ctx['attractions'] = Attraction.objects.order_by('-Views')[:10]
    return render(request, 'homepage.html', context=ctx)


def citypage(request, NameSlug, sortBy):
    ctx = {}
    city = City.objects.get(NameSlug=NameSlug)

    # increase city view count
    city.Views = city.Views + 1
    city.save()

    ctx['city'] = city
    if sortBy.lower() == "views":
        ctx['attractions'] = Attraction.objects.order_by('-Views')
        ctx['dropdown_msg'] = 'Most Popular'
    # elif sortBy.lower() == "rating":
    #     ctx['attractions'] = Attraction.objects.order_by('-Views') # sort by average rating
    #     ctx['dropdown_msg'] = 'Top Rated'
    # elif sortBy.lower() == "date":
    #     ctx['attractions'] = Attraction.objects.order_by('-Views') # sort by date
    #     ctx['dropdown_msg'] = 'Newest First'
    else:
        ctx['attractions'] = Attraction.objects.all()
        ctx['dropdown_msg'] = 'Sorted By:'
    


    # don't look at comments below

    # if(request.user):
    #     my_rating =  AttractionReviews.objects.filter(UserReviewing=request.user).first()

    # ratings = AttractionRatings.objects.filter(CityRated=city)

    # ratings_sum = 0
    # ratings_ave = 0
    # ratings_count = ratings.count()
    # if(ratings_count>0):
    #     for rating in ratings:
    #         ratings_sum += rating.Rating
    #     ratings_ave = rating.Rating/ratings.count()
    # ctx['avg_rating'] = ratings_ave + 0.5


    return render(request, 'citypage.html', context=ctx)

