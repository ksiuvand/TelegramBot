import config
import telebot
from telebot import types  # кнопки
from string import Template
import mysql.connector


bot = telebot.TeleBot('1749134886:AAFrVXIR8eTELnlAeYeIsTcQ4qJ8rmwJOwk')


db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="13042005",
  port="3306",
  database="foood"
)

# print(mydb)

#####################################Работа с базой данных############################################

cursor = db.cursor()


# cursor.execute("CREATE DATABASE foood")

# cursor.execute("SHOW DATABASES")
#
# for x in cursor:
#     print(x)


# cursor.execute("CREATE TABLE users (fullname VARCHAR(255), city VARCHAR(255), age VARCHAR(255), sex VARCHAR(255))")


# cursor.execute("SHOW TABLES")
#
# for x in cursor:
#     print(x)


# cursor.execute("ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE)")


# sql = "INSERT INTO users (fullname, city, age, sex, user_id) VALUES (%s, %s, %s, %s, %s)"

# val = ("John", "Екатеринбург", 13, "женский", 3)

# cursor.execute(sql, val)
#
# db.commit()
#
# print(cursor.rowcount, "запись добавлена")

#####################################################################

user_dict = {}

c = ''


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'age',
                'weight', 'height', 'aktiv',
                'sex', 'zel', 'ozenka']

        for key in keys:
            self.key = None


# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/registr')
    itembtn3 = types.KeyboardButton('/thank')

    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Здравствуйте, "
                     + message.from_user.first_name
                     + ", я бот, чтобы вы хотели узнать?",
                     reply_markup=markup)


# /about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "Я составлю вам меню на 3 дня, " +
                                      "которое поможет вам начать питаться " +
                                      "правильно и поддерживать здоровый образ жизни." +
                                      "Чтобы начать, нажмите на кнопку /registr и введите " +
                                      "свои данные. Затем вы получите" +
                                      "меню на первые 3 дня.")


# /thank
@bot.message_handler(commands=['thank'])
def send_req(message):
    bot.send_message(message.chat.id, 'Спасибо за то, что пользуетесь нашим ботом и надеемся, что вам все нравится.')





# /registr
@bot.message_handler(commands=["registr"])
def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    itembtn1 = types.KeyboardButton('Екатеринбург')
    itembtn2 = types.KeyboardButton('Москва')
    itembtn3 = types.KeyboardButton('Санкт-Петербург')
    itembtn4 = types.KeyboardButton('Казань')
    itembtn5 = types.KeyboardButton('Самара')
    itembtn6 = types.KeyboardButton('Другой')

    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

    msg = bot.send_message(message.chat.id, 'В каком городе вы живете?', reply_markup=markup)

    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Введите фамилию и имя', reply_markup=markup)

        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message, 'ooops1!!')


def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        user.fullname = message.text

        msg = bot.send_message(chat_id, 'Укажите ваш номер телефона (если нет, отправьте 1)')

        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops2!!')


def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]

        user.phone = message.text

        msg = bot.send_message(chat_id, 'Сколько вам лет?')

        bot.register_next_step_handler(msg, process_age_step)

    except Exception as e:
        msg = bot.reply_to(message, 'oops3!')

        bot.register_next_step_handler(msg, process_phone_step)


def process_age_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        user.age = message.text

        msg = bot.send_message(chat_id, 'Сколько вы весите?')

        bot.register_next_step_handler(msg, process_weight_step)

    except Exception as e:
        bot.reply_to(message, 'ooops4!!')


def process_weight_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        user.weight = message.text

        msg = bot.send_message(chat_id, 'Какой у вас рост?')

        bot.register_next_step_handler(msg, process_height_step)

    except Exception as e:
        bot.reply_to(message, 'ooops5!!')


def process_height_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        user.height = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        itembtn1 = types.KeyboardButton('Очень активен')
        itembtn2 = types.KeyboardButton('Активен')
        itembtn3 = types.KeyboardButton('Почти не активен')

        markup.add(itembtn1, itembtn2, itembtn3)

        msg = bot.send_message(chat_id, 'Насколько вы активны в течении дня?', reply_markup=markup)

        bot.register_next_step_handler(msg, process_aktiv_step)

    except Exception as e:
        bot.reply_to(message, 'ooops6!!')


def process_aktiv_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        user.aktiv = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        itembtn1 = types.KeyboardButton('Мужской')
        itembtn2 = types.KeyboardButton('Женский')

        markup.add(itembtn1, itembtn2)

        msg = bot.send_message(chat_id, 'Укажите ваш пол', reply_markup=markup)

        bot.register_next_step_handler(msg, process_sex_step)

    except Exception as e:
        bot.reply_to(message, 'ooops7!!')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        user.sex = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        itembtn1 = types.KeyboardButton('Похудеть')
        itembtn2 = types.KeyboardButton('Набрать')
        itembtn3 = types.KeyboardButton('Для здоровья')
        itembtn4 = types.KeyboardButton('Другое')

        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(chat_id, 'Почему вы хотите питаться правильно?', reply_markup=markup)

        bot.register_next_step_handler(msg, process_zel_step)
    except Exception as e:
        print('oops8')


def process_zel_step(message):
    global c
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id

        user = user_dict[chat_id]

        user.zel = message.text

        c = user.zel
        # заносим данные в базу данных
        sql = "INSERT INTO users (fullname, city, age, sex, user_id) VALUES (%s, %s, %s, %s, %s)"

        val = (user.fullname, user.city, user.age, user.sex, user_id)

        cursor.execute(sql, val)

        db.commit()

        bot.send_message(chat_id, 'Вы успешно зарегестрировались!')

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")

        bot.send_message(chat_id, 'Ваше меню на первые 3 дня:')
        # отправить в группу
        # bot.send_message(config.chat_id, getRegData(user, 'Заявка от бота', bot.get_me().username),
        #                  parse_mode="Markdown")

    except Exception as e:
        print('ooops9!!')
    if c == 'Похудеть':
        bot.send_message(message.chat.id, 'День 1:\n' +
                                          'Утренний прием пищи: рис 200 г, сливочное масло 10 г, один банан или '+
                                          'одно яблоко, черный кофе.\n ' +
                                          'Перекус: подсушенный серый хлеб, вареное яйцо, томат.\n' +
                                          'Дневной прием пищи: скумбрия на пару 200 г, салат из пекинской капусты с '+
                                          'горошком и подсолнечным маслом 180 грамм. \n' +
                                          'Второй перекус: нежирный творожок 120 г с ложкой 10% сметаны, зеленое '+
                                          'яблоко, 200 мл чая. \n' +
                                          'Вечерний прием пищи: отварные овощи 220 г, запеченный кусок говядины '+
                                          '140 г \n' +
                                          'День 2:\n' +
                                          'Утренний прием пищи: бутерброд из кусочка цельнозернового хлеба, сливочный'+
                                          ' творог и пластик огурца, виноград 100 г, чай или кофе с медом. \n' +
                                          'Перекус: творог 50 г с чайной ложкой меда.\n' +
                                          'Дневной прием пищи: бульон мясной 200 г, свежий салат из пекинской капусты'+
                                          ' с огурцом и томатом, заправленным соком лимонным.\n' +
                                          'Второй перекус: красное яблоко и одно киви, чай зеленый или травяной.\n' +
                                          'Вечерний прием пищи: постная говядина 200 г, два свежих огурца. \n' +
                                          'День 3:\n' +
                                          'Утренний прием пищи: вареная овсянка без молока — 210 г, ложка меда, '+
                                          'авокадо и несладкий кофе. \n' +
                                          'Перекус: орешки кедровые или грецкие 60 г, зеленое яблоко, чай, кружок '+
                                          'лимона.\n' +
                                          'Дневной прием пищи: бурый рис 150 г, столько же припущенных овощей.\n' +
                                          'Второй перекус: запеканка из творога, манки, банана 150 г, чай травяной.\n' +
                                          'Вечерний прием пищи: морепродукты очищенные 200 г, два огурца и один томат.')
    elif c == 'Для здоровья':
        bot.send_message(message.chat.id, 'День 1:\n' +
                         'Утренний прием пищи: рис 200 г, сливочное масло 10 г, один банан или одно яблоко, '+
                         'черный кофе.\n ' +
                         'Перекус: подсушенный серый хлеб, вареное яйцо, томат.\n' +
                         'Дневной прием пищи: скумбрия на пару 200 г, салат из пекинской капусты с горошком и '+
                         'подсолнечным маслом 180 грамм. \n' +
                         'Второй перекус: нежирный творожок 120 г с ложкой 10% сметаны, зеленое яблоко, 200 мл чая. \n' +
                         'Вечерний прием пищи: отварные овощи 220 г, запеченный кусок говядины 140 г \n' +
                         'День 2:\n' +
                         'Утренний прием пищи: бутерброд из кусочка цельнозернового хлеба, сливочный творог и '+
                         'пластик огурца, виноград 100 г, чай или кофе с медом. \n' +
                         'Перекус: творог 50 г с чайной ложкой меда.\n' +
                         'Дневной прием пищи: бульон мясной 200 г, свежий салат из пекинской капусты с огурцом и '+
                         'томатом, заправленным соком лимонным.\n' +
                         'Второй перекус: красное яблоко и одно киви, чай зеленый или травяной.\n' +
                         'Вечерний прием пищи: постная говядина 200 г, два свежих огурца. \n' +
                         'День 3:\n' +
                         'Утренний прием пищи: вареная овсянка без молока — 210 г, ложка меда, авокадо и несладкий '+
                         'кофе. \n' +
                         'Перекус: орешки кедровые или грецкие 60 г, зеленое яблоко, чай, кружок лимона.\n' +
                         'Дневной прием пищи: бурый рис 150 г, столько же припущенных овощей.\n' +
                         'Второй перекус: запеканка из творога, манки, банана 150 г, чай травяной.\n' +
                         'Вечерний прием пищи: морепродукты очищенные 200 г, два огурца и один томат.')
    elif c == 'Набрать' or c == 'Другое':
        bot.send_message(message.chat.id, 'День 1:\n'
                                          'Завтрак: Рисовая молочная каша со сливочным маслом, фрукты.\n' +
                         'Второй завтрак: Пирожок с мясом или овощами.\n' +
                         'Обед: Суп с макаронными изделиями и фрикадельками из говядины и свинины, со сметаной. '+
                         'Овощной салат, белый хлеб. \n'
                         'Полдник: Молоко с овсяным печеньем, пряниками.\n' +
                         'Ужин: Мясо, запеченное в духовке, с овощным салатом, хлеб. Фруктовый десерт с медом.\n' +
                         'Второй ужин: Стакан жирного молока.\n' +
                         'День 2:\n' +
                         'Завтрак: Геркулес на меду, с орехами и кусочками фруктов.\n' +
                         'Второй завтрак: Омлет с сыром, помидоры.\n' +
                         'Обед: Уха, макароны с сыром, белый хлеб.\n' +
                         'Полдник: Бутерброд с ветчиной и зеленью.\n' +
                         'Ужин: Рыба с рисом, хлеб, фрукты.\n' +
                         'Второй ужин: Стакан ряженки или кефира.\n' +
                         'День 3:\n' +
                         'Завтрак: Сладкий кофе со сливками, сдобная булочка и тосты с вареньем.\n' +
                         'Второй завтрак: Пирожок с мясом или овощами.\n' +
                         'Обед: Борщ со сметаной, картофельное пюре с жареной рыбой.\n' +
                         'Полдник:Фруктовое мороженое, семена подсолнечника или тыквы. Фруктовый йогурт, банан.\n' +
                         'Ужин: Гречка с молоком, сухофрукты, хлеб с маслом.\n' +
                         'Второй ужин: Йогурт.\n')



def getRegData(user, title, name):
    t = Template(
        '$title *$name* \n Город: *$userCity* \n ФИО: *$fullname* \n Телефон: *$phone* \n Возраст: *$age* \n Вес: *$weight* \n Рост: *$height* \n Активность: *$aktiv* \n Пол: *$sex* \n Цель здорового питания: *$zel*')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        'phone': user.phone,
        'age': user.age,
        'weight': user.weight,
        'height': user.height,
        'aktiv': user.aktiv,
        'sex': user.sex,
        'zel': user.zel,
    })


# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, 'О нас - /about\nРегистрация - /registr\nПомощь - /help\nБлагодарность - /thank')


# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')


bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)