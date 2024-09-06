from aiogram import F,Router
from aiogram.filters import Command
from aiogram.types import Message   
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger


import app.components.keyboards as kb
from app.components.fun_weather import request_city_API_OpenWeatherMap, request_coordinates_API_OpenWeatherMap
from app.components.command import commands
from app.components.working_db import DataBase


router_weather = Router(name='weather')
db = DataBase()


@router_weather.message(Command('weather'))
async def weather(message: Message):
    lan = message.from_user.language_code
    
    # Получаем данные из базы данных
    city = await db.read_database(message.from_user.id, 'city')
    coordinates = await db.read_database(message.from_user.id, 'coordinates')
    
    # Если нет ни города, ни координат, просим пользователя ввести данные
    if city is None and coordinates is None:
        await message.answer(commands[lan]['WEATHER'][0])
        await message.answer(commands[lan]['WEATHER'][1])
        # if lan == 'ru':
        await message.answer( 
            reply_markup=kb.weather_coordinates_and_city_keyboard_ru
        )
        # else:
        # await message.answer( 
        #     reply_markup=kb.weather_coordinates_and_city_keyboard_en
        # )
    else:
        # Проверяем город
        if city != None:
            result = await request_city_API_OpenWeatherMap(city, lan)  # Добавляем язык в запрос
            
            # Формируем ответ в зависимости от языка
            if lan == 'ru':
                await message.answer(f"Город: {city}\nОписание: {result['description']}\nТемпература: {result['temp']}°C")
            else:
                await message.answer(f"City: {city}\nDescription: {result['description']}\nTemperature: {result['temp']}°C")
        
        # Проверяем координаты
        elif coordinates != None:
            result = await request_coordinates_API_OpenWeatherMap(coordinates)
            print(result)
            
            # Формируем ответ в зависимости от языка
            if lan == 'ru':
                await message.answer(f"Город по координатам: {coordinates}\nОписание: {result['description']}\nТемпература: {result['temp']}°C")
            else:
                await message.answer(f"City by coordinates: {coordinates}\nDescription: {result['description']}\nTemperature: {result['temp']}°C")


# получения города !
@router_weather.message(lambda message: message.text == 'Написать город  🏙') # пока на английском 
async def ask_for_city(message:Message):
    lan = message.from_user.language_code
    await message.answer("Пожалуйста, введите название города:")


# Обработка текста, введенного пользователем
@router_weather.message(lambda message: message.text and message.text != 'Отправить свою локацию 🗺️')
async def handle_city_input(message:Message):
    city = message.text
    user_id = message.from_user.id
    
    print(city)
    print(user_id)
    
    # check city through API
    result = await request_city_API_OpenWeatherMap(city)
    print('result:',result)
    
    if result:
        await message.answer(f"Город: {result['city']}\nОписание: {result['description']}\nТемпература: {result['temp']}°C")
        await db.write_database(user_id, city ,'city')
    else:
        await message.answer("Не удалось найти указанный город. Пожалуйста, проверьте правильность написания.")
        await message.answer("Пожалуйста, введите название города:")
    
    
    
@router_weather.message(F.location)
async def handle_location(message: Message):
    user_id = message.from_user.id
    coordinates = f"{message.location.latitude, message.location.longitude}"
    
    
    # Сохранение координат в базе данных
    
    # Запрос погоды по координатам
    result = request_coordinates_API_OpenWeatherMap(coordinates)
    print(result)
    if result:
        await db.write_database(user_id, coordinates, 'coordinates')
        await message.answer(f"Город по координатам: {coordinates}\nОписание: {result['description']}\nТемпература: {result['temp']}°C")
    else:
        await message.answer("Не удалось получить данные о погоде по указанным координатам.")
        await message.answer("Пожалуйста, отправьте свою локацию снова.")
        
        
        
# функции для рассылки по времени 


# Функция для рассылки сообщения
async def send_message_to_user(user_id: int, text: str):
    try:
        await router_weather.send_message(user_id, text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        
        
# Фоновая задача для рассылки
async def schedule_message(user_id: int, text: str, send_time_utc: datetime):
    scheduler = AsyncIOScheduler()

    # Установка триггера для рассылки по времени (в UTC)
    trigger = DateTrigger(run_date=send_time_utc)

    # Добавляем задачу в планировщик
    scheduler.add_job(send_message_to_user, trigger, args=[user_id, text])

    scheduler.start()

# Пример команды для установки времени рассылки
@router_weather.message(commands=['set_schedule'])
async def set_schedule(message:Message):
    user_id = message.from_user.id
    text = "Это ваше запланированное сообщение!"
    
    # Пример установки времени (в UTC)
    send_time_utc = datetime.now(timezone.utc).replace(minute=message.text.split()[1], second=0, microsecond=0)  # Например, через 5 минут
    
    # Планируем отправку сообщения
    await schedule_message(user_id, text, send_time_utc)
    await message.answer("Сообщение запланировано!")