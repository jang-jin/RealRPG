from datetime import datetime
import numpy as np
from table import *

def generate_problems():
    english_word = read_table('english_word')
    problems = []
    errors = []

    number = int(input("문제 개수 : "))
    while len(problems) < number:
        i = np.random.randint(0, len(english_word))
        if i not in problems:
            problems.append(i)
    for i in problems:
        answer = input(f"{english_word.loc[i, 'word']} : ")
        if answer != english_word.loc[i, 'meaning']:
            errors.append(i)
    print()
    print(f"틀린 개수 {len(errors)}/{number}")
    
    for i in errors:
        print(f"{english_word.loc[i, 'word']}\t{english_word.loc[i, 'meaning']}")
    print()

    if len(errors) <= number//10:
        return True
    else:
        return False

def word_registration(today):
    english_word = read_table('english_word')
    if english_word.empty:
        no = 0
    else:
        no = len(english_word.loc[english_word['date'] == today])
    while True:
        no += 1

        word = input("단어 : ")
        if word == "exit":
            break
        meaning = input("의미 : ")
        if meaning == "exit":
            break
        
        write_table('english_word', {'date':today, 'no':no,'word':word, 'meaning':meaning})

def main():
    create_table('english_word')

    print("="*38)
    print("="*2+" RealRPG - English Word Generator "+"="*2)
    print("="*38)
    print()

    today = datetime.today().strftime("%Y-%m-%d")

    while True:
        menu = int(input("1. Generate Problems\n2. Word Registration\n3. Go to Lobby\n==>"))
        if menu == 1:
            generate_problems()
        elif menu == 2:
            word_registration(today)
        else:
            break

if __name__ == "__main__":
    main()