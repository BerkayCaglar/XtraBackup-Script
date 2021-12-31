from dotenv import load_dotenv
import os
import time
from datetime import date, datetime
import schedule
import json
load_dotenv()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def old_backup():
    klasor=os.listdir(os.getenv("BASE_PATH"))

    times = []
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        times.append(dosya)

    minn=min(times)
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        if dosya == minn:
            old_backupp=i
            break
    return old_backupp

def last_backup():
    klasor=os.listdir(os.getenv("BASE_PATH"))

    times = []
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        times.append(dosya)

    maxx=max(times)
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        if dosya == maxx:
            last_full_backup=i
            break
    return last_full_backup

def copy_back(last_full_backup):
    
    os.system("systemctl stop mysql@bootstrap")

    os.system("rm -rf /var/lib/mysql/*")

    os.system("innobackupex --apply-log --redo-only {}/{}".format(os.getenv("BASE_PATH"),last_full_backup))

    incrementals=os.listdir(os.getenv("INC_PATH")+"/"+last_full_backup)
    
    y=0
    for i in incrementals:
        if y==len(incrementals)-1:
            os.system("innobackupex --apply-log {}/{} --incremental-dir={}/{}/{}"
            .format(os.getenv("BASE_PATH"),last_full_backup,os.getenv("INC_PATH"),last_full_backup,i))

            os.system("innobackupex --apply-log {}/{}".format(os.getenv("BASE_PATH"),last_full_backup))
        else:
            os.system("innobackupex --apply-log --redo-only {}/{} --incremental-dir={}/{}/{}"
            .format(os.getenv("BASE_PATH"),last_full_backup,os.getenv("INC_PATH"),last_full_backup,i))
            y=y+1
    
    os.system("innobackupex --copy-back {}/{}".format(os.getenv("BASE_PATH"),last_full_backup))

    os.system("chown -cR mysql:mysql /var/lib/mysql")

    os.system("systemctl start mysql@bootstrap")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def full_backup():
    os.system("innobackupex --user={} --password={} {}".format(os.getenv("USER_"),os.getenv("PASS_"),os.getenv("BASE_PATH")))

    klasor=os.listdir(os.getenv("BASE_PATH"))

    if 3<len(klasor):
            old_=old_backup()
            os.system("rm -rf {}/{}".format(os.getenv("BASE_PATH"),old_))

def Inc_backup():
    last_full_backup=last_backup()
    os.system("innobackupex --incremental --user={} --password={} {}/{} --incremental-basedir={}/{}"
    .format(os.getenv("USER_"),os.getenv("PASS_"),os.getenv("INC_PATH"),last_full_backup,os.getenv("BASE_PATH"),last_full_backup))

def restore_Backup():
    last_full_backup=last_backup()
    copy_back(last_full_backup)
    pass

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    schedule.every().day.at(os.getenv("FULL_BACKUP_TIME")).do(full_backup)

    for i in range(0,len(json.loads(os.environ['INC_BACKUP_TIME']))):
        schedule.every().day.at(json.loads(os.environ['INC_BACKUP_TIME'])[i]).do(Inc_backup)

    schedule.every().day.at(os.getenv("RESTORE_FULL_BACKUP_TIME")).do(restore_Backup)

    check=True
    while check:
        if datetime.now().second == 0:
            check = False
            while True:
                schedule.run_pending()
                print(schedule.get_jobs())
                time.sleep(60-datetime.now().second)
                
        else:
            time.sleep(0.1)

main()