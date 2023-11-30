import json
import sqlite3


def get_json(dname: str) -> dict:
    '''取的資料並轉成Python字典'''
    with open(dname, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data


def show_list() -> None:
    '''顯示選擇表單'''
    print('-' * 10, ' 選單 ', '-' * 10)
    print('0 / Enter 離開')
    print('1 建立資料庫與資料表')
    print('2 匯入資料')
    print('3 顯示所有紀錄')
    print('4 新增記錄')
    print('5 修改記錄')
    print('6 查詢指定手機')
    print('7 刪除所有記錄')
    print('-' * 26)


# 預設連結的資料庫
DB = 'wanghong.db'
conn = sqlite3.connect(DB)
cursor = conn.cursor()
