import telebot
import sqlite3
import taxi
from telebot import types
import settings
import change

def student_menu():
	keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
	key_profile = types.InlineKeyboardButton(text='Мой профиль', callback_data='profile'); #кнопка «Да»
	keyboard.add(key_profile); #добавляем кнопку в клавиатуру
	key_taxi= types.InlineKeyboardButton(text='Заказать репетитора', callback_data='taxi');
	keyboard.add(key_taxi);
	key_pay= types.InlineKeyboardButton(text='Оплатить заказ', callback_data='pay');
	keyboard.add(key_pay);
	return keyboard


def repetitors_menu():
	keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
	key_profile = types.InlineKeyboardButton(text='Мой профиль', callback_data='profile'); #кнопка «Да»
	keyboard.add(key_profile); #добавляем кнопку в клавиатуру
	key_taxirep= types.InlineKeyboardButton(text='Список заказов', callback_data='taxirep');
	keyboard.add(key_taxirep);
	key_taxi= types.InlineKeyboardButton(text='Заказать репетитора', callback_data='taxi');
	keyboard.add(key_taxi);
	key_pay= types.InlineKeyboardButton(text='Оплатить заказ', callback_data='pay');
	keyboard.add(key_pay);
	return keyboard