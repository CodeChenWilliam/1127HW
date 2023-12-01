import json
import sqlite3

# 預設資料庫變數
DB = 'wanghong.db'

def get_json(dname: str) -> dict:
    '''取的資料並轉成Python字典'''
    with open(dname, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data


def show_list() -> None:
    '''顯示選擇表單'''
    print()
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
    # 變更記錄到DB雖然創建表格不需要，但我懶得重寫
    conn.commit()
    # 關閉連線以免資料庫被鎖定
    cursor.close()
    conn.close()


def create_dbandtable():
    '''建立資料庫與資料表，並顯示結果'''
    # 連線到資料庫
    con_db()
    cmd = 'CREATE TABLE if not exists members(iid INTEGER PRIMARY \
        KEY AUTOINCREMENT, mname TEXT NOT NULL, msex TEXT NOT NULL,\
        mphone TEXT UNQIUE)'
    # 確認資料表與資料庫是否正確建立
    try:
        cursor.execute(cmd)
        message = '=>資料庫已建立'
    except sqlite3.Error as e:
        message = e
    # 結束資料庫連線
    end_con_db()
    # 回傳資訊
    print(message)


def import_data(dname: str) -> None:
    '''從members.txt匯入資料並顯示異動資料數'''
    # 讀取檔案
    data = [line.strip() for line in open(dname, 'r', encoding='UTF-8')]
    # 紀錄資料數量
    index = len(data)
    # 用於Try Catch 變數
    hasError = False
    # 連線到資料庫
    con_db()
    # 切割資料並插入資料庫
    for i in data:
        try:
            insert_value = i.split(',')
            format_value = (insert_value[0], insert_value[1], insert_value[2])
            cursor.execute('INSERT INTO members (mname, msex, mphone)\
                            VALUES (?, ?, ?)', format_value)
        except sqlite3.Error as e:
            print(f'Error Message: {e}')
            hasError = True
    if not hasError:
        print(f'=>異動 {index} 筆記錄')
    # 結束資料庫連線
    end_con_db()
def show_data(tname: str) -> None:
    ''' tname = Tables name
        顯示所有紀錄(資料表內容)'''
    # 連線到資料庫
    con_db()
    # 查詢資料表是否有資料
    has_data = False
    try:
        cmd = f'SELECT * FROM {tname}'
        cursor.execute(cmd)
        result_all = cursor.fetchall()
        if result_all != ():
            has_data = True
        # 表格標題
        print()
        print('姓名　　　　性別　手機')
        print('-'*30)
        for row in result_all:
            # 切割資料
            name = row[1]
            name_len = len(name)
            sex = row[2]
            phone = row[3]
            print(f'{name:\u3000<7}{sex:<5}{phone}')
    except sqlite3.Error as e:
        print(e)
    # 如果沒有資料
    if not has_data:
        print('=>查無資料')
    # 結束資料庫連線
    end_con_db()

def add_data(tname:str) -> None:
    ''' tname : Table name
        增加一行資料到tname資料表中
        因為是寫死的沒有其他判斷條件
    '''
    # 連線到資料庫
    con_db()
    # 取得輸入資料
    has_Error = False
    name = input('請輸入姓名: ')
    sex = input('請輸入性別: ')
    phone = input('請輸入手機: ')
    if name == '':
        print('名字不可為空值')
        has_Error = True
    elif sex == '':
        print('性別不可為空值')
        has_Error = True
    elif phone == '':
        print('電話號碼不可為空值')
        has_Error = True
    # 寫入資料表
    data = (name, sex, phone)
    try:
        cursor.execute('INSERT INTO members (mname, msex, mphone) \
            VALUES (?, ?, ?)', data)
    except sqlite3.Error as e:
        print(e)
        has_Error = True
    # 輸出異動成功
    if not has_Error:
        print('=>異動 1 筆記錄')
    # 結束資料庫連線
    end_con_db()


def updata(tname: str) -> None:
    ''' tname: Tables Name
        修改tname的資料
        性別與手機都要修改
    '''
    # 連線到資料庫
    con_db()
    # 修改資料
    has_Error = False
    name = input('請輸入想修改記錄的姓名: ')
    if name == '':
        print('=>必須指定姓名才可修改記錄')
        has_Error = True
    # 無姓名則錯誤，有姓名而無手機或性別也錯誤
    if not has_Error:
        sex = input('請輸入要改變的性別: ')
        phone = input('請輸入要改變的手機: ')
        if sex == '' or phone == '':
            print('性別與手機都必須要修改！')
            has_Error = True
    try:
        if not has_Error:
            #取得原本資料
            cursor.execute(f'SELECT * FROM {tname} WHERE mname = "{name}"')
            odata = cursor.fetchone()
            cursor.execute(f'UPDATE {tname} SET msex = ?, mphone = ? WHERE mname = ?',
                        (sex, phone, name))
            cursor.execute(f'SELECT * FROM {tname} WHERE mname = "{name}"')
            cdata = cursor.fetchone()
    except sqlite3.Error as e:
        print(e)
        has_Error = True
    if not has_Error:
        print()
        print('原資料：')
        print(f'姓名：{odata[1]}，性別：{odata[2]}，手機：{odata[3]}')
        print('=>異動 1 筆記錄')
        print('修改後資料：')
        print(f'姓名：{cdata[1]}，性別：{cdata[2]}，手機：{cdata[3]}')
    # 結束資料庫連線
    end_con_db()


def find_use_phone(tname:str ) -> None:
    ''' tname: Table name
        使用手機查詢資料庫
    '''
    # 連線到資料庫
    con_db()
    # 取得手機
    has_Error = False
    phone = input('請輸入想查詢記錄的手機: ')
    # 取得資料
    try:
        cursor.execute(f'SELECT * FROM {tname} WHERE mphone = "{phone}"')
        cdata = cursor.fetchone()
    except sqlite3.Error as e:
        print(e)
        has_Error = True
    print(cdata)
    if cdata == []:
        print('=>查無資料')
    elif not has_Error:
        print('姓名　　　　性別　手機')
        print('-'*30)
        print(f'{cdata[1]:\u3000<7}{cdata[2]:<5}{cdata[3]}')

    # 結束資料庫連線
    end_con_db()

def delet_all_data(tname: str) -> None:
    ''' tname: Table name
        刪除所有資料
    '''
    # 連線到資料庫
    con_db()
    # 計算資料數量
    cursor.execute(f'SELECT * FROM {tname}')
    data = cursor.fetchall()
    index = len(data)
    # 刪除資料
    has_Error = False
    try:
        cursor.execute(f'DELETE FROM {tname}')
    except sqlite3.Error as e:
        print(e)
        has_Error = True

    if not has_Error:
        print(f'=>異動 {index} 筆記錄')
    # 結束資料庫連線
    end_con_db()