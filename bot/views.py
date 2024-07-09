import logging
import telebot
import string
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from datetime import datetime
from itertools import zip_longest
from .models import MainChannel
from .models import SubChannel
from .models import KeywordReplacement
from .models import KeywordReplacementItem
from .tasks import process_telegram_update
from .conf import bot

logger = logging.getLogger(__name__)

user_context = {}


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update_data = request.body.decode('utf-8')
            process_telegram_update.delay(update_data)
            logger.info(f"Отримане оновлення з webhook: {update_data}")
            return HttpResponse('')
        except Exception as e:
            logger.error(f"Помилка обробки вебхуку: {str(e)}")


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Hello Telegram!", reply_markup=create_reply_markup())


def create_reply_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton('Главные каналы'))
    markup.add(KeyboardButton('Дочерние каналы'))
    markup.add(KeyboardButton('Ключевые слова'))
    print("Кнопки меню markup")
    print(markup)
    return markup


@bot.message_handler(func=lambda message: message.text == 'Главные каналы')
def send_main_channels(message):
    chat_id = message.chat.id
    main_channels = MainChannel.objects.all()
    response = "Главные каналы:\n\n"
    for channel in main_channels:
        response += f"{channel.name}\n ID: {channel.channel_id}\n\n"
    bot.send_message(chat_id, response)


@bot.message_handler(func=lambda message: message.text == 'Дочерние каналы')
def send_sub_channels(message):
    chat_id = message.chat.id
    sub_channels = SubChannel.objects.all()
    response = "Дочерние каналы:\n\n"
    for channel in sub_channels:
        response += f"Дочерний канал: {channel.name}\n ID: {channel.channel_id}\n Главный канал: {channel.main_channel.name}\n\n"
    bot.send_message(chat_id, response)


@bot.message_handler(func=lambda message: message.text == 'Ключевые слова')
def send_keyword_replacements(message):
    chat_id = message.chat.id
    keyword_replacements = KeywordReplacementItem.objects.all()
    response = "Ключевые слова:\n\n"
    for item in keyword_replacements:
        response += f"Дочерний канал: {item.keyword_replacement.sub_channel.name}\n {item.keyword} -> {item.replacement}\n\n"
    bot.send_message(chat_id, response)


@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    chat_id = message.chat.id
    try:
        main_channel = MainChannel.objects.get(channel_id=str(chat_id))
        logger.info(f"Found main channel: {main_channel.name}")
    except MainChannel.DoesNotExist:
        logger.warning(f"Main channel with id {chat_id} not found.")
        return

    for sub_channel in main_channel.sub_channels.all():
        modified_text = message.text
        logger.info(f"Original text: {modified_text}")

        for keyword_replacement in sub_channel.keyword_replacements.all():
            for item in keyword_replacement.items.all():
                modified_text = modified_text.replace(item.keyword, item.replacement)
                logger.info(f"Replaced '{item.keyword}' with '{item.replacement}'")

        try:
            bot.send_message(sub_channel.channel_id, modified_text)
            logger.info(f"Sent modified text to sub channel {sub_channel.name}: {modified_text}")
        except Exception as e:
            logger.error(f"Failed to send message to sub_channel {sub_channel.channel_id}: {str(e)}")
