from generic_api import APIInterface
from weather_info import WeatherInfo
import datetime

class WeatherAPI(APIInterface):
    base_url: str = "http://api.weatherapi.com/v1"
    now = datetime.datetime.now()

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_weather(self, latitude, longitude) -> WeatherInfo:
        weather_data: dict = self.get_request(f"{self.base_url}/current.json", {
            "key": self.api_key,
            "q": f"{latitude},{longitude}",
            "lang": "ru"
        })
        weather_info: WeatherInfo = WeatherInfo(
            weather_state=weather_data.get("current").get("condition").get("text"),
            temperature_value=weather_data.get("current").get("temp_c"),
            temperature_unit="C",
            humidity=weather_data.get("current").get("humidity"),
            pressure=weather_data.get("current").get("pressure_mb") * 0.75,
            wind=weather_data.get("current").get("wind_kph")
        )
        return weather_info

    def get_next_3_hours(self, latitude, longitude) -> WeatherInfo:
        weather_data: dict = self.get_request(f"{self.base_url}/forecast.json", {
            "key": self.api_key,
            "q": f"{latitude},{longitude}",
            "lang": "ru",
            "days": 1,
            "hours": f"{self.now.hour+1}"
        })
        weather_info: WeatherInfo = WeatherInfo(
            weather_state=weather_data.get("current").get("condition").get("text"),
            temperature_value=weather_data.get("current").get("temp_c"),
            temperature_unit="C"
        )
        return weather_info

    def get_tomorrow_forecast(self, latitude, longitude) -> WeatherInfo:
        forecast_data: dict = self.get_request(f"{self.base_url}/forecast.json", {
            "key": self.api_key,
            "q": f"{latitude},{longitude}",
            "lang": "ru",
            "days": 2
        })
        weather_data: dict = forecast_data.get("forecast").get("forecastday")[1]

        weather_info = WeatherInfo(
            weather_state=weather_data.get("day").get("condition").get("text"),
            temperature_value=weather_data.get("day").get("avgtemp_c"),
            temperature_unit="C"
        )
        return weather_info
