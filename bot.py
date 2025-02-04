# Основная логика бота
import telebot
import buttons
import database


# Создаем объект бота
bot = telebot.TeleBot('TOKEN')


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


# Запуск бота
bot.polling()
