import random
import string

class GeneratorMod:
    def generate_digits(self, amount):
        digits = ""
        for _ in range(amount):
            digits = digits + chr(random.randint(ord('0'), ord('0')+9))
        return digits

    def generate_username(self, name):
        user = "_".join(name.split() + [self.generate_digits(7)])
        return user

    def get_random_string(self, length):
        result = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return result