import requests
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils import executor


API_TOKEN = "5986284630:AAEiE94AobDfjD1URjJK1S4nu2D3t9LEFH0"
WEATHER_API_KEY = "4e481ce0f4dc1225357d2dcc6f1637ac"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEI23dkU9W4PP-qVYCcAhFeqb4JVC3SgwACdCMAAkKGCEjJCqwmgfyNxS8E")
    await message.answer(text="Привіт. Я бот, який показує погоду. Введіть місто, і я скажу вам погоду та інформацію про неї.", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("Started")

@dp.message_handler(state=["Started"])
async def get_weather(message: types.Message):

    code_to_smile = {
        "ясно": "Ясно \U00002600",
        "облачно с прояснениями": "Мінлива хмарність ⛅",
        "переменная облачность": "Мінлива хмарність ⛅",
        "небольшая облачность": "Мінлива хмарність ⛅",
        "пасмурно": "Хмарно ☁️",
        "небольшой дождь": "Злива \U00002614",
        "дождь": "Злива \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "плотный туман": "Туман \U0001F32B"
    }
    try:
        city = message.text
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
        response = requests.get(url)
        data = response.json()
        print(data)
        weather_discription = data["weather"][0]["description"]
        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = "🥶Подивись у вікно, не розумію що там🥶"
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        feels_like = data['main']['feels_like']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await message.reply(f'Температура у місті: {city} зараз: {temp}°C\n'
                            f'Опис: {wd}\n'
                            f'Відчувається: {feels_like}°C\n'
                            f'Вологість: {humidity}%\n'
                            f'Схід сонця: {sunrise}\n'
                            f'Захід сонця: {sunset}\n'
                            f'Швидкість вітра: {wind_speed} м/с\n'
                            f'Яке місто ще будемо дивитись?', parse_mode=ParseMode.HTML)


    except Exception as e:
        print(e)
        await message.reply('🥶Щось пішло не так. Спробуйте ще раз.🥶')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)