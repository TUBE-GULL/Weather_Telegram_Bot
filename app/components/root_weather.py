from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message   
from datetime import datetime, timezone

import app.components.keyboards as kb
from app.components.fun_weather import request_API_OpenWeatherMap
from app.components.command import commands
from app.components.working_db import DataBase


router_weather = Router(name='weather')
db = DataBase()


@router_weather.message(Command('weather'))
async def weather(message:Message):
    lan = message.from_user.language_code
    await message.answer(f"{commands[lan]['WEATHER'][0]}")


@router_weather.message(Command('city'))
async def city(message:Message):
    city = message.text.split(' ')
    result = request_API_OpenWeatherMap(city)
    
    print(result)
    if result:
        await message.answer(f"Город: {result['city']}\nОписание: {result['description']}\nТемпература: {result['temp']}°C")
    else:
        await message.answer("Не удалось найти указанный город. Пожалуйста, проверьте правильность написания.")
        






