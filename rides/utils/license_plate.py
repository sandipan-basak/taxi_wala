import random

class License():

    def generate_letters(self, amount):
        letters = ""
        for _ in range(amount):
            letters = letters + chr(random.randint(65, (65+25)))
        return letters

    def generate_digits(self, amount):
        digits = ""
        for _ in range(amount):
            digits = digits + chr(random.randint(ord('0'), ord('0')+9))
        return digits

    def generate_license_plate(self):
        l_1 = self.generate_letters(2)
        d_1 = self.generate_digits(2)
        l_2 = self.generate_letters(1)
        d_2 = self.generate_digits(4)
        license_plate = l_1 + '-' + d_1 + '-' + l_2 + '-' + d_2
        return license_plate


