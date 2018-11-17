# election-board-map

1. [初步構想](https://hackmd.io/EtyCkRwRSTGov-ODJdO95A)
2. 以不干擾官方開發，保持整合彈性為原則，所以不預設後端架構，完全前端解決

## 準備資料

目前最新的資料已經放在 git 裡，如果想要自己跑一份的話，請執行以下步驟：

1. 載入資料
   1. 下載官方 [postgres dump](https://projects.readr.tw/election-board/dumps/election_board_1541565982.dump)
   2. 安裝 Postgres + PostGIS
   2. `pg_restore -d <資料庫名稱> xxx.dump -x  -U <帳號名稱>`
2. 用 Django 匯出
   1. 裝一下 Django `pip install -r requirements.txt && cd backend`
   3. 在 backend/settings.py 設定 db
   4. 假裝有作 migration `python manage.py migrate --fake`
   5. 整理一下資料 `python manage.py cleandata`
   6. 匯出資料 `python manage.py export`


## 執行 UI

1. 所有程式都在 `ui` 底下
1. 安裝所需套件 `npm i`
1. 執行開發環境 `npm run dev` ，網頁在 `http://localhost:3000/election-board-map`
2. 建立線上版本 `npm run generate`

更多使用方式請參見 [nuxt](https://nuxtjs.org/)
