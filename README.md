# Mock Weather app
Django project interacting with third party weather application(s) and displays current temperature

### Setup
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

### Endpoints

Local server URL: 127.0.0.1:8000/

1. / (Index) - contains the form to input latitude, longitude and weather Sources
2. /currentTemp - redirects to display the current temperature

### Input

1. Enter only float values for Latitude and Longitude, else page redirects to the index page
2. Select at least one source, else page redirects to the index page

### Output

Displays the current average temperature from one or all the sources selected
