import json
from telebot import TeleBot
from telebot.types import Message, Location, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from accuweather_api import AccuWeatherAPI
from openweather_api import OpenWeatherAPI
from weather_info import WeatherInfo
from weatherapi_api import WeatherAPI
from rating import Ratings

with open("tokens.json", "r") as read_file:
    tokens = json.load(read_file)
    TOKEN = tokens["Telegram"]
    ACCUWEATHER_TOKEN = tokens["AccuWeather"]
    WEATHERAPI_TOKEN = tokens["WeatherAPI"]
    OPENWEATHER_TOKEN = tokens["OpenWeather"]

accuweather_api = AccuWeatherAPI(ACCUWEATHER_TOKEN)
weatherapi_api = WeatherAPI(WEATHERAPI_TOKEN)
openweather_api = OpenWeatherAPI(OPENWEATHER_TOKEN)
bot = TeleBot(TOKEN, skip_pending=True)
feedback = None

actions = [
    "Текущая погода",
    "Прогноз на 3 часа",
    "Прогноз на завтра"
]

ratings = Ratings()


def gen_markup(src):
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(InlineKeyboardButton("1", callback_data=f"{src}_cb_1"),
               InlineKeyboardButton("2", callback_data=f"{src}_cb_2"),
               InlineKeyboardButton("3", callback_data=f"{src}_cb_3"),
               InlineKeyboardButton("4", callback_data=f"{src}_cb_4"),
               InlineKeyboardButton("5", callback_data=f"{src}_cb_5"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    callback = call.data.split('_')
    provider = callback[0]
    ratings.deserialize()
    if "cb_1" in call.data:
        bot.answer_callback_query(call.id, "1")
        ratings.ratings[provider].append(1)
    elif "cb_2" in call.data:
        bot.answer_callback_query(call.id, "2")
        ratings.ratings[provider].append(2)
    elif "cb_3" in call.data:
        bot.answer_callback_query(call.id, "3")
        ratings.ratings[provider].append(3)
    elif "cb_4" in call.data:
        bot.answer_callback_query(call.id, "4")
        ratings.ratings[provider].append(4)
    elif "cb_5" in call.data:
        bot.answer_callback_query(call.id, "5")
        ratings.ratings[provider].append(5)
    ratings.serialize()
    print("Отправил оценку на сервер")
    bot.edit_message_text("Спасибо", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def handle_provider_reply(message: Message, latitude, longitude):
    action = message.text
    ratings.deserialize()
    provider = ratings.get_best()
    print(latitude)
    print(longitude)

    msg_text = "Выбран неизвестный провайдер! Пожалуйста повторите операцию."
    temp_msg = bot.send_message(message.chat.id, f"Запрашиваем информацию от {provider}...")
    if provider == "AccuWeather":
        location_key = accuweather_api.get_location_key(latitude, longitude)
        if action == actions[0]:
            weather_info: WeatherInfo = accuweather_api.get_current_weather(location_key)
            msg_text = f"{action}:\n\n{weather_info.weather_state} \nТемпература {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit} \nВлажность {weather_info.humidity} % \nДавление {weather_info.pressure:.0f} мм рт. ст. \nВетер {weather_info.wind:.1f} км/ч"
        elif action == actions[1]:
            forecast_info_list = accuweather_api.get_next_3_hours(location_key)
            msg_text = f"{action}:\n\n"
            for forecast_info in forecast_info_list:
                weather_info: WeatherInfo = forecast_info.weather_info
                date = forecast_info.date_time
                msg_text += f"<b>{date}</b> - {weather_info.weather_state}, {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit}\n\n"
        elif action == actions[2]:
            weather_info: WeatherInfo = weatherapi_api.get_tomorrow_forecast(latitude, longitude)
            msg_text = f"{action}:\n\n{weather_info.weather_state} \nТемпература {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit}"

    elif provider == "WeatherAPI":
        if action == actions[0]:
            weather_info: WeatherInfo = weatherapi_api.get_current_weather(latitude, longitude)
            msg_text = f"{action}:\n\n{weather_info.weather_state} \nТемпература {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit} \nВлажность {weather_info.humidity} % \nДавление {weather_info.pressure:.0f} мм рт. ст. \nВетер {weather_info.wind:.1f} км/ч"
        elif action == actions[1]:
            forecast_info_list = openweather_api.get_next_3_hours(latitude, longitude)
            msg_text = f"{action}:\n\n"
            for forecast_info in forecast_info_list:
                weather_info: WeatherInfo = forecast_info.weather_info
                date = forecast_info.date_time
                msg_text += f"<b>{date}</b> - {weather_info.weather_state}, {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit}\n\n"
        elif action == actions[2]:
            weather_info: WeatherInfo = weatherapi_api.get_tomorrow_forecast(latitude, longitude)
            msg_text = f"{action}:\n\n{weather_info.weather_state} \nТемпература {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit}"

    elif provider == "OpenWeather":
        if action == actions[0]:
            weather_info: WeatherInfo = openweather_api.get_current_weather(latitude, longitude)
            msg_text = f"{action}:\n\n{weather_info.weather_state} \nТемпература {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit} \nВлажность {weather_info.humidity} % \nДавление {weather_info.pressure:.0f} мм рт. ст. \nВетер {weather_info.wind:.1f} км/ч"
        elif action == actions[1]:
            forecast_info_list = openweather_api.get_next_3_hours(latitude, longitude)
            msg_text = f"{action}:\n\n"
            for forecast_info in forecast_info_list:
                weather_info: WeatherInfo = forecast_info.weather_info
                date = forecast_info.date_time
                msg_text += f"<b>{date}</b> - {weather_info.weather_state}, {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit}\n\n"
        elif action == actions[2]:
            weather_info: WeatherInfo = openweather_api.get_tomorrow_forecast(latitude, longitude)
            msg_text = f"{action}:\n\n{weather_info.weather_state} \nТемпература {weather_info.temperature_value:+.0f}°{weather_info.temperature_unit}"
    print("Вывел прогноз")
    bot.delete_message(message.chat.id, temp_msg.message_id)
    bot.send_message(message.chat.id, msg_text, parse_mode="HTML")
    bot.send_message(message.chat.id, "Оцените прогноз", reply_markup=gen_markup(provider))


@bot.message_handler(content_types=["location"])
def handle_location(message: Message):
    location: Location = message.location
    latitude = location.latitude
    longitude = location.longitude
    print("Передал локацию: " + str(location.latitude) + ",   " + str(location.longitude))
    keyboard_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard_markup.add(KeyboardButton("Текущая погода"))
    keyboard_markup.add(KeyboardButton("Прогноз на 3 часа"))
    keyboard_markup.add(KeyboardButton("Прогноз на завтра"))
    bot_message = bot.send_message(message.chat.id, "Выберите одно из действий на клавиатуре:", reply_markup=keyboard_markup)
    print("Вывел клавиатуру")
    bot.register_next_step_handler(bot_message, lambda x: handle_provider_reply(x, latitude, longitude))


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Отправь мне геопозицию чтобы узнать погоду")


if __name__ == "__main__":
    bot.polling(none_stop=True)
