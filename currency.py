from datetime import datetime
import bisect


class Currency:
    def __init__(self, name: str, rate: float, time: datetime):
        self.name = name
        self.dates = [time, ]
        self.rates = [rate, ]

    def add_rate(self, rate: float, time: datetime):
        index = bisect.bisect_left(self.dates, time)
        self.dates.insert(index, time)
        self.rates.insert(index, rate)

    def get_rate(self, time: datetime):
        print('________GET RATE____________')
        print('time', time)
        print(self.dates)
        index = bisect.bisect_left(self.dates, time)
        print('index', index)
        print('self.rates', self.rates)
        print('self.rates[index-1]', self.rates[index-1])
        if index < len(self.dates):
            if self.dates[index] == time:
                return self.rates[index]
        return self.rates[index-1]

    def get_date(self, rate):
        index = self.rates.index(rate)
        return self.dates[index]



