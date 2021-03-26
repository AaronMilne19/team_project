from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import homepage, contactus, rating, saveAttraction, citypage, citypage_unsorted, attractionpage, myattractions, leave_a_review, send_somewhere_random, saveAttraction

class TestUrls(SimpleTestCase):

    def test_homepage_url_is_resolved(self):
        url = reverse('home:homepage')
        self.assertEqual(resolve(url).func, homepage)
    
    def test_citypage_unsorted_url_is_resolved(self):
        url = reverse('home:citypage_unsorted', args=['some-city'])
        self.assertEqual(resolve(url).func, citypage_unsorted)
    
    def test_citypage_url_is_resolved(self):
        url = reverse('home:citypage', args=['some-city','some-sort'])
        self.assertEqual(resolve(url).func, citypage)
    
    def test_contactus_url_is_resolved(self):
        url = reverse('home:contact')
        self.assertEqual(resolve(url).func, contactus)

    def test_rating_url_is_resolved(self):
        url = reverse('home:rating')
        self.assertEqual(resolve(url).func, rating)

    def test_attraction_url_is_resolved(self):
        url = reverse('home:attractionpage', args=['some-city','some-attraction'])
        self.assertEqual(resolve(url).func, attractionpage)
    
    def test_save_attraction_url_is_resolved(self):
        url = reverse('home:save')
        self.assertEqual(resolve(url).func, saveAttraction)

    def test_send_random_url_is_resolved(self):
        url = reverse('home:random')
        self.assertEqual(resolve(url).func, send_somewhere_random)

    def test_my_attractions_url_is_resolved(self):
        url = reverse('home:myattractions')
        self.assertEqual(resolve(url).func, myattractions)
    
    # def test_leave_a_review_url_is_resolved(self):
    #     url = reverse('home:random')
    #     self.assertEqual(resolve(url).func, leave_a_review)
