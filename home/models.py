from django.db import models
from django.template.defaultfilters import slugify

class City(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    NameSlug = models.SlugField(unique=True)
    Description = models.TextField()
    HeaderPicture = models.ImageField()
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
    HeaderPicture = models.ImageField()
    Views = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.NameSlug = slugify(self.Name)
        super(Attraction, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.Name
    

    

