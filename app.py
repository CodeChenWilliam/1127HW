from pkg.modu import get_json

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
    print('正式開始')
