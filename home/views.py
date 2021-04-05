from django.shortcuts import render, redirect
from home.models import City, Attraction, AttractionReviews, CityRatings, MVUser, User
from django.http import Http404, JsonResponse
from random import randint
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from home.forms import ReviewForm
from django.urls import reverse



# Create your views here.

def contactus(request):
    ctx = {}
    return render(request, 'contact.html', context=ctx)


def homepage(request):
    ctx = {}
    cities = City.objects.all()
    attractions = Attraction.objects.order_by('-Views')[:10]

    ctx['cities'] = sorted(cities.all(), key=lambda a: -a.getAverageRating())
    ctx['attractions'] = attractions

    if request.user.is_authenticated:
        user = MVUser.objects.get(DjangoUser=request.user)
        ctx['city_ratings'] = CityRatings.objects.filter(UserRating=user)
        
    ctx['center'] = { 'lat': attractions.aggregate(Avg('CoordinateNorth'))['CoordinateNorth__avg'], 'lng': attractions.aggregate(Avg('CoordinateEast'))['CoordinateEast__avg'] } 

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

            #If user clicks same star button again then delete the rating and refresh the page
            if obj.Rating == int(val):
                obj.delete()
                return JsonResponse({'success':'true', 'score':0}, safe=False)

            else:
                obj.Rating = val
                obj.save()

        except CityRatings.DoesNotExist:
            obj = CityRatings(UserRating=user, CityRated=city, Rating=val)
            obj.save()

        return JsonResponse({'success':'true', 'score':val}, safe=False)
    return JsonResponse({'success':'false'})


@login_required
def saveAttraction(request):
    if request.method == 'POST':
        attraction_name = request.POST.get('name')

        attraction = Attraction.objects.get(NameSlug=attraction_name)
        user = MVUser.objects.get(DjangoUser=request.user)

        for a in user.SavedAttractions.all():
            if a == attraction:
                user.SavedAttractions.remove(attraction)
                user.save()
                return JsonResponse({'success':'true', 'value':0})

        user.SavedAttractions.add(attraction)
        user.save()

        return JsonResponse({'success':'true', 'value':1})
    return JsonResponse({'success':'false'})


def send_somewhere_random(request):
    #get array of all attractions and then choose a random one from that and redirect user to it.
    rand_attractions = Attraction.objects.all()
    count = rand_attractions.count()

    if count == 0:
        raise Http404

    rand_num = randint(0, count-1)
    rand_attraction = rand_attractions[rand_num]

    return redirect('/home/cities/' + rand_attraction.City.NameSlug + '/attractions/' + rand_attraction.NameSlug + '/')


def citypage_unsorted(request, NameSlug):
    return citypage(request, NameSlug, "")


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

    if request.user.is_authenticated:
        user = MVUser.objects.get(DjangoUser=request.user)
        ctx['saved_attractions'] = user.SavedAttractions.all()
        
    ctx['center'] = { 'lat': attractions.aggregate(Avg('CoordinateNorth'))['CoordinateNorth__avg'], 'lng': attractions.aggregate(Avg('CoordinateEast'))['CoordinateEast__avg'] }


    return render(request, 'citypage.html', context=ctx)


def attractionpage(request, CityNameSlug, AttractionNameSlug):
    city = City.objects.get(NameSlug=CityNameSlug)
    attraction = Attraction.objects.get(City=city, NameSlug=AttractionNameSlug)
    
    ctx = {}
    ctx['city'] = city
    ctx['attraction'] = attraction
    ctx['reviews'] = AttractionReviews.objects.filter(AttractionReviewed=attraction)
    ctx['users_rating'] = attraction.getUsersRating(request.user)

    if request.user.is_authenticated:
        user = MVUser.objects.get(DjangoUser=request.user)
        try:
            ctx['my_review'] = AttractionReviews.objects.get(UserReviewing=user, AttractionReviewed=attraction)
        except Exception:
            ctx['my_review'] = None
        finally:
            for attr in user.SavedAttractions.all():
                if attr == attraction:
                    ctx['saved_attraction'] = attraction
    
    return render(request, 'attractionpage.html', context=ctx)


def view_review(request, CityNameSlug, AttractionNameSlug, ReviewIdSlug):
    review = AttractionReviews.objects.get(id=ReviewIdSlug)
    city = City.objects.get(NameSlug=CityNameSlug)
    attraction = Attraction.objects.get(City=city, NameSlug=AttractionNameSlug)

    ctx = {}
    ctx['city'] = city
    ctx['attraction'] = attraction
    ctx['review'] = review
    ctx['reviewer'] = review.UserReviewing
    ctx['reviewer_rating'] = review.Rating

    duration = str(review.TimeTaken).split(':')
    ctx['time'] = duration

    if request.user.is_authenticated:
        user = MVUser.objects.get(DjangoUser=request.user)
        ctx['users_rating'] = attraction.getUsersRating(request.user)
        try:
            ctx['my_review'] = AttractionReviews.objects.get(UserReviewing=user, AttractionReviewed=attraction)
        except Exception:
            ctx['my_review'] = None
        finally:
            for attr in user.SavedAttractions.all():
                if attr == attraction:
                    ctx['saved_attraction'] = attraction

    return render(request, 'view_review.html', context=ctx)


@login_required
def myattractions(request):
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

@login_required
def myreviews(request):
    user = MVUser.objects.get(DjangoUser=request.user)
    ctx={}
    ctx["reviews"] = AttractionReviews.objects.filter(UserReviewing=user).order_by('-DateAdded').all()

    return render(request, 'myreviews.html', context=ctx)


@login_required
def leave_a_review(request, CityNameSlug, AttractionNameSlug):
    city = City.objects.get(NameSlug=CityNameSlug)
    attraction = Attraction.objects.get(City=city, NameSlug=AttractionNameSlug)
    user = MVUser.objects.get(DjangoUser=request.user)

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            try:
                AttractionReviews.objects.get(UserReviewing=user, AttractionReviewed=attraction).delete()
            finally:
                review = form.save(commit=False)
                review.AttractionReviewed = attraction
                review.UserReviewing = user
                review.save()

                return redirect(reverse('home:attractionpage', kwargs={'CityNameSlug': CityNameSlug, 'AttractionNameSlug': AttractionNameSlug}))
        else:
            print(form.errors)


    ctx = {}
    ctx['city'] = city
    ctx['attraction'] = attraction
    ctx['form'] = form
    ctx['users_rating'] = attraction.getUsersRating(request.user)

    try:
        ctx['my_review'] = AttractionReviews.objects.get(UserReviewing=user, AttractionReviewed=attraction)
    except Exception:
        ctx['my_review'] = None
    finally:
        for attr in user.SavedAttractions.all():
            if attr == attraction:
                ctx['saved_attraction'] = attraction

        return render(request, 'leave_a_review.html', context=ctx)


@login_required
def remove_review(request, CityNameSlug, AttractionNameSlug):
    user = MVUser.objects.get(DjangoUser=request.user)
    attraction = Attraction.objects.get(NameSlug=AttractionNameSlug)

    review = AttractionReviews.objects.get(UserReviewing=user, AttractionReviewed=attraction)
    review.delete()

    return redirect(reverse('home:attractionpage', kwargs={'CityNameSlug': CityNameSlug, 'AttractionNameSlug': AttractionNameSlug}))