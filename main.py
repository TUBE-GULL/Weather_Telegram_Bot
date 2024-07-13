import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from log import my_logo 
from app.read_tokens import TOKEN
from app.handlers import router

bot = Bot(token = TOKEN[0])
dp = Dispatcher()

async def main():
    my_logo.logo()
    dp.include_router(router)
    await dp.start_polling(bot)

async def sticker(id):
    await bot.send_sticker(Message.from_user.id, sticker=id)

if __name__  == '__main__':
    asyncio.run(main())
    