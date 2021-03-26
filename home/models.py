from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class City(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    NameSlug = models.SlugField(unique=True)
    Description = models.TextField()
    HeaderPicture = models.ImageField(upload_to='city_pictures', null=True)
    Views = models.IntegerField(default=0)
    Added = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.NameSlug = slugify(self.Name)
        super(City, self).save(*args, **kwargs)
        
    def getAverageRating(self):
        return CityRatings.objects.filter(CityRated=self).aggregate(models.Avg('Rating'))['Rating__avg'] 
    
    class Meta(): 
        verbose_name_plural = 'Cities'    
    
    def __str__(self):
        return self.Name
 
 
class Attraction(models.Model):
    City = models.ForeignKey(City, on_delete=models.CASCADE)
    
    Name = models.CharField(max_length=150, unique=True)
    NameSlug = models.SlugField(unique=True)
    CoordinateNorth = models.DecimalField(max_digits=20, decimal_places=18)
    CoordinateEast = models.DecimalField(max_digits=20, decimal_places=18)
    Description = models.TextField()
    HeaderPicture = models.ImageField(upload_to='attraction_pictures', null=True)
    Views = models.IntegerField(default=0)
    Added = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.NameSlug = slugify(self.Name)
        super(Attraction, self).save(*args, **kwargs)
        
    def getAverageRating(self):
        return AttractionReviews.objects.filter(AttractionReviewed=self).aggregate(models.Avg('Rating'))['Rating__avg']
        
    def getUsersRating(self, user):
        if (user.is_authenticated):
          mvuser = MVUser.objects.get(DjangoUser=user)
          if AttractionReviews.objects.filter(AttractionReviewed=self, UserReviewing=mvuser).exists():
              return AttractionReviews.objects.get(AttractionReviewed=self, UserReviewing=mvuser).Rating
        return 0
        
    def getAverageTimeSpent(self):
        avgTimeTaken = AttractionReviews.objects.filter(AttractionReviewed=self).aggregate(models.Avg('TimeTaken'))['TimeTaken__avg']
        hours, remainder = divmod(avgTimeTaken.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return { 'hours': hours, 'minutes': minutes }
    
    def __str__(self):
        return self.Name 
 
 
class MVUser(models.Model):
    DjangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    
    CityRatings = models.ManyToManyField(City, through='CityRatings')
    SavedAttractions = models.ManyToManyField(Attraction, related_name='saves')
    ReviewedAttractions = models.ManyToManyField(Attraction, through='AttractionReviews', through_fields=('UserReviewing', 'AttractionReviewed'), related_name='reviews')
    
    Name = models.CharField(max_length=50, null=True)
    Surname = models.CharField(max_length=50, null=True)
    DateOfBirth = models.DateField(null=True)
    Avatar = models.ImageField(upload_to='profile_pictures', null=True, blank=True,default="/static/profile_pictures/default.png")
    
    def save(self, *args, **kwargs):
        if (self.Avatar == '' or self.Avatar == None): 
            self.Avatar = 'profile_pictures/default.png'
        super(MVUser, self).save(*args, **kwargs)
    
    class Meta(): 
        verbose_name_plural = 'MustVisit Users' 
    
    def __str__(self):
        return self.DjangoUser.username 

        
class CityRatings(models.Model):
    CityRated = models.ForeignKey(City, on_delete=models.CASCADE)
    UserRating = models.ForeignKey(MVUser, on_delete=models.CASCADE) # SUGGESTION: we might want to keep ratings from deleted users, i.e. on_delete=models.SET_NULL
    
    #User can rate between 1-5 if value 0 then city not been rated.
    Rating = models.PositiveSmallIntegerField(default=0,
        validators = [MaxValueValidator(5), MinValueValidator(0)]
    )
    
    class Meta(): 
        verbose_name_plural = 'City Ratings'       
    
    def __str__(self):
        return '%s rates %s %i/5' % (str(self.UserRating), str(self.CityRated), self.Rating)
 
 
class AttractionReviews(models.Model):
    Likes = models.ManyToManyField(MVUser, through='ReviewLikes', related_name='likers')
    
    AttractionReviewed = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    UserReviewing = models.ForeignKey(MVUser, on_delete=models.CASCADE) # SUGGESTION: we might want to keep reviews from deleted users as above
    
    
    Title = models.CharField(max_length=100)
    DateVisited = models.DateField(null=True)
    TimeTaken = models.DurationField(null=True)
    Comment = models.TextField()
    Rating = models.PositiveSmallIntegerField()
    Picture = models.ImageField(null=True)
    DateAdded = models.DateTimeField(auto_now_add=True)
    
    class Meta(): 
        verbose_name_plural = 'Attraction Reviews'
    
    def __str__(self): 
        return '%s\'s review of %s (%i/5)' % (str(self.UserReviewing), str(self.AttractionReviewed), self.Rating)
        
        
    
class ReviewLikes(models.Model):
    ReviewLiked = models.ForeignKey(AttractionReviews, on_delete=models.CASCADE)
    UserLiking = models.ForeignKey(MVUser, on_delete=models.CASCADE) # SUGGESTION: we might want to keep likes from deleted users as above
    
    Like = models.BooleanField()
    
    class Meta(): 
        verbose_name_plural = 'Review Likes'
    
    def __str__(self):
        if self.Like:
            return '%s liked %s' % (str(self.UserLiking), str(self.ReviewLiked))
        else:
            return '%s disliked %s' % (str(self.UserLiking), str(self.ReviewLiked))
            
#returns float Rating__avg            


#returns float Rating__avg    


# returns tuple (home.models.Attraction, avg_rating)    
def TopCities(howMany):
    top = CityRatings.objects.values('CityRated').annotate(avg_rating=models.Avg('Rating')).order_by('-avg_rating')[:howMany]
    
    return_top = []
    for city in top:
        return_top += [(City.objects.get(id=city['CityRated']), city['avg_rating'])]
    return return_top 
    

# returns tuple (home.models.Attraction, avg_rating)
def TopAttractions(howMany):
    top = AttractionReviews.objects.values('AttractionReviewed').annotate(avg_rating=models.Avg('Rating')).order_by('-avg_rating')[:howMany]
    
    return_top = []
    for attr in top:
        return_top += [(Attraction.objects.get(id=attr['AttractionReviewed']), attr['avg_rating'])]
    return return_top 