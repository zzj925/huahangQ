import schedule
from datetime import datetime, timedelta, time
def job():
    print('working...')
schedule.every().second.until('23:59').do(job)  # 今天23:59停止
schedule.every().second.until('2030-01-01 18:30').do(job)  # 2030-01-01 18:30停止
schedule.every().second.until(timedelta(hours=8)).do(job)  # 8小时后停止
schedule.every().second.until(time(23, 59, 59)).do(job)  # 今天23:59:59停止
schedule.every().second.until(datetime(2030, 1, 1, 18, 30, 0)).do(job)  # 2030-01-01 18:30停止
schedule.every(10).minutes.do(job)  ##10分钟执行一次
schedule.every().day.at("10:30").do(job)  ##每天十点半执行任务
while True:
    schedule.run_pending()

