from pkg.lib import create_dbandtable, get_json, import_data, show_list

# 設立檔案名稱
FILENAME = 'pass.json'
# 預設啟動變數
login_statue = False
# 取得字典
user_dict = get_json(FILENAME)
# 確認登入資料
account = input('請輸入帳號：')
password = input('請輸入密碼：')
# 判斷登入是否正確
for i in user_dict:
    if account == i['帳號']:
        if password == i['密碼']:
            login_statue = True
if not login_statue:
    print('=>帳密錯誤，程式結束')

# 登入成功後執行系統
while login_statue:
    # 顯示選單
    show_list()
    # 使用者選擇
    choice = input('請輸入您的選擇 [0-7]: ')
    # 選擇離開
    if choice == '0' or choice == '':
        login_statue = False
        continue
    # 非離開給予回應
    choice = int(choice)
    match choice:
        case 1:
            create_dbandtable()
        case 2:
            import_data('members.txt')
        case 3:
            print('3')
        case 4:
            print('4')
        case 5:
            print('5')
        case 6:
            print('6')
        case 7:
            print('7')
        case _:
            print('無效的選擇')
