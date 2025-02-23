# Работа с кнопками
from telebot import types


# Кнопки отправки номера
def num_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    num = types.KeyboardButton('Отправить номер📞', request_contact=True)
    # Добавляем кнопку в пространство
    kb.add(num)

    return kb


# Кнопки отправки локации
def loc_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    loc = types.KeyboardButton('Отправить локацию📍', request_location=True)
    # Добавляем кнопку в пространство
    kb.add(loc)

    return kb


# Кнопки главного меню
def main_menu(products):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    cart = types.InlineKeyboardButton(text='Корзина🛒', callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=i[0]) for i in products]
    # Добавляем кнопки
    kb.add(*all_products)
    kb.row(cart)

    return kb


# Кнопки выбора количества
def choose_pr_count(pr_amount, plus_or_minus='', amount=1):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    to_cart = types.InlineKeyboardButton(text='В корзину🛒', callback_data='to_cart')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')

    # Алгоритм изменения количества
    if plus_or_minus == 'increment':
        if amount <= pr_amount:
            count = types.InlineKeyboardButton(text=str(amount + 1), callback_data=str(amount + 1))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            count = types.InlineKeyboardButton(text=str(amount - 1), callback_data=str(amount - 1))

    # Добавляем кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(back, to_cart)

    return kb


# Кнопки корзины
def cart_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    order = types.InlineKeyboardButton(text='Оформить заказ✅', callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить корзину🗑️', callback_data='clear')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    # Добавляем кнопки в пространство
    kb.add(order, clear)
    kb.row(back)

    return kb


# Кнопки админ панели
def admin_buttons():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Добавить продукт')
    but2 = types.KeyboardButton('Удалить продукт')
    but3 = types.KeyboardButton('Изменить продукт')
    but4 = types.KeyboardButton('Перейти в главное меню')
    # Добавляем кнопки
    kb.add(but1, but2, but3)
    kb.row(but4)

    return kb


# Кнопки товаров для админ-панели
def admin_pr_buttons(products):
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    back = types.KeyboardButton('Назад⬅')
    all_products = [types.KeyboardButton(i[1]) for i in products]
    # Добавляем кнопки в пространство
    kb.add(*all_products)
    kb.row(back)

    return kb


def attr_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    name = types.InlineKeyboardButton(text='Название', callback_data='name')
    des = types.InlineKeyboardButton(text='Описание', callback_data='des')
    count = types.InlineKeyboardButton(text='Количество', callback_data='count')
    price = types.InlineKeyboardButton(text='Цена', callback_data='price')
    photo = types.InlineKeyboardButton(text='Фото', callback_data='photo')
    # Добавляем кнопки в пространство
    kb.add(name, des, count, price)
    kb.row(photo)

    return kb
