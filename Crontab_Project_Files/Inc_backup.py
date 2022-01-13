from dotenv import load_dotenv
import os
from datetime import date,datetime
load_dotenv()

def last_backup():
    folder=os.listdir(os.getenv("BASE_PATH"))

    times = []
    for i in folder:
        file = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        times.append(file)

    maxx=max(times)
    for i in folder:
        file = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        if file == maxx:
            last_full_backup=i
            break
    return last_full_backup

def Inc_backup():
    if datetime.now().hour == 8:
        pass
    else:
        last_full_backup=last_backup()
        os.system("innobackupex --incremental --user={} --password={} {}/{} --incremental-basedir={}/{}"
        .format(os.getenv("USER_"),os.getenv("PASS_"),os.getenv("INC_PATH"),last_full_backup,os.getenv("BASE_PATH"),last_full_backup))

Inc_backup()