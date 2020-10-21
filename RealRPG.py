import os
import csv

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
    # create_table() 만들기
    print("="*10+" WELCOME REAL RPG "+"="*10)
    print("일일퀘스트")
    menu = int(input("1.퀘스트 완료\n2.퀘스트 등록/삭제\n"))
    if menu == 1:
        pass
    elif menu == 2:
        quest_management()
        main()

main()