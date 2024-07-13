from app.read_tokens import TOKEN_WEATHER
    
def conclusion_function(weather):
    weather_info = (
        f"ваш город : {weather['city']}\n"
        f"температура: {weather['temp']}℃\n"
        f"температуру по ощущениям: {weather['feels_like']}℃\n"
        f"облочность: {weather['description']}\n"
        f"скорость ветра: {weather['wind speed']} м.с\n"
        f"относительную влажность воздуха: {weather['humidity']}%\n"
        f"давление: {weather['pressure']} миллиметрах ртутного столба")  
    return weather_info
 
 
def request_API_OpenWeatherMap (city, language = 'en'):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={TOKEN_WEATHER}"
    weather = requests.get(url).json()    
    return {
        'lon':weather.get('coord')['lon'],
        'lat':weather.get('coord')['lat'],
        'city' :city,
        'temp': weather.get('main')['temp'],
        'feels_like': weather.get('main')['feels_like'],
        'description': weather.get('weather')[0]['description'],
        "wind speed": weather.get('wind')['speed'],
        'humidity': weather.get('main')['humidity'],
        'pressure': weather.get('main')['pressure'],
        }
 
 
def get_air_quality_index(city):
    result = request_API_OpenWeatherMap(city)
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={result['lat']}&lon={result['lon']}&appid={TOKEN_WEATHER}"
    return  requests.get(url).json()
    # 
    # 
def get_next_day_weather(city):
    #получаю текущие время 
    current_date = int(datetime.datetime.today().strftime('%d'))

    result = request_API_OpenWeatherMap(city)
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={result['lat']}&lon={result['lon']}&appid={TOKEN_WEATHER}"
    response = requests.get(url).json()
 
    array = []
    for weather in response['list']:
        if int(weather['dt_txt'][8:10]) == current_date + 1:
            array.append(f"wehter for the {weather['dt_txt']}\n"
                        f"температура: {weather.get('main')['temp']}℃\n"
                        f"температуру по ощущениям: {weather.get('main')['feels_like']}℃\n"
                        f"облочность: {weather.get('weather')[0]['description']}\n"
                        f"скорость ветра: {weather.get('wind')['speed']} м.с\n"
                        f"относительную влажность воздуха: {weather.get('main')['humidity']}%\n"
                 f"давление: {weather.get('main')['pressure']} миллиметрах ртутного столба\n") 
    return array

