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
