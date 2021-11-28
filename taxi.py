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

def rep_course_is_exist(course):
	avbl = "available"
	notavbl = "not available"
	cursor = sqlite_connection.cursor()

	sql_select_query = """SELECT * FROM repetitors WHERE course = ?"""
	cursor.execute(sql_select_query, (course,))
	records = cursor.fetchone()
	if records is None:
		return notavbl
	if records is not None:
		return avbl 

def update_theme_and_price(chat_id, unique_id, course_order, schoolclass, theme, rankrep, price):
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

		sql_select_query = """SELECT * FROM repetitors WHERE course = ? AND schoolclass >= ? AND rank = ?"""
		cursor.execute(sql_select_query, (course_order, schoolclass, rankrep,))
		records = cursor.fetchall()

		if (records == []):
			bot.send_message(chat_id, 'Извините, но репетиторов выбранного вами класса ещё нет, поэтому мы предоставим вам репетитора классом чуть ниже.')

		while(records == []):
			if(rankrep == "Элит"):
				rankrep = "Бизнес"
				sql_select_query = """SELECT * FROM repetitors WHERE course = ? AND schoolclass >= ? AND rank = ?"""
				cursor.execute(sql_select_query, (course_order, schoolclass, rankrep,))
				records = cursor.fetchall()

			elif(rankrep == "Бизнес"):
				rankrep = "Комфорт"
				sql_select_query = """SELECT * FROM repetitors WHERE course = ? AND schoolclass >= ? AND rank = ?"""
				cursor.execute(sql_select_query, (course_order, schoolclass, rankrep,))
				records = cursor.fetchall()

			elif(rankrep == "Комфорт"):
				rankrep = "Эконом"
				sql_select_query = """SELECT * FROM repetitors WHERE course = ? AND schoolclass >= ? AND rank = ?"""
				cursor.execute(sql_select_query, (course_order, schoolclass, rankrep,))
				records = cursor.fetchall()

		if (records != []):
			insert_data = """UPDATE orders 
							SET rankrep = ?
							WHERE id = ?"""
			data_tuple = (rankrep, unique_id)
			cursor.execute(insert_data, data_tuple)

		sqlite_connection.commit()
		cursor.close()
	except sqlite3.OperationalError:
		pass
	return rankrep


