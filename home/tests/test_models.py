from django.test import TestCase, Client
from home.models import City, Attraction, CityRatings, AttractionReviews, User, MVUser
from django.db import IntegrityError
import datetime

class TestModels(TestCase):

    def setUp(self):
        self.city1 = City.objects.create(
            Name='Glasgow', Description="It's an amazing city.", Views = 500
        ) 


        self.user1 = User.objects.create(
            username="Sam", email="sam@gmail.com"
        )

        self.mvuser1 = MVUser.objects.create(
            DjangoUser=self.user1
        )

        self.attraction1 = Attraction.objects.create(
            City=self.city1, Name="John Williamson Building", Description="The best building in Glasgow",
            Views=100000, Added = datetime.date.today, CoordinateNorth=0, CoordinateEast=0
        )
    
    def test_city_is_assigned_slug_on_creation(self):
        self.assertEquals(self.city1.NameSlug, 'glasgow')
    
    def test_attraction_is_assigned_slug_on_creation(self):
        self.assertEquals(self.attraction1.NameSlug, 'john-williamson-building')

    def test_city_get_average_rating_with_no_ratings(self):
        self.assertEquals(self.city1.getAverageRating(), None)

    def test_city_get_average_rating_with_existing_ratings(self):

        rating1 = CityRatings.objects.create( 
            CityRated=self.city1, UserRating= self.mvuser1, Rating = 4,
        )

        user2 = User.objects.create(
            username="Emily", email="emily@gmail.com",
        )
        mvuser2 = MVUser.objects.create(
            DjangoUser=user2,
        )

        rating2 = CityRatings.objects.create(
            CityRated=self.city1, UserRating= mvuser2, Rating = 5,
        )

        self.assertEquals(self.city1.getAverageRating(), 4.5)

    def test_attraction_get_average_rating_with_no_ratings(self):
        self.assertEquals(self.attraction1.getAverageRating(), None)

    def test_city_object_uniqueness(self):
        
        with self.assertRaises(Exception) as exception:
            name = self.city1.Name
            description = 'A short description'
            views = 30
            
            city2 = City.objects.create(
                Name=name, Description=description, Views=views,
            )
        
        self.assertEqual(IntegrityError, type(exception.exception))

    def test_user_object_uniqueness(self):
        
        with self.assertRaises(Exception) as exception:
            username = self.user1.username
            email = 'email@email.com'
            
            city2 = User.objects.create(
                username=username, email=email
            )
        
        self.assertEqual(IntegrityError, type(exception.exception))
    
    def test_mvuser_object_uniqueness(self):
        
        with self.assertRaises(Exception) as exception:
            mvuser2 = MVUser.objects.create(
                DjangoUser=self.user1
            )
        
        self.assertEqual(IntegrityError, type(exception.exception))

    def test_attraction_object_uniqueness(self):
        with self.assertRaises(Exception) as exception:
            attraction2 = Attraction.objects.create(
                Name=self.attraction1.Name, City=self.city1, Description="Amazing Building", Views=42342,
                Added=datetime.date.today, CoordinateNorth=1,CoordinateEast=1 
            )
        
        self.assertEqual(IntegrityError, type(exception.exception))

