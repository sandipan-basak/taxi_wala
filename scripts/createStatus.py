from rides.models import Status

def create_objects(name, color):
    Status.objects.create(name, color)

def run():
    Status.objects.all().delete()
    s1 = create_objects('On Queue', '#007bff')
    s2 = create_objects('Ongoing', '#28a745')
    s3 = create_objects('Completed', '#28a745')
    s4 = create_objects('Cancelled', '#00000')
    print(Status.objects.all())
