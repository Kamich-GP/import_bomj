# Основная логика бота
import calendar

import telebot
import buttons
import database


# Создаем объект бота
bot = telebot.TeleBot('TOKEN')
# Временные данные
users = {}
admins = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем наличие пользователя
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!')
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Привет! Давай начнем регистрацию!\n'
                                  'Напиши свое имя!', reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    # Определяем имя пользователя
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправь свой номер!', reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)


# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id
    # Проверяем отправлен ли номер через кнопку
    if message.contact:
        user_num = message.contact.phone_number
        # Заносим пользователя в БД
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку!')
        # Возврат на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)


# Выбор количества
@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'])
def choose_count(call):
    user_id = call.message.chat.id
    if call.data == 'increment':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choose_pr_count
                                      (database.get_exact_pr(users[user_id]['pr_name'])[3], 'increment',
                                       users[user_id]['pr_count']))
        users[user_id]['pr_count'] += 1
    elif call.data == 'decrement':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choose_pr_count
                                      (database.get_exact_pr(users[user_id]['pr_name'])[3], 'decrement',
                                       users[user_id]['pr_count']))
        users[user_id]['pr_count'] -= 1
    elif call.data == 'to_cart':
        pr_name = database.get_exact_pr(users[user_id]['pr_name'])[1]
        database.add_to_cart(user_id, pr_name, users[user_id]['pr_count'])
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Товар успешно помещен в корзину! Желаете что-то еще?',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    elif call.data == 'back':
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Возвращаю вас обратно в меню',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))


# Работа с корзиной
@bot.callback_query_handler(lambda call: call.data in ['cart', 'order', 'clear'])
def cart_handle(call):
    user_id = call.message.chat.id
    text = 'Ваша корзина:\n\n'

    if call.data == 'cart':
        user_cart = database.show_cart(user_id)
        total = 0.0
        for i in user_cart:
            text += (f'Товар: {i[1]}\n'
                     f'Количество: {i[2]}\n\n')
            total += database.get_exact_price(i[1])[0] * i[2]
        text += f'Итого: ${round(total, 2)}'
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, text, reply_markup=buttons.cart_buttons())
    elif call.data == 'clear':
        database.clear_cart(user_id)
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Ваша корзина очищена!',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    elif call.data == 'order':
        text = text.replace('Ваша корзина:', f'Новый заказ!\nКлиент: @{call.message.chat.username}')
        user_cart = database.show_cart(user_id)
        total = 0.0
        for i in user_cart:
            text += (f'Товар: {i[1]}\n'
                     f'Количество: {i[2]}\n\n')
            total += database.get_exact_price(i[1])[0] * i[2]
        text += f'Итого: ${round(total, 2)}'
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Для оформления заказа, отправьте локацию.', reply_markup=buttons.loc_button())
        # Перевод на этап получения локации
        bot.register_next_step_handler(call.message, get_loc, text)


# Этап получения локации
def get_loc(message, text):
    user_id = message.from_user.id
    # Проверка на правильность отправки локации
    if message.location:
        bot.send_message('YOUR_USER_ID', text)
        bot.send_location('YOUR_USER_ID', latitude=message.location.latitude, longitude=message.location.longitude)
        database.make_order(user_id)
        bot.send_message(user_id, 'Ваш заказ был оформлен! Скоро с вами свяжутся!')
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        # Возвращение на этап получения локации
        bot.register_next_step_handler(message, get_loc, text)


# Выбор товара
@bot.callback_query_handler(lambda call: int(call.data) in [i[0] for i in database.get_all_pr()])
def choose_product(call):
    user_id = call.message.chat.id
    pr_info = database.get_exact_pr(int(call.data))
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    bot.send_photo(user_id, photo=pr_info[5], caption=f'{pr_info[1]}\n\n'
                                                      f'Описание: {pr_info[2]}\n'
                                                      f'Количество: {pr_info[3]}\n'
                                                      f'Цена: ${pr_info[4]}',
                   reply_markup=buttons.choose_pr_count(pr_info[3]))
    users[user_id] = {'pr_name': pr_info[0], 'pr_count': 1}


# Запуск бота
bot.polling()
