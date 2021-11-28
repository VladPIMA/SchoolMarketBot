import telebot
import sqlite3
import uuid
import settings
import change
import menu
import taxi
from telebot import types

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

# создание и подключение к бд
try:
	sqlite_connection = sqlite3.connect('schoolmarket.db', check_same_thread = False)
	cursor = sqlite_connection.cursor()

	createCommand = """
	CREATE TABLE students (
		"id"	INTEGER,
		"name"	TEXT,
		"surname"	TEXT,
		"dateofbirth" TEXT,
		"schoolclass"	INTEGER,
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
		"id"	INTEGER,
		"name"	TEXT,
		"surname"	TEXT,
		"dateofbirth"	TEXT,
		"schoolclass"	INTEGER,
		"course"	TEXT,
		"rank"	TEXT,
		"level"	TEXT,
		"rating"	INTEGER,
		"currency"	INTEGER
	);"""

	cursor.execute(createCommand)
	cursor.close()
except sqlite3.OperationalError:
	pass

try:
	cursor = sqlite_connection.cursor()
	createCommand = """
	CREATE TABLE orders (
		"id"	TEXT,
		"course"	TEXT,
		"schoolclass"	INTEGER,
		"theme"	TEXT,
		"rankrep"	TEXT,
		"idstudent"	INTEGER,
		"username" TEXT,
		"namestudent"	TEXT,
		"price"	INTEGER,
	);"""

	cursor.execute(createCommand)
	cursor.close()
except sqlite3.OperationalError:
	pass

# поиск пользователя в бд
def get_user_info(id):
	stud = "student"
	rep = "repetitor"
	try:
		sqlite_connection = sqlite3.connect('schoolmarket.db')
		cursor = sqlite_connection.cursor()

		sql_select_query = """SELECT * FROM repetitors WHERE id = ?"""
		cursor.execute(sql_select_query, (id,))
		records = cursor.fetchone()
		if records is None:
			try:
				sqlite_connection = sqlite3.connect('schoolmarket.db')
				cursor = sqlite_connection.cursor()

				sql_select_query = """SELECT * FROM students WHERE id = ?"""
				cursor.execute(sql_select_query, (id,))
				records = cursor.fetchone()
				if records is None:
					return 0

					cursor.close()
				else:
					return stud

			except sqlite3.Error as error:
				print("Ошибка при работе с SQLite", error)
		else:
			return rep

			cursor.close()

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)

#@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def start(message):
	global status
	chat_id = message.from_user.id

	# вывод информации о пользователе сделать через клавиатуру
#	if get_user_info(chat_id) != 0:
	if get_user_info(chat_id) == "student":
		bot.send_message(message.from_user.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.student_menu())
	elif get_user_info(chat_id) == "repetitor":
		bot.send_message(message.from_user.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())
	# if == 0 то регистрация
	elif get_user_info(chat_id) == 0:
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


''' РЕГИСТРАЦИЯ УЧЕНИКА '''

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
	bot.send_message(message.from_user.id, 'В каком ты классе?' + '\n' + '(Напиши только цифру)');
	bot.register_next_step_handler(message, get_schoolClass);

def get_schoolClass(message):
	global schoolclass
	global currency
	schoolclass = 0
	schoolclass = int(message.text)
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


''' РЕГИСТРАЦИЯ РЕПЕТИТОРА '''

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
	bot.send_message(message.from_user.id, 'В каком ты классе?'  + '\n' + '(Напиши только цифру)');
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
		insert_data = """INSERT INTO repetitors(id, name, surname, dateofbirth, schoolclass, rank, level, rating, currency)
							VALUES (?, ?, ?, ?, ?, 'Эконом', 'Новичок', 0, 0);"""
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


''' СОЗДАНИЕ ЗАКАЗА '''

def get_schoolclass(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, 'Прекрасно!', reply_markup=hide_markup)

	global schoolclass
	global idstudent
	global namestudent
	global unique_id
	global usernamestudtg

	idstudent = message.from_user.id
	unique_id = str(uuid.uuid1())
	usernamestudtg = message.from_user.username

	try:
		sqlite_connection = sqlite3.connect('schoolmarket.db')
		cursor = sqlite_connection.cursor()

		if get_user_info(message.from_user.id) == "students":
			sqlite_select_query = """SELECT * from students where id = ?"""
		elif get_user_info(message.from_user.id) == "repetitor":
			sqlite_select_query = """SELECT * from repetitors where id = ?"""

		cursor.execute(sqlite_select_query, (idstudent, ))
		record = cursor.fetchone()
		schoolclass = int(record[4])

		
		if get_user_info(message.from_user.id) == "students":
			sqlite_select_query = """SELECT * from students where id = ?"""
		elif get_user_info(message.from_user.id) == "repetitor":
			sqlite_select_query = """SELECT * from repetitors where id = ?"""

		cursor.execute(sqlite_select_query, (idstudent, ))
		record = cursor.fetchone()
		namestudent = record[1]  + ' ' + record[2]

		insert_data = """INSERT INTO orders(id, schoolclass, theme, idstudent, username, namestudent, price)
							VALUES (?, ?, "0", ?, ?, ?, 0);"""
		data_tuple = (unique_id, schoolclass, idstudent, usernamestudtg, namestudent)
		cursor.execute(insert_data, data_tuple)
		sqlite_connection.commit()

		cursor.close()

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)
	get_course(idstudent)


def get_course(chat_id_key):

	keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
	key_rus_lang = types.InlineKeyboardButton(text='Русский Язык', callback_data='rus_lango'); #кнопка «Да»
	keyboard.add(key_rus_lang); #добавляем кнопку в клавиатуру
	key_math= types.InlineKeyboardButton(text='Математика', callback_data='matho');
	keyboard.add(key_math);
	key_phys= types.InlineKeyboardButton(text='Физика', callback_data='physo');
	keyboard.add(key_phys);
	key_chem= types.InlineKeyboardButton(text='Химия', callback_data='chemo');
	keyboard.add(key_chem);
	key_bio= types.InlineKeyboardButton(text='Биология', callback_data='bioo');
	keyboard.add(key_bio);
	key_soc= types.InlineKeyboardButton(text='Обществознание', callback_data='soco');
	keyboard.add(key_soc);
	key_hist= types.InlineKeyboardButton(text='История', callback_data='histo');
	keyboard.add(key_hist);
	question = 'По какому предмету ты хотел(а) бы заказать урок?';
	bot.send_message(chat_id_key, text=question, reply_markup=keyboard)

def get_theme(message):
	global theme
	theme = message.text

	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	econom = types.KeyboardButton(text="Эконом")
	keyboard.add(econom)
	comfort = types.KeyboardButton(text="Комфорт")
	keyboard.add(comfort)
	business = types.KeyboardButton(text="Бизнес")
	keyboard.add(business)
	elites = types.KeyboardButton(text="Элит")
	keyboard.add(elites)

	bot.send_message(message.from_user.id, 'Какого класса должен быть твой репетитор(Эконом, Комфорт, Бизнес, Элит)? ' + '\n'
											 + 'Помни, что чем элитнее класс, тем дороже стоят услуги репетитора!', reply_markup=keyboard)
	bot.register_next_step_handler(message, get_rankrep)

def get_rankrep(message):
	global rankrep
	rankrep = message.text
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, 'Сколько коинов ты предлагаешь за этот урок?', reply_markup=hide_markup)
	bot.register_next_step_handler(message, get_price)

def get_price(message):
	global price
	price = int(message.text)
	chat_id_key = message.from_user.id
	
	bot.send_message(message.from_user.id, 'Твой заказ принят, ожидай отклика от репетитора, у которого класс: ' +
					 taxi.update_theme_and_price(message.from_user.id, unique_id, course_order, schoolclass, theme, rankrep, price))


''' ПОИСК ЗАКАЗА РЕПЕТИТОРОМ '''

def get_rep_info(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, 'Прекрасно!', reply_markup=hide_markup)

	global schoolclassRepet
	global course
	global unique_id_order

	sqlite_connection = sqlite3.connect('schoolmarket.db')
	cursor = sqlite_connection.cursor()

	sql_select_query = """SELECT * FROM repetitors WHERE id = ?"""
	cursor.execute(sql_select_query, (message.from_user.id,))
	records = cursor.fetchone()
	schoolclassRepet = int(records[4])
	course = records[5]
	
	sql_select_query = """SELECT * FROM orders WHERE schoolclass <= ? AND course = ?"""
	cursor.execute(sql_select_query, (schoolclassRepet, course,))
	records = cursor.fetchall()
	mssg = ''
	count = 1
	for row in records:
		msg = ("Заказ №" + str(count) + ": " + '\n' + "Имя ученика: " + row[7] + '\n'
				 + "Школьный класс ученика: " + str(row[2]) + '\n'
				 + "Проблемная тема: " + row[3] + '\n' 
				 + "Предлагаемая цена за урок: " + str(row[8]) + '\n' + '\n')
#			mssg += msg
		count+= 1

		unique_id_order = row[0]
		keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
		key_order = types.InlineKeyboardButton(text='Выбрать этот заказ', callback_data='order'); #кнопка «Да»
		keyboard.add(key_order); #добавляем кнопку в клавиатуру
		bot.send_message(message.from_user.id, msg, reply_markup=keyboard)

	sqlite_connection.commit()
	cursor.close()


''' ХЭНДЛЕР ДЛЯ КНОПОК КЛАВИАТУРЫ '''

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	global course_order
	chat_id_key = call.message.chat.id

	if call.data == "yes":
		bot.send_message(call.message.chat.id, 'Запомню : )');

		if get_user_info(chat_id_key) != 0:

			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.student_menu())

	elif call.data == "no":
		bot.send_message(call.message.chat.id, 'Что не так?');
	elif call.data == "student":

		bot.send_message(call.message.chat.id, 'Как тебя зовут?');
		bot.register_next_step_handler(call.message, get_name);
		bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

	elif call.data == "repetitor":

		bot.send_message(call.message.chat.id, 'Как тебя зовут?');
		bot.register_next_step_handler(call.message, get_nameRep);
		bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

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

		if get_user_info(chat_id_key) != 0:

			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())

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

		if get_user_info(chat_id_key) != 0:
			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())

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

		if get_user_info(chat_id_key) != 0:

			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())

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

		if get_user_info(chat_id_key) != 0:

			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())

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

		if get_user_info(chat_id_key) != 0:

			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())

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

		if get_user_info(chat_id_key) != 0:

			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())

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

		if get_user_info(chat_id_key) != 0:

			bot.send_message(call.message.chat.id, text = 'Что бы ты хотел сделать?', reply_markup = menu.repetitors_menu())

	elif call.data == 'profile':
		if get_user_info(call.message.chat.id) == 'repetitor':
			cursor = sqlite_connection.cursor()
			sql_select_query = """SELECT * FROM repetitors WHERE id = ?"""
			cursor.execute(sql_select_query, (call.message.chat.id, ))
			record = cursor.fetchone()
			bot.send_message(call.message.chat.id, "ID: " + str(record[0]) + '\n' + "Имя: " + str(record[1]) + '\n' +
													 "Фамилия: " + record[2] + '\n' + "Дата рождения: " + record[3] + '\n' +
													  "Класс: " + str(record[4]) + '\n' + "Предмет репетиторства: " + record[5] + '\n' +
													  "Ранг: " + str(record[6]) + '\n' + "Уровень: " + str(record[7]) + '\n' +
													  "Рейтинг: " + str(record[8]) + '\n' + "Баланс: " + str(record[9]))
			cursor.close()
			bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

		elif get_user_info(call.message.chat.id) == 'student':
			cursor = sqlite_connection.cursor()
			sql_select_query = """SELECT * FROM students WHERE id = ?"""
			cursor.execute(sql_select_query, (call.message.chat.id, ))
			record = cursor.fetchone()
			bot.send_message(call.message.chat.id, "ID: " + str(record[0]) + '\n' + "Имя: " + record[1] + '\n' +
													 "Фамилия: " + record[2] + '\n' + "Дата рождения: " + record[3] + '\n' +
													  "Класс: " + str(record[4]) + '\n' + "Баланс: " + str(record[5]))
			cursor.close()
			bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

	elif call.data == 'taxi':
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		yes = types.KeyboardButton(text="Да, всё верно!")
		keyboard.add(yes)

		bot.send_message(call.message.chat.id, "Ты хочешь найти себе репетитора?", reply_markup=keyboard)
		bot.register_next_step_handler(call.message, get_schoolclass)
		bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

	elif call.data == 'taxirep':
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		yes = types.KeyboardButton(text="Да, всё верно!")
		keyboard.add(yes)

		bot.send_message(call.message.chat.id, "Ты хочешь найти себе ученика?", reply_markup=keyboard)
		bot.register_next_step_handler(call.message, get_rep_info)
		bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)



	elif call.data == 'rus_lango':
		course_order = 'Russian Language'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE orders 
						SET course = ?
						WHERE id = ?;"""
		data = (course_order, unique_id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()

		if (taxi.rep_course_is_exist(course_order) == 'available'):
			bot.send_message(call.message.chat.id, 'Какая тема?')
			bot.register_next_step_handler(call.message, get_theme)
		else:
			cursor = sqlite_connection.cursor()
			sql_select_query = """DELETE FROM orders WHERE id = ?"""
			cursor.execute(sql_select_query, (unique_id,))
			sqlite_connection.commit()
			bot.send_message(call.message.chat.id, 'Извините, но репетиторов выбранного вами класса ещё нет.')

	elif call.data == 'matho':
		course_order = 'Mathematics'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE orders 
						SET course = ?
						WHERE idt = ?;"""
		data = (course_order, unique_id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
		if (taxi.rep_course_is_exist(course_order) == 'available'):
			bot.send_message(call.message.chat.id, 'Какая тема?')
			bot.register_next_step_handler(call.message, get_theme)
		else:
			cursor = sqlite_connection.cursor()
			sql_select_query = """DELETE FROM orders WHERE id = ?"""
			cursor.execute(sql_select_query, (unique_id,))
			sqlite_connection.commit()
			bot.send_message(call.message.chat.id, 'Извините, но репетиторов выбранного вами класса ещё нет.')

	elif call.data == 'physo':
		course_order = 'Physics'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE orders 
						SET course = ?
						WHERE id = ?;"""
		data = (course_order, unique_id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()
		if (taxi.rep_course_is_exist(course_order) == 'available'):
			bot.send_message(call.message.chat.id, 'Какая тема?')
			bot.register_next_step_handler(call.message, get_theme)
		else:
			cursor = sqlite_connection.cursor()
			sql_select_query = """DELETE FROM orders WHERE id = ?"""
			cursor.execute(sql_select_query, (unique_id,))
			sqlite_connection.commit()
			bot.send_message(call.message.chat.id, 'Извините, но репетиторов выбранного вами класса ещё нет.')
			

	elif call.data == 'chemo':
		course_order = 'Chemistry'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE orders 
						SET course = ?
						WHERE id = ?;"""
		data = (course_order, unique_id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()

		if (taxi.rep_course_is_exist(course_order) == 'available'):
			bot.send_message(call.message.chat.id, 'Какая тема?')
			bot.register_next_step_handler(call.message, get_theme)
		else:
			cursor = sqlite_connection.cursor()
			sql_select_query = """DELETE FROM orders WHERE id = ?"""
			cursor.execute(sql_select_query, (unique_id,))
			sqlite_connection.commit()
			bot.send_message(call.message.chat.id, 'Извините, но репетиторов выбранного вами класса ещё нет.')

	elif call.data == 'bioo':
		course_order = 'Biology'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE orders 
						SET course = ?
						WHERE id = ?;"""
		data = (course_order, unique_id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()

		if (taxi.rep_course_is_exist(course_order) == 'available'):
			bot.send_message(call.message.chat.id, 'Какая тема?')
			bot.register_next_step_handler(call.message, get_theme)
		else:
			cursor = sqlite_connection.cursor()
			sql_select_query = """DELETE FROM orders WHERE id = ?"""
			cursor.execute(sql_select_query, (unique_id,))
			sqlite_connection.commit()
			bot.send_message(call.message.chat.id, 'Извините, но репетиторов выбранного вами класса ещё нет.')

	elif call.data == 'soco':
		course_order = 'Social'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE orders 
						SET course = ?
						WHERE id = ?;"""
		data = (course_order, unique_id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()

		if (taxi.rep_course_is_exist(course_order) == 'available'):
			bot.send_message(call.message.chat.id, 'Какая тема?')
			bot.register_next_step_handler(call.message, get_theme)
		else:
			cursor = sqlite_connection.cursor()
			sql_select_query = """DELETE FROM orders WHERE id = ?"""
			cursor.execute(sql_select_query, (unique_id,))
			sqlite_connection.commit()
			bot.send_message(call.message.chat.id, 'Извините, но репетиторов выбранного вами класса ещё нет.')

	elif call.data == 'histo':
		course_order = 'History'
		cursor = sqlite_connection.cursor()
		updateCourse = """UPDATE orders 
						SET course = ?
						WHERE id = ?;"""
		data = (course_order, unique_id)
		cursor.execute(updateCourse, data)
		sqlite_connection.commit()
		cursor.close()

		if (taxi.rep_course_is_exist(course_order) == 'available'):
			bot.send_message(call.message.chat.id, 'Какая тема?')
			bot.register_next_step_handler(call.message, get_theme)
		else:
			cursor = sqlite_connection.cursor()
			sql_select_query = """DELETE FROM orders WHERE id = ?"""
			cursor.execute(sql_select_query, (unique_id,))
			sqlite_connection.commit()
			bot.send_message(call.message.chat.id, 'Извините, но репетиторов выбранного вами класса ещё нет.')

	elif call.data == 'order':
		bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

		# СДЕЛАТЬ ВЫВОД ИНФОРМАЦИИ УЧЕНИКУ И РЕПЕТУ О ПРИНЯТИИ ЗАКАЗА
		# СДЕЛАТЬ ПОДТВЕРЖДЕНИЕ ПРОШЕДШЕГО ЗАНЯТИЯ
		cursor = sqlite_connection.cursor()
		sql_select_query = """SELECT * FROM orders WHERE id = ?"""
		cursor.execute(sql_select_query, (unique_id_order,))
		record = cursor.fetchone()
		id_student = int(record[5])
		name_student = record[6]
		

		# msg репету
		bot.send_message(call.message.chat.id, 'Замечательно! Договориcь о времени и месте занятия в личных сообщениях с учеником - @' + name_student)
		bot.send_message(call.message.chat.id, "Имя и фамилия ученика: " + record[7] + '\n' + "Класс: " + str(record[2]) + '\n' +
												"Проблемная тема: " + record[3] + '\n' + "Предлагаемая цена за урок: " + str(record[8]))


		# msg ученику
		bot.send_message(id_student, 'Спешу тебя обрадовать! Твой заказ принял репетитор - @' + call.message.chat.username + '\n'
							+ 'Скорее договаривайтесь о месте и времени занятия в личных сообщениях!')

bot.polling(none_stop=True, interval=0)