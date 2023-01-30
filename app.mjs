import { Telegraf } from 'telegraf';
import axios, { Axios } from 'axios';
import { writeFile, readFileSync, writeFileSync } from 'node:fs';
import dotenv from 'dotenv'
import { getWeather } from './getUrlData.mjs';

dotenv.config();




const bot = new Telegraf(process.env.TOKEN);

bot.start(ctx => ctx.reply(`hi`))

console.log(await getWeather('tyumen'))



bot.launch()
console.log('bot start !')

