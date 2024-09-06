# create keyboard
from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           InlineKeyboardMarkup,InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='catalog')],
    [KeyboardButton(text='trash'),KeyboardButton(text='contact')]
],
                          resize_keyboard=True, # min size 
                          input_field_placeholder='choice item menu') # text in search

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='text', url='http://cryptobumsnft.com/')]
])

# weather_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="/time_weather"), KeyboardButton(text="/utc")]
#     ],
#     resize_keyboard=True
# )

weather_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="/time_weather", callback_data="/time_weather")],
    [InlineKeyboardButton(text="/weather_now", callback_data="/weather_now")]
])


# weather_coordinates_and_city_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
#     KeyboardButton('написать город  🏙')
# ).add(
#     KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
# )

weather_coordinates_and_city_keyboard_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Написать город  🏙'), KeyboardButton(text='Отправить свою локацию 🗺️', request_location=True)]
    ],
    resize_keyboard=True, # min size 
    one_time_keyboard=True, 
)

weather_coordinates_and_city_keyboard_en = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Write the city  🏙'), KeyboardButton(text='Send your location 🗺️', request_location=True)]
    ],
    resize_keyboard=True, # min size 
    one_time_keyboard=True, 
)