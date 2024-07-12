import asyncio
from aiogram import Bot, Dispatcher
from log import my_logo 
from app import read_tokens

bot = Bot(token = read_tokens.TOKEN[0])
dp = Dispatcher()

async def main():
    my_logo.logo()
    await dp.start_polling(bot)

if __name__  == '__main__':
    asyncio.run(main())
    