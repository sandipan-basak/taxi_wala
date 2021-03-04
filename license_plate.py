import random

# INVALID_PLATE_LETTERS = ["FOR", "AXE", "JAM", "JAB", "ZIP", "ARE", "YOU",
        # "JUG", "JAW", "JOY"]

def generate_letters(amount):
    letters = ""
    for _ in range(amount):
        letters = letters + chr(random.randint(65, (65+25)))
    return letters

def generate_digits(amount):
    digits = ""
    for _ in range(amount):
        digits = digits + chr(random.randint(ord('0'), ord('0')+9))

    return digits

def generate_license_plate():
    l_1 = generate_letters(2)
    d_1 = generate_digits(2)
    l_2 = generate_letters(1)
    d_2 = generate_digits(4)
    license_plate = l_1 + '-' + d_1 + '-' + l_2 + '-' + d_2
    return license_plate

print(generate_license_plate())

print(generate_letters(3))
print(generate_digits(3))
