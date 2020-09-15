import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        spent_today = sum(record.amount for record in self.records
                          if record.date == today)

        return spent_today

    def get_week_stats(self):
        today = dt.date.today()
        this_week = today - dt.timedelta(days=7)
        week_stats = sum(record.amount for record in self.records
                         if this_week < record.date <= today)

        return week_stats


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = self.calc_date(date)

    def calc_date(self, date):
        if not date:
            return dt.date.today()
        return dt.datetime.strptime(date, "%d.%m.%Y").date()


class CaloriesCalculator(Calculator):
    OVER_LIMIT_CAL = "Хватит есть!"
    BELOW_LIMIT_CAL = ("Сегодня можно съесть что-нибудь ещё, "
                       "но с общей калорийностью не более {calories} кКал")

    def get_calories_remained(self):
        calories_left = self.limit - self.get_today_stats()

        if 0 < calories_left <= self.limit:
            return self.BELOW_LIMIT_CAL.format(calories=calories_left)
        else:
            return self.OVER_LIMIT_CAL


class CashCalculator(Calculator):
    USD_RATE = 75.00
    EURO_RATE = 89.00
    RUB_RATE = 1.00

    POSITIVE_RESP = "На сегодня осталось {balance} {cur_name}"
    NEGATIVE_RESP = "Денег нет, держись: твой долг - {balance} {cur_name}"
    ZERO_RESP = "Денег нет, держись"

    @property
    def currencies(self):

        return {
                "rub": {"name": "руб", "rate": self.RUB_RATE},
                "usd": {"name": "USD", "rate": self.USD_RATE},
                "eur": {"name": "Euro", "rate": self.EURO_RATE}
             }

    def get_today_cash_remained(self, currency):

        balance_left = self.limit - self.get_today_stats()
        balance_converted = round(abs(balance_left /
                                      self.currencies[currency]["rate"]), 2)

        if balance_left == 0:
            return self.ZERO_RESP

        if 0 < balance_left:
            return \
                self.POSITIVE_RESP.format(balance=balance_converted,
                                          cur_name=self.currencies[currency]
                                          ["name"])

        return \
            self.NEGATIVE_RESP.format(balance=balance_converted,
                                      cur_name=self.currencies[currency]
                                      ["name"])


if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    calories_calculator = CaloriesCalculator(3000)

    calories_calculator.add_record(Record(amount=200,
                                          comment="завтрак"))
    calories_calculator.add_record(Record(amount=300,
                                          comment="обед"))
    calories_calculator.add_record(Record(amount=400,
                                          comment="ужин",
                                          date="08.11.2019"))

    cash_calculator.add_record(Record(amount=14522.122,
                                      comment="проезд"))
    cash_calculator.add_record(Record(amount=300,
                                      comment="обед"))
    cash_calculator.add_record(Record(amount=303,
                                      comment="цветы",
                                      date="03.09.2020"))

    print(cash_calculator.get_today_cash_remained("rub"))
    print(calories_calculator.get_calories_remained())
    print(cash_calculator.get_week_stats())
