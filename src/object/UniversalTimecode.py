class UniversalTimecode():
    def __init__(self, date: str = "", universal: int = 0):
        if date != "":
            self.raw_date = date
            
            splitted_date = date.split(" ")[0].split("/")
            splitted_time = date.split(" ")[1].split(":")
            
            self.year = int(splitted_date[0]) - 1970
            self.month = int(splitted_date[1])
            self.day = int(splitted_date[2])
            self.hour = int(splitted_time[0])
            self.minute = int(splitted_time[1])
            self.second = int(splitted_time[2])
            
            self.value = self.year * 31536000 + self.month * 2628000 + self.day * 86400 + self.hour * 3600 + self.minute * 60 + self.second
        else:
            self.value = universal
            
            self.year = int(universal / 31536000)
            universal -= self.year * 31536000
            self.month = int(universal / 2628000)
            universal -= self.month * 2628000
            self.day = int(universal / 86400)
            universal -= self.day * 86400
            self.hour = int(universal / 3600)
            universal -= self.hour * 3600
            self.minute = int(universal / 60)
            universal -= self.minute * 60
            self.second = universal
            
            self.raw_date = f"{self.year}/{self.month}/{self.day} {self.hour}:{self.minute}:{self.second}"

    def __eq__(self, timecode):
        if timecode == None: return False
        else: return self.value == timecode.value

    def __repr__(self):
        return f"{self.raw_date} [{self.value}]"

    def __sub__(self, timecode):
        return UniversalTimecode(universal = (self.value - timecode.value))
    
    def get_detailed_date(self):
        return f"{self.year} YEAR(S) {self.month} MONTH(S) {self.day} DAY(S)\n{self.hour}H {self.minute}MIN {self.second}S"
    
    @staticmethod
    def now():
        from datetime import datetime
        NOW = datetime.now()
        return UniversalTimecode(date=f"{NOW.year}/{NOW.month}/{NOW.day} {NOW.hour}:{NOW.minute}:{NOW.second}")
