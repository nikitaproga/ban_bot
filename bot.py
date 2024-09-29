
import asyncio
import config

from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(config.token)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
    await bot.reply_to(message, text)


@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if "https://" in message.text:
        chat_id = message.chat.id 
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            await bot.reply_to(f"Мы забанили пользователя {user_id}")                
asyncio.run(bot.polling())
