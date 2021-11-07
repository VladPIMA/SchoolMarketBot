import telebot
from telebot import types
import settings
import change
import sqlite3

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

try:
	sqlite_connection = sqlite3.connect('schoolmarket.db', check_same_thread = False)
except sqlite3.OperationalError:
	pass

def update_theme_and_price(unique_id, theme, rankrep, price):
	# запись в бд
	try:
		cursor = sqlite_connection.cursor()
		insert_data = """UPDATE orders 
						SET theme = ?
						WHERE id = ?"""
		data_tuple = (theme, unique_id)
		cursor.execute(insert_data, data_tuple)

		insert_data = """UPDATE orders 
						SET price = ?
						WHERE id = ?"""
		data_tuple = (price, unique_id)
		cursor.execute(insert_data, data_tuple)

		insert_data = """UPDATE orders 
						SET rankrep = ?
						WHERE id = ?"""
		data_tuple = (rankrep, unique_id)
		cursor.execute(insert_data, data_tuple)

		sqlite_connection.commit()
		cursor.close()
	except sqlite3.OperationalError:
		pass

