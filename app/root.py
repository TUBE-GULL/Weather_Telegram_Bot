import asyncio
from aiogram import F,Router,Dispatcher
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
# from aiogram import Bot, Dispatcher

#import models
import app.components.keyboards as kb 

#import roots
from app.components.weather import router_weather
from app.components.stop import stop
from app.components.stop_days import stop_days
from app.components.stop_weeks import stop_weeks

router = Router()
router.include_router(router_weather)
router.include_router(stop)
router.include_router(stop_days)
router.include_router(stop_weeks)


HELP_COMMANDS = """
<b>/start</b> - <em>старт бот</em> 
<b>/help</b> - <em>набор команд в бот </em>
<b>/weather</b> - <em>покажит прогноз погоды в данный момент времени</em>
<b>/days</b> - <em>установить ежедневное уведомления на день</em>
<b>/weeks</b> - <em>установить eженедельные уведомления на неделю</em>
<b>/stop</b> - <em>остановить все уведомления</em>
<b>/stop_days</b> - <em>остановить уведомления на день</em>
<b>/stop_weeks</b> - <em>остановить вуведомления на неделю</em>
"""

# command START !
@router.message(CommandStart())
async def start(message:Message):
    await message.answer(f"Hello! my friend {message.from_user.first_name.capitalize()}")
    await message.answer(text=HELP_COMMANDS, parse_mode='HTML')
    
# work with PHOTO
@router.message(F.photo)
async def get_photo(message:Message):
    #  тут получаю id photo  await message.answer(f"ID photo {message.photo[-1].file_id}")
    await message.answer_photo(photo = message.photo[-1].file_id , caption="I do not with photos")

# command HELP !
@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer("команда /help ")
    await message.answer(text=HELP_COMMANDS, parse_mode='HTML')
