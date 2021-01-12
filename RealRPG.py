from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from table import *
from english_word_generator import generate_problems

SELECT_TODAY_QUEST_TYPE = ['언어', '체력', '코딩', '지식']

QUEST_TYPE = ['언어', '체력', '코딩', '지식']

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
    print(f"***{today} Daily Quest***")

    perform = read_table('perform')
    today_quest = perform.loc[(perform['date'] == today) & (perform['name'] != "출석")]
    if today_quest.empty:
        for today_quest_type in SELECT_TODAY_QUEST_TYPE:
            select_random_quest(today, today_quest_type)

    perform = read_table('perform')
    today_quest = perform.loc[(perform['date'] == today) & (perform['name'] != "출석")]
    for today_quest_name, today_quest_fulfillment in zip(today_quest['name'], today_quest['fulfillment']):
        print((" O " if today_quest_fulfillment == "True" else " X ") + today_quest_name)
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

def quest_completion(today):
    perform = read_table('perform')
    today_quest = perform.loc[(perform['date'] == today) & (perform['name'] != "출석") & (perform['fulfillment'] == "False")]
    
    if today_quest.empty:
        print()
        print("Today's quest all completed~")
        print()
    else:
        print("\tSelect the completed quest!")
        print()
        for i, today_quest_name in enumerate(today_quest['name']):
            print(f"\t{i+1}. {today_quest_name}")
        selected_quest = today_quest.iloc[int(input("\t==>"))-1, 1]
        fulfillment = True
        
        if selected_quest.split(" ")[1] == "영어단어외우기":
            fulfillment = generate_problems()

        perform.loc[(perform['date'] == today) & (perform['name'] == selected_quest), 'fulfillment'] = fulfillment
        print()

        create_table('perform', init=True)
        for i in range(len(perform)):
            write_table('perform', dict(perform.iloc[i]))

        if fulfillment:
            write_table('coin', {'date':today, 'reason':"랜덤퀘스트 완료", 'number':1})
            coin = read_table('coin')
            today_coin = coin.loc[(coin['date'] == today) & (coin['reason'] == "랜덤퀘스트 완료")]
            if len(today_coin) == 4:
                write_table('coin', {'date':today, 'reason':"일일퀘스트 모두완료", 'number':2})
                print("Today's Quest Completion is gotten 2 coins!!")
                print()

def quest_registration():
    quest_name = input("\tQuest Name\n\t==>")
    quest_number = int(input("\tQuest Number of times\n\t==>"))
    print("\tQuest Type\n\t", end="")
    for i, type_name in enumerate(QUEST_TYPE):
        print(f"{i+1}.{type_name}", end=" ")
    quest_type = QUEST_TYPE[int(input("\n\t==>"))-1]
    
    quest = {
        'name':quest_name,
        'number':quest_number,
        'type':quest_type,
        'activation':True
    }
    write_table('quest', quest)

def gambling(today):
    coin = read_table('coin')
    print(f"\tYou have {coin['number'].astype('int').sum()} coins")
    print()
    menu = int(input("\t1. A single draw\n\t2. Ten times draws\n\t3. Go to Lobby\n\t==>"))
    if menu == 1:
        a_single_draw(today)
    elif menu == 2:
        ten_times_draws(today)

def a_single_draw(today):
    write_table('coin', {'date':today, 'reason':"단챠", 'number':-1})

    bins = [0,0.1,0.8,1]
    labels = ["꽝 0", "유튜브시청 1", "유튜브시청 2"]
    name, number = pd.cut([np.random.rand()], bins, labels=labels)[0].split()

    write_table('reward', {'date':today, 'name':name, 'number':number})

    if number == "2":
        print(f"축! {name} {number}개 획득!!!")
    elif number == "1":
        print(f"{name} {number}개 획득")
    elif number == "0":
        print("꽝ㅠ")
    print()

def ten_times_draws(today):
    write_table('coin', {'date':today, 'reason':"10연챠", 'number':-10})

    write_table('reward', {'date':today, 'name':"유튜브시청", 'number':2})
    print("축! 유튜브시청 2개 획득!!!")
    for i in range(9):
        bins = [0,0.1,0.8,1]
        labels = ["꽝 0", "유튜브시청 1", "유튜브시청 2"]
        name, number = pd.cut([np.random.rand()], bins, labels=labels)[0].split()

        write_table('reward', {'date':today, 'name':name, 'number':number})

        if number == "2":
            print(f"축! {name} {number}개 획득!!!")
        elif number == "1":
            print(f"{name} {number}개 획득")
        elif number == "0":
            print("꽝ㅠ")
    print()

def using_rewards(today):
    reward = read_table('reward')
    reward_list = list(reward['name'].unique())
    reward_list.remove("꽝")
    
    print("\tSelect a reward to use!")
    print()
    for i, reward_name in enumerate(reward_list):
        print(f"\t{i+1}. {reward_name} {reward.loc[reward['name'] == reward_name, 'number'].astype('int').sum()}")
    print()

    write_table('reward', {'date':today, 'name':reward_list[int(input("\t==>"))-1], 'number':-1})
    print("Done Using!!")
    print()

def show_results():
    perform = read_table('perform')
    fulfillment = perform.loc[perform['name'] != "출석",'fulfillment']
    print(f"\tQuest Success Rate : {fulfillment.value_counts()['True']} / {fulfillment.count()} ( {fulfillment.value_counts(1)['True']*100:.2f} % )")
    print()

    quest = read_table('quest')[['name', 'type']]
    perform.loc[perform['name'] != "출석",'number'] = perform.loc[perform['name'] != "출석",'name'].str.split(" ").str[0]
    perform.loc[perform['name'] != "출석",'name'] = perform.loc[perform['name'] != "출석",'name'].str.split(" ").str[1]
    perform_quest = pd.merge(perform, quest, how='left')
    fulfillment_by_type = perform_quest.groupby('type')['fulfillment'].value_counts()

    for type_name in QUEST_TYPE:
        print(f"{type_name} : {fulfillment_by_type.loc[(type_name, 'True')]} / {fulfillment_by_type.loc[type_name].sum()} ( {1} % )")
    print(fulfillment_by_type.loc["언어"].sum())


def main():
    for table_name in TABLE_PATH.keys():
        create_table(table_name)
    print("=================================================================")
    print("=====================    WELCOME REAL RPG   =====================")
    print("=================================================================")

    today = datetime.today().strftime("%Y-%m-%d")
    attendance(today)
    continuous_attendance(today)
    print()

    while True:
        show_daily_quest(today)
        print("          7          |          8          |          9          ")
        print("     Show results    |                     |                     ")
        print("-----------------------------------------------------------------")
        print("          4          |          5          |          6          ")
        print("       Gambling      |    Using Rewards    |                     ")
        print("-----------------------------------------------------------------")
        print("          1          |          2          |          3          ")
        print("   Quest Completion  |   Add Random Quest  |  Quest Registration ")
        print("-----------------------------------------------------------------")
        print("                     |          0          |                     ")
        print("                     |        Logout       |                     ")
        menu = int(input("==>"))
        if menu == 0:
            break
        elif menu == 1:
            quest_completion(today)
        elif menu == 2:
            select_random_quest(today)
            print()
        elif menu == 3:
            quest_registration()
        elif menu == 4:
            gambling(today)
        elif menu == 5:
            using_rewards(today)
        elif menu == 7:
            show_results()

if __name__ == "__main__":
    # main()
    show_results()
    