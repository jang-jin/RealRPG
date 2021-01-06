import os
import csv
import pandas as pd

TABLE_PATH = {
    'quest' : os.getcwd() + "/quest.csv", 
    'perform' : os.getcwd() + "/perform.csv", 
    'coin' : os.getcwd() + "/coin.csv",
    'english_word' : os.getcwd() + "/english_word.csv",
    'reward' : os.getcwd() + "/reward.csv",
}
TABLE_FIELD = {
    'quest' : ['name', 'number', 'type', 'activation'], 
    'perform' : ['date', 'name', 'fulfillment'], 
    'coin' : ['date', 'reason', 'number'],
    'english_word' : ['date', 'no', 'word', 'meaning'],
    'reward' : ['date', 'name', 'number'],
}

def create_table(table_name, init=False):
    table_path = TABLE_PATH[table_name]
    if not os.path.exists(table_path) or init:
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