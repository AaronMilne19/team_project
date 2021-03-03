from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class City(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    NameSlug = models.SlugField(unique=True)
    Description = models.TextField()
    HeaderPicture = models.ImageField(blank=True, upload_to='city_pictures')
    Views = models.IntegerField(default=0)
    Added = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.NameSlug = slugify(self.Name)
        super(City, self).save(*args, **kwargs)
    
    class Meta(): 
        verbose_name_plural = 'Cities'    
    
    def __str__(self):
        return self.Name
        
class Attraction(models.Model):
    City = models.ForeignKey(City, on_delete=models.CASCADE)
    
    Name = models.CharField(max_length=150, unique=True)
    NameSlug = models.SlugField(unique=True)
    CoordinateNorth = models.DecimalField(max_digits=9, decimal_places=7)
    CoordinateEast = models.DecimalField(max_digits=9, decimal_places=7)
    Description = models.TextField()
    HeaderPicture = models.ImageField(blank=True, upload_to='attraction_pictures')
    Views = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.NameSlug = slugify(self.Name)
        super(Attraction, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.Name 
        
class MVUser(models.Model):
    DjangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    
    CityRatings = models.ManyToManyField(City, through='CityRatings')
    SavedAttractions = models.ManyToManyField(Attraction, related_name='saves')
    ReviewedAttractions = models.ManyToManyField(Attraction, through='AttractionReviews', through_fields=('UserReviewing', 'AttractionReviewed'), related_name='reviews')
    
    Name = models.CharField(max_length=50)
    Surname = models.CharField(max_length=50)
    DateOfBirth = models.DateField()
    Email = models.EmailField()
    Avatar = models.ImageField(blank=True, upload_to='profile_pictures')
    
    def __str__(self):
        return self.DjangoUser.username 
        
class CityRatings(models.Model):
    CityRated = models.ForeignKey(City, on_delete=models.CASCADE)
    UserRating = models.ForeignKey(MVUser, on_delete=models.CASCADE) # SUGGESTION: we might want to keep ratings from deleted users, i.e. on_delete=models.SET_NULL
    
    Rating = models.PositiveSmallIntegerField()
    
class AttractionReviews(models.Model):
    Likes = models.ManyToManyField(MVUser, through='ReviewLikes', related_name='likers')
    
    AttractionReviewed = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    UserReviewing = models.ForeignKey(MVUser, on_delete=models.CASCADE) # SUGGESTION: we might want to keep reviews from deleted users as above
    
    
    Title = models.CharField(max_length=100)
    DateVisited = models.DateField()
    TimeTaken = models.DurationField()
    Comment = models.TextField()
    Rating = models.PositiveSmallIntegerField()
    Picture = models.ImageField(blank=True)
    DateAdded = models.DateTimeField(auto_now_add=True)
    
class ReviewLikes(models.Model):
    ReviewLiked = models.ForeignKey(AttractionReviews, on_delete=models.CASCADE)
    UserLiking = models.ForeignKey(MVUser, on_delete=models.CASCADE) # SUGGESTION: we might want to keep likes from deleted users as above
    
    Like = models.BooleanField()
    
    
        


    

    

