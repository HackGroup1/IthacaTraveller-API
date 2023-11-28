import os, json, requests
from dotenv import load_dotenv
from flask import request

load_dotenv()
url = 'http://api.weatherapi.com/v1'
API_KEY = os.environ.get("API_KEY")


def get_weather_at(long, lati):
    """
    Takes in longtitude and latitude, returns json with temperature info at given location
    """
    request = requests.get(url+'/current.json?key='+API_KEY+'&q='+str(long)+','+str(lati))
    body = request.json()
    current = body.get("current")
    return current

def get_astro_at(long, lati):
    """
    Takes in longtitude and latitude, returns json with astro info at given location
    """
    request = requests.get(url+'/astronomy.json?key='+API_KEY+'&q='+str(long)+','+str(lati))
    body = request.json()
    astro = body.get("astronomy").get("astro")
    return astro

def get_formatted_weather(long, lati):
    """
    Takes in longtitude and latitude, returns json with formatted info at given location
    Format: 
    {
        sunrise: <time>
        sunset: <time>
        weather: <0 for sunny, 1 for cloudy, 2 for rainning>
        temperature: <value in string>
    }
    """
    formatted_weather = {}
    weather = get_weather_at(long, lati)
    astro = get_astro_at(long, lati)

    if weather is None or astro is None:
        return None

    temperature = str(weather.get("temp_f"))
    condition = weather.get("condition").get("text").lower()
        
    sunrise = astro.get('sunrise')
    sunset = astro.get('sunset')

    formatted_weather["sunrise"] = sunrise
    formatted_weather["sunset"] = sunset
    formatted_weather["weather"] = condition
    formatted_weather["temperature"] = temperature

    return json.dumps(formatted_weather)

def weather_route(app):
    @app.route('/api/weather/')
    def formatted_weather():
        """
        Endpoint for returning formatted weather
        """
        
        long = request.args.get('longitude', default = None, type = int)
        lati = request.args.get('latitude', default = None, type = int)

        if long is None or lati is None:
            return {"error":"missing parameters"}, 400
        
        weather = get_formatted_weather(long, lati)
        
        if weather is None:
            return {"error":"incorrect parameters"}, 400
        
        return weather
    


#for debug purpose:
if __name__ == '__main__':
    print(get_weather_at(42.443962,-76.501884))
    print(get_astro_at(42.443962,-76.501884))
    print(get_formatted_weather(42.443962,-76.501884))
