class WeatherInfo:
    def __init__(self, weather_state: str, temperature_value: float, temperature_unit: str, humidity: int = None, pressure: float = None, wind: float = None):
        self.temperature_unit = temperature_unit
        self.temperature_value = temperature_value
        self.weather_state = weather_state
        self.humidity = humidity
        self.pressure = pressure
        self.wind = wind
