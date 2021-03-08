from django.shortcuts import render

from home.models import City, Attraction, AttractionReviews

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html', context={})

def citypage(request, NameSlug, sortBy):
    ctx = {}

    city = City.objects.get(NameSlug=NameSlug)
    ctx['city'] = city
    if sortBy.lower() == "views":
        ctx['attractions'] = Attraction.objects.order_by('-Views')
        ctx['dropdown_msg'] = 'Most Popular'
    # elif sortBy.lower() == "rating":
    #     ctx['attractions'] = Attraction.objects.order_by('-Views') # sort by average rating
    #     ctx['dropdown_msg'] = 'Top Rated'
    # elif sortBy.lower() == "date":
    #     ctx['attractions'] = Attraction.objects.order_by('-Views') # sort by date
    #     ctx['dropdown_msg'] = 'Newest first'
    else:
        ctx['attractions'] = Attraction.objects.all()
    
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