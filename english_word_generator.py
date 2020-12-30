from RealRPG import create_table, read_table, write_table
from datetime import datetime

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
            pass
        elif menu == 2:
            word_registration(today)
        else:
            break

if __name__ == "__main__":
    main()