import asyncio
from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message

#import keybord
import app.keyboards as kb 

router = Router()

HELP_COMMANDS = """
<b>/help</b> - <em>help me bot</em>
<b>/weather</b> - <em>weather</em>
<b>/start</b> - <em>start bot</em> 
"""

INSTRUCTION_COMMANDS = """
ТУТ БУДУТ ИНСТРУКЦИИ 
"""

# command START !
@router.message(CommandStart())
async def  cmd_start(message:Message):
    await message.answer(f"Hello! my friend {message.from_user.first_name.capitalize()}")
    # await message.answer(striker="AAMCAgADGQEAASyM5WaSal3GjNHELOrqFS6v-qulUdSLAAIBAQACVp29CiK-nw64wuY0AQAHbQADNQQ")  
    await message.answer(text=HELP_COMMANDS, parse_mode='HTML')  
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
