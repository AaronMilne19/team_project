from django.shortcuts import render

from home.models import City, Attraction

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html', context={})

def citypage(request, NameSlug):
    ctx = {}
    ctx['city'] = City.objects.get(NameSlug=NameSlug)
    ctx['attractions'] = Attraction.objects.order_by('-Views')
    return render(request, 'citypage.html', context=ctx)