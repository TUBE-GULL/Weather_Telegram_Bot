from aiogram import F,Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
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
        await message.answer(commands['ru']['WEATHER'][0])
        # await message.answer(commands[lan]['WEATHER'][1],reply_markup=kb.weather_coordinates_and_city_keyboard_ru)
        # if lan == 'ru':
        await message.answer(commands['ru']['WEATHER'][1],reply_markup=kb.weather_coordinates_and_city_keyboard_ru)
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
    lan = message.from_user.language_code # для локализации 
    await db.write_database(message.from_user.id, 'city', 'question') # запись вопроса для обрабочика вопросов!
    await message.answer("Пожалуйста, введите название города:", reply_markup=ReplyKeyboardRemove())

 
@router_weather.message(F.location)
async def handle_location(message: Message):
    user_id = message.from_user.id
    coordinates = f"{message.location.latitude, message.location.longitude}"
    
    # Запрос погоды по координатам
    result = await request_coordinates_API_OpenWeatherMap(coordinates)
    print(result)
    if result:
        # Сохранение координат в базе данных
        await db.write_database(user_id, coordinates, 'coordinates')
        await message.answer(f"Город по координатам: {coordinates}\nОписание: {result['description']}\nТемпература: {result['temp']}°C")
    else:
        await message.answer("Не удалось получить данные о погоде по указанным координатам.")
        await message.answer("Пожалуйста, отправьте свою локацию снова.")
        

# функции для рассылки по времени 
@router_weather.message(Command('newsletter'))
async def newsletter(message:Message):

     # print(message)
    local_time = datetime.now()
    print("Локальное время сервера:", local_time)
    print(message.date)
    result = await db.read_database(message.from_user.id,'time_zone')

    # тут дальнейший вопрос 
    if result:
        await message.answer(f"Ваше время уже установлено: {result}")
    else:
        await message.answer("Мы не знаем ваш часовой пояс. Хотите указать текущее время?", reply_markup=kb.yes_no_keyboard_ru)

        
# Обработка ответа на опрос
@router_weather.message(lambda message: message.text in ['Да', 'Нет'])
async def handle_yes_no(message: Message):
    if message.text == 'Да':
        await message.answer("Пожалуйста, укажите текущее время в формате HH:MM (например, 14:30):", reply_markup=ReplyKeyboardRemove())
        await db.write_database(message.from_user.id, 'time' , 'question')# обновляем статус вопроса !
    else:
        await message.answer("Хорошо, если понадобится, вы сможете указать время позже.", reply_markup=ReplyKeyboardRemove())




@router_weather.message()
async def handle_weather_input(message:Message):
    question = await db.read_database(message.from_user.id,'question')# проверяет соответствия вопроса 
    print('hi')
   
    if question == 'city':
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
            await db.write_database(message.from_user.id, None , 'question')# сбрасываем значения     
        else:
            await message.answer("Не удалось найти указанный город. Пожалуйста, проверьте правильность написания.")
            await message.answer("Пожалуйста, введите название города:")
    
    elif question == 'time':
        user_time = message.text

        try:
            # Проверяем правильность формата времени (HH:MM)
            user_time_obj = datetime.strptime(user_time, '%H:%M').time()

            # Получаем время из сообщения и преобразуем его в объект datetime
            message_time_obj = datetime.fromisoformat(message.date.isoformat())
            message_time_obj = message_time_obj.time()

            # Создаем datetime объекты для сравнения
            today = datetime.today().date()
            user_datetime = datetime.combine(today, user_time_obj)
            message_datetime = datetime.combine(today, message_time_obj)

            # Вычисляем разницу
            time_difference = user_datetime - message_datetime

            # Получаем разницу в часах как целое число
            difference_in_hours = int(time_difference.total_seconds() // 3600)

            await db.write_database(message.from_user.id, difference_in_hours, 'time_zone')

            await message.answer(f"Ваше время ({user_time}) успешно сохранено.")
            await db.write_database(message.from_user.id, None , 'question') # сброс статуса 
        except ValueError:
            await message.answer("Неправильный формат времени. Пожалуйста, укажите время в формате HH:MM.")





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


async def set_schedule():
    #sort in days and weeks
    users = db.get_all_users_with_time()
    week_users = [user for user in users['alarm_week']]
    day_users = [user for user in users['alarm_day']]
    
        
    text = "Это ваше запланированное сообщение!"
    
    utc_now = datetime.now(timezone.utc)
    
    # рассылка в 8 утра 
    day_users['time_zone']  = time_ for time in users['time_zone']
    utc_now == day_users[]
    
    
    
    # Планируем отправку сообщения
    # await schedule_message(user_id, text, send_time_utc)
    # await message.answer("Сообщение запланировано!")



# Функция для проверки времени рассылки
async def check_users_newsletter():
    # Здесь извлекаем всех пользователей и их время рассылки из базы данных
    users = db.get_all_users_with_time()  # Предположим, что эта функция возвращает список пользователей с их временем
    
    current_time = datetime.utcnow().time()  # Получаем текущее время в UTC
    
    for user in users:
        user_id = user['user_id']
        user_time = user['newsletter_time']  # Время, сохраненное для пользователя в базе
        
        # Проверяем, совпадает ли текущее время с временем пользователя
        if current_time.hour == user_time.hour and current_time.minute == user_time.minute:
            # Отправляем рассылку
            await send_newsletter(user_id, "Ваше ежедневное уведомление!")