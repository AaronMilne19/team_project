from django.test import TestCase, Client
from django.urls import reverse
from home.models import City, CityRatings, MVUser, User, Attraction
import json
import datetime

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()

        self.city1 =  City.objects.create(
            Name='Glasgow', Description="It's an amazing city.", Views = 50
        ) 

        self.user1 = User.objects.create(
            username="Sam", email="sam@gmail.com"
        )

        self.mvuser1 = MVUser.objects.create(
            DjangoUser=self.user1
        )

        self.cityrating1 = CityRatings.objects.create(
            CityRated = self.city1, UserRating=self.mvuser1, Rating = 4
        )


        self.home_url = reverse('home:homepage')
        self.city_url = reverse('home:citypage', args=['glasgow','views'])
        self.contact_url = reverse('home:contact')
        self.rating = reverse('home:rating')

        

    def test_home(self):

        # test city object in the view
        city_names = ['Paris', 'London', 'Berlin', 'Moscow', 'New York City']
        views_count = [25, 35, 25, 40, 55]
        ratings = [1,2,4,3,5]

        for count in range(5):
            city = City.objects.create(
                Name=city_names[count], Description="It's an amazing city.", Views = views_count[count]
            ) 
            cityrating = CityRatings.objects.create(
                CityRated = city, UserRating=self.mvuser1, Rating = ratings[count]
            )
        
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertTemplateUsed(response, 'base.html')
        
        self.assertContains(response, city_names[0])
      
        self.assertEquals(response.context[-1]['cities'][0].Name, 'New York City')
        self.assertEquals(response.context[-1]['cities'][-1].Name, 'Paris')

        # test if send me somewhere random is on the page
        self.assertContains(response, 'Send Me Somewhere Random!</button>') 

    def test_city(self):
        
        for count in range(5):
            attractions = Attraction.objects.create(
                Name="attraction"+str(count), Description="It's an amazing attraction.", Views = count, City=self.city1,
                CoordinateNorth = count, CoordinateEast= -count
            
            ) 
        
        
        response = self.client.get(self.city_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'citypage.html')
        self.assertTemplateUsed(response, 'base.html')

        self.assertContains(response, 'Glasgow City')

        views = 2 ** 64 
        for i in range(len(response.context[-1]['attractions'])):
            self.assertContains(response, response.context[-1]['attractions'][i].Name)
            self.assertGreaterEqual(views, response.context[-1]['attractions'][i].Views)
            views = response.context[-1]['attractions'][i].Views # check descending order of views
        





    def test_contactus(self):
        response = self.client.get(self.contact_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, '<input class="button" type="submit" value="Send">') # checks if send button exists
        self.assertContains(response, '<form') # checks if form is created
    

        



