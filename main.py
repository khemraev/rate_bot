import telebot
import requests
from bs4 import BeautifulSoup as soup 
from telebot import types

SMN_RUB = 'https://rub.ru.currencyrate.today/tjs/1000'
SMN_DOLL = 'https://www.calc.ru/kurs-USD-TJS.html?text_quantity=100'
headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.4.143 Yowser/2.5 Safari/537.36' , 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

token = '1282440639:AAHrtMxmEEBAbylSkzhZglhVpSMhklQQmBU'

bot = telebot.TeleBot(token)

full_page_rub = requests.get(SMN_RUB , headers = headers)
full_page_doll = requests.get(SMN_DOLL , headers = headers)

html_rub = soup(full_page_rub.content , 'html.parser')
html_doll = soup(full_page_doll.content , 'html.parser')

doll = html_doll.findAll("b", {})[1].text
rub = html_rub.findAll("span", {"class": "cc-result"})[1].text


@bot.message_handler(commands=['start'])
def start(message):

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("/rubl")
	btn2 = types.KeyboardButton("/dollar")
	markup.add(btn1, btn2)

	bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}!\nВедите валюту, чтобы узнать курс на сегодня !", reply_markup=markup)



@bot.message_handler(commands=['rubl'])
def mess(message):
	bot.send_message(message.chat.id, f"Курс рубля на сегодня: \n"+ "1000р = " + rub)

@bot.message_handler(commands=['dollar'])
def mess2(message):
	bot.send_message(message.chat.id, f"Курс доллара на сегодня: \n"+ "100 доллар = " + doll)


if __name__ == '__main__':
	bot.polling(none_stop=True)