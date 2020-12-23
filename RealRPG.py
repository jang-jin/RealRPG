from datetime import datetime
import os
import csv

TABLE_PATH = {
    'quest' : os.getcwd() + "/quest.csv", 
    'perform' : os.getcwd() + "/perform.csv", 
    'coin' : os.getcwd() + "/coin.csv"
}
TABLE_FIELD = {
    'quest' : ['name', 'number', 'type', 'activation'], 
    'perform' : ['date', 'name', 'fulfillment'], 
    'coin' : ['date', 'reason', 'number']
}

def create_table():
    for table_name, table_path in TABLE_PATH.items():
        if not os.path.exists(table_path):
            with open(table_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
                pass

def attendance(today):
    attendance_check = False

    with open(TABLE_PATH['perform'], 'r', encoding='utf-8-sig', newline='') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=TABLE_FIELD['perform'])
        for row in reader:
            if row['date'] == today and row['name'] == "출석":
                attendance_check = True
                break
    
    if attendance_check is False:
        with open(TABLE_PATH['perform'], 'a', encoding='utf-8-sig', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=TABLE_FIELD['perform'])
            writer.writerow({'date':today, 'name':"출석", 'fulfillment':True})
        with open(TABLE_PATH['coin'], 'a', encoding='utf-8-sig', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=TABLE_FIELD['coin'])
            writer.writerow({'date':today, 'reason':"출석", 'number':1})
        print(today + " Attendance Completion!!")

def quest_registration():
    name = input("\t\t퀘스트 명 : ")
    reward = int(input("\t\t보상 : "))
    quest = {
        'name':name,
        'reward':reward
    }
    path = os.getcwd() + "/quest.csv"
    with open(path, 'a', encoding='utf-8', newline='') as csv_file:
        wr = csv.DictWriter(csv_file, fieldnames=['name','reward'])
        wr.writerow(quest)

def quest_management():
    menu = int(input("\t1.퀘스트 등록\n\t2.퀘스트 삭제\n\t3.나가기\n\t"))
    if menu == 1:
        quest_registration()
    elif menu == 2:
        pass

def main():
    create_table()

    print("="*38)
    print("="*10+" WELCOME REAL RPG "+"="*10)
    print("="*38)

    today = datetime.today().strftime("%Y-%m-%d")
    attendance(today)

    # print(today)
    # print("일일퀘스트")
    # menu = int(input("1.퀘스트 완료\n2.퀘스트 등록/삭제\n"))
    # if menu == 1:
    #     pass
    # elif menu == 2:
    #     quest_management()
    #     main()

main()