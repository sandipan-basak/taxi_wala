import random
import json
from faker import Faker
from django.core.management.base import BaseCommand
from rides.models import Executive, Cab, User
from rides.utils.generator_util import GeneratorMod
from rides.utils.license_plate import License

class Command(BaseCommand):

    shift_options = (('M','08:00 - 17:00'),('E','16:00 - 01:00'),('N','00;00 - 09:00'))
    fakegen = Faker()
    lic = License() 
    gu = GeneratorMod()

    def populate_execs(self, n=2):

        for _ in range(n):

            shift = self.shift_options[random.randint(0, 2)]
            name = self.fakegen.name()
            pas_ = self.gu.get_random_string(10)
            uname = self.gu.generate_username(name)
            car_number = self.lic.generate_license_plate()
            cab = Cab.objects.create(number=car_number)

            user = User.objects.create(username=uname, name=name, password=pas_, is_ex=True, is_rider=False)

            Executive.objects.create(user=user, car=cab, shift=shift)

    def populate_rider(self, n=2):
        file = open('user_pass.json', 'a+')
        
        data = json.load(file)
        for _ in range(n):
            
            name = self.fakegen.name()
            pas_ = self.gu.get_random_string(10)
            uname = self.gu.generate_username(name)
            
            user = User.objects.create(username=uname, name=name, password=pas_, is_ex=False, is_rider=True)
            
            data.append({
                "name": name,
                "username": uname,
                "pass": pas_
            })

            Rider.objects.create(user=user)

        json.dump(data, file)
        file.close()

    def add_arguments(self, parser):
        parser.add_argument('limit', metavar='Limit', type=int, 
                    help='Number of users... By default the users are executives..')
        parser.add_argument(
                '--rider',
                action='store_true',
                help='Populate rider',
            )
        parser.add_argument(
                '--exec',
                action='store_true',
                help='Populate executives',
            )
    
    def handle(self, *args, **options):

        with open('user_pass.json','a+') as file:
            
        print(file.read())
        if options['rider']:
            print(int(options['limit']))
            self.populate_rider(options['limit'])
        else:
            self.populate_execs(options['limit'])