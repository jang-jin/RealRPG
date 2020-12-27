from datetime import datetime, timedelta
import os
import csv
import numpy as np
import pandas as pd

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

SELECT_TODAY_QUEST_TYPE = ['언어', '체력', '알고리즘']

QUEST_TYPE = ['언어', '체력', '알고리즘', '지식']

def create_table():
    for table_name, table_path in TABLE_PATH.items():
        if not os.path.exists(table_path):
            with open(table_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
                pass

def read_table(table_name):
    with open(TABLE_PATH[table_name], 'r', encoding='utf-8-sig', newline='') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=TABLE_FIELD[table_name])
        table = pd.DataFrame(reader)
    return table

def write_table(table_name, values):
    with open(TABLE_PATH[table_name], 'a', encoding='utf-8-sig', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=TABLE_FIELD[table_name])
        writer.writerow(values)

def attendance(today):
    perform = read_table('perform')
    if perform.loc[(perform['date'] == today) & (perform['name'] == "출석")].empty:
        write_table('perform', {'date':today, 'name':"출석", 'fulfillment':True})
        write_table('coin', {'date':today, 'reason':"출석", 'number':1})
        print(today + " Attendance Completion!!")

def continuous_attendance(today):
    continuous_day = 0
    perform = read_table('perform')
    for date in perform.loc[perform['name'] == "출석", "date"][::-1]:
        if (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(date, "%Y-%m-%d")).days == continuous_day:
            continuous_day += 1
        else:
            break
    print(str(continuous_day) + " Days Continuous Attendance!!")

    if continuous_day % 10 == 0:
        coin = read_table('coin')
        if coin.loc[(coin['date'] == today) & (coin['reason'] == "연속출석")].empty:
            write_table('coin', {'date':today, 'reason':"연속출석", 'number':5})
            print("Continuous Attendance Completion is gotten 5 coins!!")

def show_daily_quest(today):
    print("***Daily Quest***")

    perform = read_table('perform')
    today_quest = perform.loc[(perform['date'] == today) & (perform['name'] != "출석")]
    if today_quest.empty:
        for today_quest_type in SELECT_TODAY_QUEST_TYPE:
            select_random_quest(today, today_quest_type)

    perform = read_table('perform')
    today_quest = perform.loc[(perform['date'] == today) & (perform['name'] != "출석")]
    for today_quest_name, today_quest_fulfillment in zip(today_quest['name'], today_quest['fulfillment']):
        print(" O " if today_quest_fulfillment == "True" else " X " + today_quest_name)
    print()

def select_random_quest(today, today_quest_type=None):
    quest = read_table('quest')
    if today_quest_type is None:
        quest = quest.loc[quest['activation'] == "True"]
    else:
        quest = quest.loc[(quest['type'] == today_quest_type) & (quest['activation'] == "True")]
    selected_quest = quest.iloc[np.random.randint(0, len(quest))]
    name = f"{int(np.around((np.random.rand() * 0.4 + 0.8) * int(selected_quest['number'])))} {selected_quest['name']}"
    write_table('perform', {'date':today, 'name':name, 'fulfillment':False})

def quest_completion():
    pass

def quest_management():
    menu = int(input("\t1.Quest Registration\n\t2.Quest Update\n\t3.Go to Lobby\n\t==>"))
    if menu == 1:
        quest_registration()
    elif menu == 2:
        pass
        # quest_update()

def quest_registration():
    quest_name = input("\t\tQuest Name\n\t\t==>")
    quest_number = int(input("\t\tQuest Number of times\n\t\t==>"))
    print("\t\tQuest Type\n\t\t", end="")
    for i, type_name in enumerate(QUEST_TYPE):
        print(f"{i+1}.{type_name}", end=" ")
    quest_type = QUEST_TYPE[int(input("\n\t\t==>"))-1]
    
    quest = {
        'name':quest_name,
        'number':quest_number,
        'type':quest_type,
        'activation':True
    }
    write_table('quest', quest)

# def quest_update():
#     print("\t\tSelect a Quest")
#     with open(TABLE_PATH['quest'], 'r', encoding='utf-8-sig', newline='') as csv_file:
#         reader = csv.DictReader(csv_file, fieldnames=TABLE_FIELD['quest'])
#         for row in reader:
#             print("\t\t{}")

def main():
    create_table()

    print("="*38)
    print("="*10+" WELCOME REAL RPG "+"="*10)
    print("="*38)

    today = datetime.today().strftime("%Y-%m-%d")
    attendance(today)
    continuous_attendance(today)
    print()

    while True:
        show_daily_quest(today)

        menu = int(input("1.Quest Completion\n2.Using Coins\n3.Add Random Quest\n4.Quest Management\n5.Logout\n==>"))
        if menu == 1:
            pass
        elif menu == 2:
            pass
        elif menu == 3:
            select_random_quest(today)
        elif menu == 4:
            quest_management()
        elif menu == 5:
            break

main()