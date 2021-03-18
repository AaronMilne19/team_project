
from django.shortcuts import render, redirect
from home.models import City, Attraction, AttractionReviews, CityRatings, MVUser
from django.http import Http404, JsonResponse
from random import randint
from django.contrib.auth.decorators import login_required

# Create your views here.

def contactus(request):
    ctx = {}
    return render(request, 'contact.html', context=ctx)

def homepage(request):
    ctx = {}
    ctx['cities'] = City.objects.order_by('-Views')[:10]
    ctx['attractions'] = Attraction.objects.order_by('-Views')[:10]
    return render(request, 'homepage.html', context=ctx)


@login_required
def rating(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        val = request.POST.get('score')
        obj = CityRatings.objects.get(CityRated=name)
        obj.UserRating = request.user
        obj.Rating = val
        obj.save()
        return JsonResponse({'success':'true', 'score':val}, safe=False)
    return JsonResponse({'success':'false'})


def send_somewhere_random(request):
    #get array of all attractions and then choose a random one from that and redirect user to it.
    rand_attractions = Attraction.objects.all()
    count = rand_attractions.count()

    if count == 0:
        raise Http404

    rand_num = randint(0, count-1)
    rand_attraction = rand_attractions[rand_num]

    return redirect('/home/cities/' + rand_attraction.City.NameSlug + '/' + rand_attraction.NameSlug + '/')


def citypage(request, NameSlug, sortBy):
    ctx = {}
    city = City.objects.get(NameSlug=NameSlug)

    # increase city view count
    city.Views = city.Views + 1
    city.save()
    ctx['city'] = city

    attractions = Attraction.objects.filter(City=city)
    if sortBy.lower() == "views":
        ctx['attractions'] = attractions.order_by('-Views')
        ctx['dropdown_msg'] = 'Most Popular'
    # elif sortBy.lower() == "rating":
    #     ctx['attractions'] = attractions.order_by('-Views') # sort by average rating
    #     ctx['dropdown_msg'] = 'Top Rated'
    # elif sortBy.lower() == "date":
    #     ctx['attractions'] = attractions.order_by('-Views') # sort by date
    #     ctx['dropdown_msg'] = 'Newest First'
    else:
        ctx['attractions'] = attractions.all()
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


