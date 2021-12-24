import os
import time

class system_():
    def __init__(self,username,password,base_path,incremental_path):
        self.username = username
        self.password = password

        self.base_path = base_path
        self.incremental_path = incremental_path

user_1= system_("root","qm4d2rFDKpaVn4yP","/root/test_backups/Base","/root/test_backups/Incremental")


def select():
    while (True):
        print("\n-------Please select an operation-------\n")

        print("1- Full Backup 2- Incremental Backup 3- Copy Back 4- Quit")
        try:
            selected=int(input("--->"))
            break
        except:
            print("\n-----Incorrect Entry-----")
            time.sleep(1)
    
    if selected==1:
        text = "innobackupex --user={} --password={} {}".format(user_1.username,user_1.password,user_1.base_path)
        os.system(text)

        print("\n\n-----COMPLETED !-----")
        time.sleep(1)

        klasor=os.listdir(user_1.base_path)

        
        if 3<len(klasor):
            old_=old_backup()
            os.system("rm -rf {}/{}".format(user_1.base_path,old_))

    elif selected==2:
        klasor=os.listdir(user_1.base_path)
        if not klasor:
            print("\n------First you need to full backup------")
            time.sleep(1)
        else:
            last_full_backup=last_backup()
            os.system("innobackupex --incremental --user={} --password={} {}/{} --incremental-basedir={}/{}"
            .format(user_1.username,user_1.password,user_1.incremental_path,last_full_backup,user_1.base_path,last_full_backup))

            print("\n\n-----COMPLETED !-----")

    elif selected==3:
        while(True):
            try:
                print("Are you sure? [y/n]")
                yes_no = str(input("--->"))
                yes_no=yes_no.upper()
            except:
                print("\n-----Incorrect Entry-----")
                time.sleep(1)
            if yes_no=="Y":
                klasor=os.listdir(user_1.base_path)
                if not klasor:
                    print("\n------First you need to full backup------")
                    time.sleep(1)
                else:
                    last_full_backup=last_backup()
                    copy_back(last_full_backup)
                    break

            elif yes_no == "N":
                break
            else:
                print("ERROR!")
                break

    elif selected==4:
        quit()

def last_backup():
    klasor=os.listdir(user_1.base_path)

    times = []
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(user_1.base_path,i))
        times.append(dosya)

    maxx=max(times)
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(user_1.base_path,i))
        if dosya == maxx:
            last_full_backup=i
            break
    return last_full_backup

def old_backup():
    klasor=os.listdir(user_1.base_path)

    times = []
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(user_1.base_path,i))
        times.append(dosya)

    minn=min(times)
    for i in klasor:
        dosya = os.path.getmtime("{}/{}".format(user_1.base_path,i))
        if dosya == minn:
            old_backupp=i
            break
    return old_backupp

def copy_back(last_full_backup):

    os.system("systemctl stop mysql@bootstrap")
    print("MySQL Stopped !")
    time.sleep(1)

    os.system("rm -rf /var/lib/mysql/*")
    print("\n/var/lib/mysql/* Deleted !")
    time.sleep(3)

    os.system("innobackupex --apply-log --redo-only {}/{}".format(user_1.base_path,last_full_backup))

    incrementals=os.listdir(user_1.incremental_path+"/"+last_full_backup)
    
    y=0
    for i in incrementals:
        if y==len(incrementals)-1:
            os.system("innobackupex --apply-log {}/{} --incremental-dir={}/{}/{}"
            .format(user_1.base_path,last_full_backup,user_1.incremental_path,last_full_backup,i))

            os.system("innobackupex --apply-log {}/{}".format(user_1.base_path,last_full_backup))
        else:
            os.system("innobackupex --apply-log --redo-only {}/{} --incremental-dir={}/{}/{}"
            .format(user_1.base_path,last_full_backup,user_1.incremental_path,last_full_backup,i))
            y=y+1
    
    os.system("innobackupex --copy-back {}/{}".format(user_1.base_path,last_full_backup))

    os.system("chown -cR mysql:mysql /var/lib/mysql")

    os.system("systemctl start mysql@bootstrap")


def main():
    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    while(True):
        select()

main()