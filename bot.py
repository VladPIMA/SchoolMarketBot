import os
import telebot
import sqlite3
import settings
import change
from telebot import types

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)

# создание и подключение к бд
try:
	sqlite_connection = sqlite3.connect('schoolmarket.db', check_same_thread = False)
	cursor = sqlite_connection.cursor()

	createCommand = """
	CREATE TABLE students (
		"id"	INTEGER NOT NULL,
		"name"	TEXT NOT NULL,
		"surname"	TEXT NOT NULL,
		"dateofbirth" TEXT NOT NULL,
		"schoolclass"	TEXT NOT NULL,
		"currency"	INTEGER
	);"""

	cursor.execute(createCommand)
	cursor.close()
except sqlite3.OperationalError:
	pass

try:
	cursor = sqlite_connection.cursor()
	createCommand = """
	CREATE TABLE repetitors (
		"id"	INTEGER NOT NULL,
		"name"	TEXT NOT NULL,
		"surname"	TEXT NOT NULL,
		"dateofbirth" TEXT NOT NULL,
		"schoolclass"	TEXT NOT NULL,
		"course" TEXT,
		"rating" INTEGER NOT NULL,
		"currency"	INTEGER
	);"""

	cursor.execute(createCommand)
	cursor.close()
except sqlite3.OperationalError:
	pass


@bot.message_handler(content_types=['text'])
def start(message):
	global status
	chat_id = message.from_user.id
	if message.text == '/reg':
		keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
		key_student = types.InlineKeyboardButton(text='Ученик', callback_data='student');
		keyboard.add(key_student); #добавляем кнопку в клавиатуру
		key_repetitor= types.InlineKeyboardButton(text='Репетитор', callback_data='repetitor');
		keyboard.add(key_repetitor);
		question = 'Давай определимся с твоей ролью, нажми на кнопку, кем бы ты хотел быть =)';
		bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
	else:
		bot.send_message(message.from_user.id, "Привет! Чтобы зарегистрироваться напиши /reg");

def get_name(message): #получаем фамилию
	global name;
	name = message.text;
	bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
	bot.register_next_step_handler(message, get_surname);

def get_surname(message):
	global surname;
	surname = message.text;
	bot.send_message(message.from_user.id, 'Твоя дата рождения (в формате DD.MM.YYYY):');
	bot.register_next_step_handler(message, get_dateofbirth);

def get_dateofbirth(message):
	global dateofbirth;
	dateofbirth = message.text;
	bot.send_message(message.from_user.id, 'В каком ты классе?');
	bot.register_next_step_handler(message, get_schoolClass);

def get_schoolClass(message):
	global schoolclass
	global currency
	schoolclass = 0
	schoolclass = message.text
	currency = 0

	keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
	key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
	keyboard.add(key_yes); #добавляем кнопку в клавиатуру
	key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
	keyboard.add(key_no);
	question = 'Ты в ' + str(schoolclass) + ' классе, тебя зовут ' + name + ' ' + surname + ' и ты родился(-ась) ' + dateofbirth + '?';
	bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

	# запись в бд
	try:
		cursor = sqlite_connection.cursor()
		insert_data = """INSERT INTO students(id, name, surname, dateofbirth, schoolclass, currency)
							VALUES (?, ?, ?, ?, ?, 0);"""
		data_tuple = (message.from_user.id, name, surname, dateofbirth, schoolclass)
		cursor.execute(insert_data, data_tuple)
		sqlite_connection.commit()
		cursor.close()
	except sqlite3.OperationalError:
		pass

def get_nameRep(message): #получаем фамилию
	global nameRep;
	nameRep = message.text;
	bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
	bot.register_next_step_handler(message, get_surnameRep);

def get_surnameRep(message):
	global surnameRep;
	surnameRep = message.text;
	bot.send_message(message.from_user.id, 'Твоя дата рождения (в формате DD.MM.YYYY):');
	bot.register_next_step_handler(message, get_dateofbirthRep);

def get_dateofbirthRep(message):
	global dateofbirthRep;
	dateofbirthRep = message.text;
	bot.send_message(message.from_user.id, 'В каком ты классе?');
	bot.register_next_step_handler(message, get_schoolClassRep);

def get_schoolClassRep(message):
	global schoolclassRep
	global currencyRep
	schoolclassRep = 0
	schoolclassRep = message.text
	currencyRep = 0

	# запись в бд
	try:
		cursor = sqlite_connection.cursor()
		insert_data = """INSERT INTO repetitors(id, name, surname, dateofbirth, schoolclass, rating, currency)
							VALUES (?, ?, ?, ?, ?, 0, 0);"""
		data_tuple = (message.from_user.id, nameRep, surnameRep, dateofbirthRep, schoolclassRep)
		cursor.execute(insert_data, data_tuple)
		sqlite_connection.commit()
		cursor.close()
	except sqlite3.OperationalError:
		pass


	keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
	key_rus_lang = types.InlineKeyboardButton(text='Русский Язык', callback_data='rus_lang'); #кнопка «Да»
	keyboard.add(key_rus_lang); #добавляем кнопку в клавиатуру
	key_math= types.InlineKeyboardButton(text='Математика', callback_data='math');
	keyboard.add(key_math);
	key_phys= types.InlineKeyboardButton(text='Физика', callback_data='phys');
	keyboard.add(key_phys);
	key_chem= types.InlineKeyboardButton(text='Химия', callback_data='chem');
	keyboard.add(key_chem);
	key_bio= types.InlineKeyboardButton(text='Биология', callback_data='bio');
	keyboard.add(key_bio);
	key_soc= types.InlineKeyboardButton(text='Обществознание', callback_data='soc');
	keyboard.add(key_soc);
	key_hist= types.InlineKeyboardButton(text='История', callback_data='hist');
	keyboard.add(key_hist);
	question = 'Репетитором по какому предмету ты хотел(а) бы быть?';
	bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "yes":
		bot.send_message(call.message.chat.id, 'Запомню : )');
	elif call.data == "no":
		bot.send_message(call.message.chat.id, 'Что не так?');
	elif call.data == "student":

		bot.send_message(call.message.chat.id, 'Как тебя зовут?');
		bot.register_next_step_handler(call.message, get_name);

	elif call.data == "repetitor":

		bot.send_message(call.message.chat.id, 'Как тебя зовут?');
		bot.register_next_step_handler(call.message, get_nameRep);

	elif call.data == 'rus_lang':
		rul = 'Russian Language'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE repetitors 
						SET course = ?
						WHERE id = ?;"""
		data = (rul, call.message.chat.id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
	elif call.data == 'math':
		mathl = 'Mathematics'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE repetitors 
						SET course = ?
						WHERE id = ?;"""
		data = (mathl, call.message.chat.id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
	elif call.data == 'phys':
		physl = 'Physics'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE repetitors 
						SET course = ?
						WHERE id = ?;"""
		data = (physl, call.message.chat.id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
	elif call.data == 'chem':
		cheml = 'Chemistry'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE repetitors 
						SET course = ?
						WHERE id = ?;"""
		data = (cheml, call.message.chat.id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
	elif call.data == 'bio':
		biol = 'Biology'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE repetitors 
						SET course = ?
						WHERE id = ?;"""
		data = (biol, call.message.chat.id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
	elif call.data == 'soc':
		socl = 'Social'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE repetitors 
						SET course = ?
						WHERE id = ?;"""
		data = (socl, call.message.chat.id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
	elif call.data == 'hist':
		histl = 'History'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE repetitors 
						SET course = ?
						WHERE id = ?;"""
		data = (histl, call.message.chat.id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()


bot.polling(none_stop=True, interval=0)