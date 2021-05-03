# Demo for App

https://taxi-wala.herokuapp.com/

# Request a Ride:

![](rq-cpg.gif)

# Accept a ride

![](ac-cpg.gif)

# Start the App

Clone the Repo:

`git clone https://github.com/Guddu327/taxi_wala.git`

Activate virtual environment and install requirements:

`pip install -r requirements.txt`

Start the project by:

`python manage.py runserver`

Create status for the cabs:

`python manage.py add_status`

Add random users (rider or partner) to the database (create some dummy partners before the requesting for a ride):

```
$ python manage.py populate_users -h
usage: manage.py populate_users [-h] [--rider] [--exec] [--version]
                                [-v {0,1,2,3}] [--settings SETTINGS]
                                [--pythonpath PYTHONPATH] [--traceback]
                                [--no-color] [--force-color] [--skip-checks]
                                Limit

positional arguments:
  Limit                 Number of users... By default the users are riders..

optional arguments:
  -h, --help            show this help message and exit
  --rider               Populate Riders
  --exec                Populate executives
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
  --skip-checks         Skip system checks.

```



