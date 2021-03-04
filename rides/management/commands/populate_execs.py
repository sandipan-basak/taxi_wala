from django.core.management.base import BaseCommand
from rides.models import Executive, Cab

import random
from faker import Faker

fakegen = Faker()
# topics = ['Search','Social','Marketplace','News','Games']

# def add_topic():
#     s = random.randint(0,3)
#     return s



def populate(N=2):
    '''
    Create N Entries of Dates Accessed
    '''

    for entry in range(N):

        # Get Topic for Entry

        shift = random.randint(0,3)
        # top = add_topic()

        # Create Fake Data for entry
        name = fakegen.name()
        address = fakegen.address()
        fake_name = fakegen.company()

        # Create new Webpage Entry
        webpg = Webpage.objects.get_or_create(topic=top,url=fake_url,name=fake_name)[0]

        # Create Fake Access Record for that page
        # Could add more of these if you wanted...
        accRec = AccessRecord.objects.get_or_create(name=webpg,date=fake_date)[0]


if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    populate(20)
    print('Populating Complete')
