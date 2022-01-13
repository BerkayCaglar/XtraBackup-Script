from dotenv import load_dotenv
import os
load_dotenv()

def old_backup():
    folder=os.listdir(os.getenv("BASE_PATH"))

    times = []
    for i in folder:
        file = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        times.append(file)

    minn=min(times)
    for i in folder:
        file = os.path.getmtime("{}/{}".format(os.getenv("BASE_PATH"),i))
        if file == minn:
            old_backupp=i
            break
    return old_backupp

def full_backup():
    os.system("innobackupex --user={} --password={} {}".format(os.getenv("USER_"),os.getenv("PASS_"),os.getenv("BASE_PATH")))

    folder=os.listdir(os.getenv("BASE_PATH"))

    if 3<len(folder):
            old_=old_backup()
            os.system("rm -rf {}/{}".format(os.getenv("BASE_PATH"),old_))
            os.system("rm -rf {}/{}".format(os.getenv("INC_PATH"),old_))

full_backup()