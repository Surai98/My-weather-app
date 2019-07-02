import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5e1f0b496928cd54520a2cb6e8f2b92e'
    error_message = ''
    message = ''
    message_class = ''
    if request.method == 'POST':

        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    error_message = ' This City does not exist in the world!'
            else:
                error_message = ' This City already exists in the database, please add another city.'

        if error_message:
            message = error_message
            message_class = "is-danger"
        else:
            message = "Your city was added successfully!"
            message_class = "is-success"

    form = CityForm()
    cities = City.objects.all()

    weather_data = []
    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],

        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form,
               'message': message,
               'message_class': message_class

               }

    return render(request, './weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')
