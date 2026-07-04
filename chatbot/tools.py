import requests
from langchain.tools import tool

@tool
def get_weather_by_location(location_name: str) -> str:
    """
    Fetches the current weather data for a given city or country name using the free Open-Meteo API.
    Input should be a string representing the location (e.g., 'London', 'Paris', 'Tokyo').
    """
    # STEP 1: Use Open-Meteo's free Geocoding API to get Lat/Lon coordinates
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_name}&count=1&language=en&format=json"
    
    try:
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        # Check if the results key exists and has items
        if "results" not in geo_data or not geo_data["results"]:
            return f"Could not find coordinates for the location: '{location_name}'."
        
        location_info = geo_data["results"][0]
        lat = location_info['latitude']
        lon = location_info['longitude']
        resolved_name = location_info['name']
        country = location_info.get('country', 'Unknown Country')

        # STEP 2: Fetch weather using Open-Meteo's core Weather API
        # We request temperature, apparent temperature (feels like), and relative humidity
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature&temperature_unit=celsius"
        
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if "current" not in weather_data:
            return "Failed to parse weather data from the API."

        current_weather = weather_data["current"]
        temp = current_weather.get("temperature_2m")
        feels_like = current_weather.get("apparent_temperature")
        humidity = current_weather.get("relative_humidity_2m")

        return (
            f"Current weather data for {resolved_name}, {country}:\n"
            f"- Temperature: {temp}°C\n"
            f"- Feels Like: {feels_like}°C\n"
            f"- Humidity: {humidity}%"
        )

    except Exception as e:
        return f"An error occurred while fetching the weather: {str(e)}"
    

# res = get_weather_by_location.invoke({"location_name":"London"})

# print(res)