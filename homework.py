import datetime as dt


format = '%d.%m.%Y'


class Record:
    def __init__(self, amount, date=None, comment="Не регламентировано"):
        if amount < 0:
            amount = abs(amount)
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
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

    def get_calc(self):
        calc = self.limit - self.get_today_stats()
        return calc


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_day = self.get_calc()
        if calories_day > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{calories_day} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 70.00
    USD_RATE = 60.00
    RUB_RATE = 1.00
    CURRENCIES = {
        'rub': ('руб', RUB_RATE),
        'eur': ('Euro', EURO_RATE),
        'usd': ('USD', USD_RATE)}

    def get_today_cash_remained(self, currency):

        currenciess = {
            'rub': ('руб', self.RUB_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE)}

        cash_day = self.get_calc()
        if cash_day == 0:
            return 'Денег нет, держись'
        cash = cash_day / self.CURRENCIES[currency][1]
        abs_cash = abs(cash)
        currency_cash, cur_cash = currenciess.get(currency)
        if cash_day > 0:
            return (f'На сегодня осталось {cash:.2f} {currency_cash}')
        return (f'Денег нет, держись: твой долг - {abs_cash:.2f} '
                f'{currency_cash}')
