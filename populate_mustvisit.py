import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_project.settings')
import random

import django
django.setup()
from home.models import City, Attraction, MVUser, CityRatings, AttractionReviews, ReviewLikes
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from django.template.defaultfilters import slugify

from datetime import datetime, date, timedelta

@transaction.atomic
def populate():
    superuser = User.objects.get_or_create(username='admin', is_active=True, is_superuser=True, is_staff=True)[0]
    superuser.set_password('1491625')
    superuser.save()

    cities = [
    {
        'Name': 'Glasgow', 
        'Description': "Glasgow is a port city on the River Clyde in Scotland's western Lowlands. It's famed for its Victorian and art nouveau architecture, a rich legacy of the city's 18th–20th-century prosperity due to trade and shipbuilding. Today it's a national cultural hub, home to institutions including the Scottish Opera, Scottish Ballet and National Theatre of Scotland, as well as acclaimed museums and a thriving music scene.", 
        },
    {
        'Name': 'London', 
        'Description': "London, the capital of England and the United Kingdom, is a 21st-century city with history stretching back to Roman times. At its centre stand the imposing Houses of Parliament, the iconic ‘Big Ben’ clock tower and Westminster Abbey, site of British monarch coronations. Across the Thames River, the London Eye observation wheel provides panoramic views of the South Bank cultural complex, and the entire city.",
        },
    {
        'Name': 'Paris', 
        'Description': "Paris, France's capital, is a major European city and a global center for art, fashion, gastronomy and culture. Its 19th-century cityscape is crisscrossed by wide boulevards and the River Seine. Beyond such landmarks as the Eiffel Tower and the 12th-century, Gothic Notre-Dame cathedral, the city is known for its cafe culture and designer boutiques along the Rue du Faubourg Saint-Honoré.",
        },
    {
        'Name': 'Dublin', 
        'Description': "Dublin, capital of the Republic of Ireland, is on Ireland’s east coast at the mouth of the River Liffey. Its historic buildings include Dublin Castle, dating to the 13th century, and imposing St Patrick’s Cathedral, founded in 1191. City parks include landscaped St Stephen’s Green and huge Phoenix Park, containing Dublin Zoo. The National Museum of Ireland explores Irish heritage and culture.", 
        },
    {
        'Name': 'Inverness',
        'Description': "Inverness is a city on Scotland’s northeast coast, where the River Ness meets the Moray Firth. It's the largest city and the cultural capital of the Scottish Highlands. Its Old Town features 19th-century Inverness Cathedral, the mostly 18th-century Old High Church and an indoor Victorian Market selling food, clothing and crafts. The contemporary Inverness Museum and Art Gallery traces local and Highland history.", 
        },
    {
        'Name': 'Edinburgh',
        'Description': "Edinburgh is Scotland's compact, hilly capital. It has a medieval Old Town and elegant Georgian New Town with gardens and neoclassical buildings. Looming over the city is Edinburgh Castle, home to Scotland’s crown jewels and the Stone of Destiny, used in the coronation of Scottish rulers. Arthur’s Seat is an imposing peak in Holyrood Park with sweeping views, and Calton Hill is topped with monuments and memorials.", 
        }, 
    ]
 
    # IF YOU WANT TO PUT IN YOUR OWN ATTRACTIONS:   
    # If you're creating attractions for a new city, first check that you've put the city into the cities dictionary, otherwise the script won't populate its attractions!
    # For the real-word attractions data, I first google the attraction and fill in the name and description from the overview table that pops up on the right-hand side
    # Then I put the attraction into google maps, and from the right-click menu of the pin (marking the location of the attarction) copy-paste the north and east coordinates
    # this is the dictionary template: {'Name':'', 'N':, 'E':, 'Description': ""},
    attractions = {
        'Glasgow': [
            {'Name':'The University of Glasgow', 'N':55.87364650680187, 'E':-4.284779892254786, 'Description': "The University of Glasgow is a public research university in Glasgow, Scotland. Founded by papal bull in 1451, it is the fourth-oldest university in the English-speaking world and one of Scotland's four ancient universities. Along with the universities of Edinburgh, Aberdeen, and St Andrews, the university was part of the Scottish Enlightenment during the 18th century."},
            {'Name':'Glasgow City Chambers', 'N':55.86124917973871, 'E':-4.248861476014532, 'Description': "The City Chambers or Municipal Buildings in Glasgow, Scotland, has functioned as the headquarters of Glasgow City Council since 1996, and of preceding forms of municipal government in the city since 1889. It is located on the eastern side of the city's George Square. It is a Category A listed building."},
            {'Name':'John H. Williamson Building', 'N':55.873720376930635, 'E':-4.2926111155866495, 'Description': 'The most beautiful building on the University of Glasgow campus, bearing the name of a prominent local lecturer who has a particularly handsome cat.'},
        ],
        'London': [
            {'Name':'Tower of London', 'N':51.50827264339931, 'E':-0.07597075994915306, 'Description': "The Tower of London, officially Her Majesty's Royal Palace and Fortress of the Tower of London, is a historic castle on the north bank of the River Thames in central London."},
            {'Name':'Palace of Westminster', 'N':51.4996289854147, 'E':0.12479514193684446, 'Description': "The Palace of Westminster serves as the meeting place for both the House of Commons and the House of Lords, the two houses of the Parliament of the United Kingdom."},
            {'Name':'Big Ben', 'N':51.50089796097527, 'E':-0.12464493824182302, 'Description': "Big Ben is the nickname for the Great Bell of the striking clock at the north end of the Palace of Westminster; the name is frequently extended to refer to both the clock and the clock tower."},
            {'Name':"St. Paul's Cathedral", 'N':51.51405226084283, 'E':-0.09829695810141474, 'Description': "St Paul's Cathedral is an Anglican cathedral in London, United Kingdom, which, as the cathedral of the Bishop of London, serves as the mother church of the Diocese of London. It sits on Ludgate Hill at the highest point of the City of London and is a Grade I listed building."},
            {'Name':'Buckingham Palace', 'N':51.5031033625252, 'E':-0.14134798388275888, 'Description': "Buckingham Palace is the London residence and administrative headquarters of the monarch of the United Kingdom. Located in the City of Westminster, the palace is often at the centre of state occasions and royal hospitality. It has been a focal point for the British people at times of national rejoicing and mourning."},
            {'Name':'The British Museum', 'N':51.52168164494879, 'E':-0.12674520654520646, 'Description': "The British Museum, in the Bloomsbury area of London, England, is a public institution dedicated to human history, art and culture. Its permanent collection of some eight million works is among the largest and most comprehensive in existence, having been widely collected during the era of the British Empire."},       
        ],
        'Paris': [
            {'Name':'Eiffel Tower', 'N':48.85858184114911, 'E':2.2944383822733996, 'Description': "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower."},
            {'Name':'Arc de Triomphe', 'N':48.874038658582315, 'E':2.2950704129568464, 'Description': "The Arc de Triomphe de l'Étoile is one of the most famous monuments in Paris, France, standing at the western end of the Champs-Élysées at the centre of Place Charles de Gaulle, formerly named Place de l'Étoile—the étoile or \"star\" of the juncture formed by its twelve radiating avenues."},
            {'Name':'Tuileries Garden', 'N':48.863292290575785, 'E':2.3275984564000005, 'Description': "The Tuileries Garden is a public garden located between the Louvre and the Place de la Concorde in the 1st arrondissement of Paris, France. Created by Catherine de' Medici as the garden of the Tuileries Palace in 1564, it was eventually opened to the public in 1667 and became a public park after the French Revolution."},
            {'Name':'Louvre Museum', 'N':48.86216140052423, 'E':2.337883694522221, 'Description': "The Louvre, or the Louvre Museum, is the world's largest art museum and a historic monument in Paris, France, and is best known for being the home of the Mona Lisa. A central landmark of the city, it is located on the Right Bank of the Seine in the city's 1st arrondissement."},
            {'Name':'Notre-Dame Cathedral', 'N':48.85434186187135, 'E':2.3501073876768497, 'Description': "Notre-Dame de Paris, referred to simply as Notre-Dame, is a medieval Catholic cathedral on the Île de la Cité in the 4th arrondissement of Paris. The cathedral was consecrated to the Virgin Mary and considered to be one of the finest examples of French Gothic architecture."},
            {'Name':'Sacré-Cœur Basilica', 'N':48.886831564578586, 'E':2.343072111109849, 'Description': "The Basilica of the Sacred Heart of Paris, commonly known as Sacré-Cœur Basilica and often simply Sacré-Cœur, is a Roman Catholic church and minor basilica in Paris, France, dedicated to the Sacred Heart of Jesus. Sacré-Cœur Basilica is located at the summit of the butte Montmartre, the highest point in the city."},
        ],
        'Dublin': [
            {'Name':'Dublin Castle', 'N':53.343873872032944, 'E':-6.267713839336623, 'Description': "Dublin Castle is a major Irish government complex, conference centre, and tourist attraction, of significant historical importance. It is located off Dame Street in central Dublin. Until 1922 it was the seat of the British government's administration in Ireland."},
            {'Name':'Trinity College Dublin', 'N':53.34496968769554, 'E':-6.25460511337501, 'Description': "Trinity College, officially the College of the Holy and Undivided Trinity of Queen Elizabeth near Dublin, is the sole constituent college of the University of Dublin, a research university located in Dublin, Ireland."},
            {'Name':"St Patrick's Cathedral", 'N':53.34046028088291, 'E':-6.271685420022988, 'Description': "Saint Patrick's Cathedral in Dublin, Ireland, founded in 1191, is the national cathedral of the Church of Ireland. Christ Church Cathedral, also a Church of Ireland cathedral in Dublin, is designated as the local cathedral of the Diocese of Dublin and Glendalough."},       
        ],
        'Inverness': [
            {'Name':'Inverness Castle', 'N':57.476474557527204, 'E':-4.2253683983266335, 'Description': "Inverness Castle sits on a cliff overlooking the River Ness in Inverness, Scotland. The red sandstone structure, displaying an early castellated style, is the work of a few nineteenth-century architects."},
            {'Name':'Ness Islands', 'N':57.464784732670594, 'E':-4.229678577632959, 'Description': "The Ness Islands are situated on the River Ness, opposite the Bught Park, in the city of Inverness, Scotland. The first bridges to the islands were built in 1828; prior to their construction the only access to the islands was by boat."},
            {'Name':'Inverness Botanic Gardens', 'N':57.46332412985391, 'E':-4.240404903869764, 'Description': "A botanic garden with a tropical house with a carp pond and waterfalls, formal gardens and a cafe."},
        ],
        'Edinburgh': [
            {'Name':'Edinburgh Castle', 'N':55.948750874426054, 'E':-3.199881315583384, 'Description': "Edinburgh Castle is a historic fortress which dominates the skyline of Edinburgh, the capital city of Scotland, from its position on the Castle Rock. Archaeologists have established human occupation of the rock since at least the Iron Age, although the nature of the early settlement is unclear."},
            {'Name':'Dean Village', 'N':55.95347447404977, 'E':-3.216849572668915, 'Description': "Bucolic village abutting a tranquil stream, with gardens, 19th-century buildings & a museum."},
            {'Name':'The Scott Monument', 'N':55.95363610639374, 'E':-3.192671042038105, 'Description': "The Scott Monument is a Victorian Gothic monument to Scottish author Sir Walter Scott. It is the second largest monument to a writer in the world after the José Martí monument in Havana."},
            {'Name':'Palace of Holyroodhouse', 'N':55.953547902497924, 'E':-3.1726434197682067, 'Description': "The Palace of Holyroodhouse, commonly referred to as Holyrood Palace or Holyroodhouse, is the official residence of the British monarch in Scotland, Queen Elizabeth II."},
            {'Name':'The University of Edinburgh', 'N':55.94455182918802, 'E':-3.189176929076799, 'Description': "The University of Edinburgh, founded in 1582, is the sixth oldest university in the United Kingdom and English-speaking world and one of Scotland's ancient universities."},
            {'Name':'Calton Hill', 'N':55.955749997331665, 'E':-3.183041519818556, 'Description': "Calton Hill is a mix of bustling commercial areas and quiet residential streets. The hill itself, with its city views, is home to the Collective contemporary art gallery and the unfinished National Monument."}
        ],
    }
    
    users = ['George Smith', 'Alice Brown', 'Peter Wilson', 'Lena Thomson', 'John Robertson', 'Julie Campbell', 'Frank Stewart', 'Christina Anderson', 'David Macdonald', 'Ashley Scott', 'Richard Reid', 'Emily Murray']
    
    reviews = [
        {'Title':'Not worth the visit!', 'Comment': 'This place is incredibly overrated. Not nearly as picturesque, crowds everywhere, and weird smells all around.'},
        {'Title':'Nothing interesting to see there', 'Comment': 'I have to say that I\'ve imagined it to be much more interesting.'},
        {'Title':'Quite average', 'Comment': 'Just as I pictured it. The local amenities could however be a bit more up to scratch.'},
        {'Title':'Very nice', 'Comment': 'Quite beautiful. Would definitely recommend visiting.'},
        {'Title':'Loved it!', 'Comment': 'Absolutely breathtaking. Photos don\'t do this place justice. An experience of a lifetime.'}
    ]
    
    for city in cities:
        c = add_city(city['Name'], city['Description'])
        for a in attractions[city['Name']]:
            add_attraction(a['Name'], a['N'], a['E'], a['Description'], c)  
        
    for user in users: 
        current_user = add_user(user)
        for city in City.objects.all():
            add_rating(city, current_user)
        for attraction in Attraction.objects.all():
            add_save_review(attraction, current_user, reviews)           
        for review in AttractionReviews.objects.all():
            if (random.random() > 0.75):
                add_like(review, current_user)

  
# Thx to https://www.kite.com/python/answers/how-to-generate-a-random-date-between-two-dates-in-python for making my life a bit easier        
def random_date(start, end):
    start_date = date.fromisoformat(start)
    time_between_dates = date.fromisoformat(end) - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days) 
    return random_date  
    
def add_city(name, description):
    c = City.objects.get_or_create(Name=name, Description=description)[0]
    c.Views = random.randint(500,3000)
    c.HeaderPicture = "city_pictures/" + slugify(name) + ".jpg"
    c.save()
    return c
    
def add_attraction(name, n, e, description, city):
    a = Attraction.objects.get_or_create(City=city, Name=name, CoordinateNorth = n, CoordinateEast = e, Description = description)[0]
    a.Views = random.randint(100,1000)
    a.HeaderPicture = "attraction_pictures/" + slugify(name) + ".jpg"
    a.save()
    return a
    
def add_user(user):
    username = slugify(user)
    
    django_user = User.objects.get_or_create(username=username, email='%s@%s' % (username, 'mustvisit.com'))[0]
    django_user.set_password('11235813')
    django_user.save()
    
    mvuser = MVUser.objects.get_or_create(DjangoUser=django_user)[0]
    mvuser.Name = user.split(' ')[0]
    mvuser.Surname = user.split(' ')[1]
    mvuser.DateOfBirth = random_date('1950-01-01', '2003-01-01')
    if bool(random.getrandbits(1)):
        mvuser.Avatar = "profile_pictures/" + username + ".jpg"
    mvuser.save()
    
    return mvuser
    
def add_rating(city, user):
    rating = CityRatings.objects.get_or_create(CityRated=city, UserRating=user, Rating=random.randint(1,5))[0] 
    rating.save()
    
def add_save_review(attraction, user, reviews):
    how_good = random.randint(0,4)
    
    review = AttractionReviews.objects.get_or_create(
      AttractionReviewed=attraction, 
      UserReviewing=user,
      Title = reviews[how_good]['Title'],
      Comment = reviews[how_good]['Comment'],
      Rating = how_good+1
    )[0]
    
    review.DateVisited = random_date('2000-01-01', '2019-03-01')
    review.TimeTaken = timedelta(hours=random.randint(0,5), minutes=random.randint(0,3)*15)
    review.save()
    
    if (how_good >= 3):
        user.SavedAttractions.add(attraction)
        user.save() 
            
def add_like(review, user):
    like = ReviewLikes.objects.get_or_create(ReviewLiked=review, UserLiking=user, Like=bool(random.getrandbits(1)))[0]
    like.save()   
    
if __name__ == '__main__':
    print('Starting the MustVisit population script...')
    populate()