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


def con_db() -> None:
    '''連線到資料庫'''
    global conn
    conn = sqlite3.connect(DB)
    global cursor
    cursor = conn.cursor()


def end_con_db() -> None:
    '''停止連線'''
    # 變更記錄到DB隨然創建表格不需要，但我懶得重寫
    conn.commit()
    # 關閉連線
    cursor.close()
    conn.close()


def create_dbandtable():
    '''建立資料庫與資料表，並顯示結果'''
    # 連線到資料庫
    con_db()
    cmd = '''
        CREATE TABLE if not exists members(iid INTEGER AUTO_INCREMENT, mname
        TEXT NOT NULL, msex TEXT NOT NULL, mphone TEXT NOT NULL)
    '''
    # 確認資料表與資料庫是否正確建立
    try:
        cursor.execute(cmd)
        message = '=>資料庫已建立'
    except sqlite3.Error as e:
        message = e
    # 結束連線以免資料庫被鎖定
    end_con_db()
    # 回傳資訊
    print(message)


def import_data(dname: str) -> None:
    '''從members.txt匯入資料並顯示異動資料數'''
    # 讀取檔案
    data = [line.strip() for line in open(dname, 'r', encoding='UTF-8')]
    # 紀錄資料數量
    index = len(data)
    # 連結資料庫
    con_db()
    # 切割資料並插入資料庫
    for i in range(index):
        try:
            insert_value = i.split(',')
            format_value = (insert_value[0], insert_value[1], insert_value[2])
            cursor.execute('INSERT INTO members VALUES (?, ?, ?)', format_value)

        except sqlite3.Error as e:
            print(e)

    print(f'=>異動 {index} 筆記錄')
    # 結束資料庫連線
    end_con_db()


# 預設資料庫變數
DB = 'wanghong.db'
