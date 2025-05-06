import pytz
import schedule
import time
from datetime import datetime
import parser

moscow_tz = pytz.timezone("Europe/Moscow")


def job():
    print("Задача выполнена в московское время:", datetime.now(moscow_tz).strftime("%Y-%m-%d %H:%M:%S"))
    parser.parsing_steam()


def time_detect():
    now = datetime.now(moscow_tz)
    if now.hour == 19 and now.minute == 15:
        job()


schedule.every(1).minutes.do(time_detect)

while True:
    schedule.run_pending()
    time.sleep(10)
