
from django.shortcuts import render, redirect
from home.models import City, Attraction, AttractionReviews, CityRatings, MVUser, User
from django.http import Http404, JsonResponse
from random import randint
from django.contrib.auth.decorators import login_required


# Create your views here.

def contactus(request):
    ctx = {}
    return render(request, 'contact.html', context=ctx)

def homepage(request):
    ctx = {}
    cities = City.objects.all()

    ctx['cities'] = sorted(cities.all(), key=lambda a: -a.getAverageRating())
    ctx['attractions'] = Attraction.objects.order_by('-Views')[:10]
    return render(request, 'homepage.html', context=ctx)


@login_required
def rating(request):
    if request.method == 'POST':
        city_name = request.POST.get('name')
        val = request.POST.get('score')

        city = City.objects.get(NameSlug=city_name)
        user = MVUser.objects.get(DjangoUser=request.user)

        try:
            obj = CityRatings.objects.get(UserRating=user, CityRated=city)
            obj.Rating = val
            obj.save()
        except CityRatings.DoesNotExist:
            obj = CityRatings(UserRating=user, CityRated=city, Rating=val)
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
    elif sortBy.lower() == "popular":
        ctx['attractions'] = sorted(attractions.all(), key=lambda a: -a.getAverageRating()) # sort by average rating
        ctx['dropdown_msg'] = 'Top Rated'
    elif sortBy.lower() == "date":
        ctx['attractions'] = attractions.order_by('-Added') # sort by date
        ctx['dropdown_msg'] = 'Newest First'
    else:
        ctx['attractions'] = attractions.all()
        ctx['dropdown_msg'] = 'Sorted By:'
    

    return render(request, 'citypage.html', context=ctx)

@login_required
def myattractions(request):
    print(request.user)
    user = MVUser.objects.get(DjangoUser=request.user)
    attractions = user.SavedAttractions.order_by("City")
    ctx={}
    ctx["attractions"] = attractions.all()

    cities = []
    for attraction in ctx["attractions"]:
        city = attraction.City
        if city not in cities:
            cities.append(city)
    
    ctx["cities"] = cities

    
    return render(request, 'myattractions.html', context=ctx)

