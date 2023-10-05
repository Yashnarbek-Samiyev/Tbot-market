# импортируем ответ пользователю
from settings.message import MESSAGES
from settings import config
# импортируем класс-родитель
from handlers.handler import Handler


class HandlerAllText(Handler):
    """
    Класс обрабатывает события нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точне
        это выбор категории товаров
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_info(self, message):
        """
        Обработка события нажатия на кнопку 'О магазине'
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        Обработка события нажатия на кнопку 'Настройки'
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        """
        Обработка события нажатия на кнопку 'Назад'
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_product(self, message, product):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точне
        это выбор товара из категории
        """
        self.bot.send_message(message.chat.id, 'Категория ' +
                              config.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_category(
                                  config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Заказ'.
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id,MESSAGES['order_number'].format(
            self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(
                                  product_id),
                                     self.BD.select_single_product_title(
                                         product_id),
                                     self.BD.select_single_product_price(
                                         product_id),
                                     self.BD.select_order_quantity(
                                         product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(
                                  self.step, quantity))

    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # ********** меню ********** #

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.
                                          category_menu())

            # ********** меню (категории товара, ПФ, Бакалея, Мороженое)******
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')