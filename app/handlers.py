import asyncio
from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message

#import models
import app.keyboards as kb 
# import main

router = Router()

HELP_COMMANDS = """
<b>/start</b> - <em>старт бот</em> 
<b>/help</b> - <em>набор команд в бот </em>
<b>/weather</b> - <em>покажит прогноз погоды в данный момент времени</em>
<b>/days</b> - <em>установить ежедневное уведомления на день</em>
<b>/weeks</b> - <em>установить eженедельные уведомления на неделю</em>
<b>/stop</b> - <em>остановить все уведомления</em>
<b>/stop-day</b> - <em>остановить уведомления на день</em>
<b>/stop-weeks</b> - <em>остановить вуведомления на неделю</em>
"""

# command START !
@router.message(CommandStart())
async def  cmd_start(message:Message):
    await message.answer(f"Hello! my friend {message.from_user.first_name.capitalize()}")
    # await message.answer(striker="AAMCAgADGQEAASyM5WaSal3GjNHELOrqFS6v-qulUdSLAAIBAQACVp29CiK-nw64wuY0AQAHbQADNQQ")  
    await message.answer(text=HELP_COMMANDS, parse_mode='HTML')  
    # await main.sticker("AAMCAgADGQEAASyM5WaSal3GjNHELOrqFS6v-qulUdSLAAIBAQACVp29CiK-nw64wuY0AQAHbQADNQQ")
    # await bot.send_stiker(message.from_user.id, striker="")
                        # reply_markup=kb.main) #example keyboards in bottom 
                        # reply_markup=kb.settings) #example keyboards in message 
    
# work with PHOTO
@router.message(F.photo)
async def get_photo(message:Message):
    #  тут получаю id photo  await message.answer(f"ID photo {message.photo[-1].file_id}")
    await message.answer_photo(photo = message.photo[-1].file_id , caption="I do not with photos")

# command F 
@router.message(F.text == 'как дела?')
async def how_are_you(message:Message):
    await message.answer('ok!')

# command HELP !
@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer("this command /help")


@router.message(Command('weather'))
async def get_help(message:Message):
    await message.answer("this command /weather")
