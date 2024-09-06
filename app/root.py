from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message

#import models
import app.components.keyboards as kb 
from app.components.command import commands
from app.components.working_db import DataBase

#import roots
from app.components.root_weather import router_weather

router = Router()
router.include_router(router_weather)
db = DataBase()


# command START !
@router.message(CommandStart())
async def start(message:Message):
    lan = message.from_user.language_code
    await message.answer(f"{commands[lan]['START_COMMANDS'][0]} {message.from_user.first_name.capitalize()}")
    await message.answer(text=commands[lan]['START_COMMANDS'][1], parse_mode='HTML')
    # Тут инициализация пользователя !     
    await db.add_user_database(message.from_user.id, message.from_user.username, lan)
    
    
# work with PHOTO
@router.message(F.photo)
async def get_photo(message:Message):
    await message.answer_photo(photo = message.photo[-1].file_id , caption="I do not with photos")


# command HELP !
@router.message(Command('help'))
async def get_help(message:Message):
    print(message.from_user)
    lan = message.from_user.language_code
    await message.answer(f"{commands[lan]['HELP_COMMANDS'][0]}")
    await message.answer(text=commands[lan]['HELP_COMMANDS'][1], parse_mode='HTML')


# command  change language
@router.message(Command('language'))
async def get_language(message:Message):
    lan = message.from_user.language_code
    tx = message.text.split(' ')
    if len(tx)>1 and tx[1] in ['ru', 'en']:
        await db.write_database(message.from_user.id, tx[1],'language')
        await message.answer(f"{commands[lan]['LANGUAGE'][1]} {tx[1]}")
    else:
        await message.answer(f"{commands[lan]['LANGUAGE'][0]}")
        