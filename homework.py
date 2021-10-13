import datetime as dt
format = '%d.%m.%Y'


class Record:
    def __init__(self, amount, date=None, comment="Не регламентировано"):
        if amount < 0:
            amount = abs(amount)
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.today().date()
        stat = sum(record.amount for record in self.records if
                   record.date == today)
        return stat

    def get_week_stats(self):
        now_date = dt.date.today()
        sum = 0
        time_delta = now_date - dt.timedelta(days=7)
        for record in self.records:
            if time_delta < record.date <= now_date:
                sum += record.amount
        return sum


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_day = self.limit - self.get_today_stats()
        if calories_day > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.limit - self.get_today_stats()} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 70.00
    USD_RATE = 60.00
    RUB_RATE = 1.00
    CURRENCIES = {
        'rub': ('руб', RUB_RATE),
        'eur': ('Euro', EURO_RATE),
        'usd': ('USD', USD_RATE)
    }

    def get_today_cash_remained(self, currency):
        cash_day = self.limit - self.get_today_stats()
        cash = cash_day / self.CURRENCIES[currency][1]
        if cash_day > 0:
            return (f'На сегодня осталось {(cash):.2f} '
                    f'{self.CURRENCIES[currency][0]}')
        if cash_day == 0:
            return 'Денег нет, держись'
        else:
            return (f'Денег нет, держись: твой долг - {abs(cash):.2f} '
                    f'{self.CURRENCIES[currency][0]}')


cash_calculator = CashCalculator(300)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))

r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
r2 = Record(amount=1568,
            comment='Наполнение потребительской корзины',
            date='09.03.2019')
r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

# для CaloriesCalculator
calor = CaloriesCalculator(300)
r4 = Record(amount=1186,
            comment='Кусок тортика. И ещё один.')
r5 = Record(amount=84, comment='Йогурт.')
r6 = Record(amount=1140, comment='Баночка чипсов.')

print(calor.get_calories_remained())