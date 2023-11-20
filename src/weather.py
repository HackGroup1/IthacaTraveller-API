import os, json, requests
from dotenv import load_dotenv

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
    Takes in longtitude and latitude, returns json with temperature info at given location
    """
    request = requests.get(url+'/astronomy.json?key='+API_KEY+'&q='+str(long)+','+str(lati))
    body = request.json()
    astro = body.get("astronomy").get("astro")
    return astro



#for debug purpose:
if __name__ == '__main__':
    print(get_weather_at(42.443962,-76.501884))
    print(get_astro_at(42.443962,-76.501884))