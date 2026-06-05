# LINE AI Chatbot

使用 LINE Messaging API 與 CGU LLM API 建立的 AI 聊天機器人。

## 功能

* AI 問答（gpt-5.4-mini）
* 對話記憶（最近 100 筆）
* JSON 持久化儲存
* LINE Bot 即時聊天
* pyngrok 自動建立公開網址

---

## 環境需求

* Python 3.11
* Conda（建議）

---

## 建立虛擬環境

```bash
conda create -n linebot python=3.11
conda activate linebot
```

---

## 安裝套件

```bash
pip install -r requirements.txt
```

---

## 建立 .env

在專案根目錄建立 `.env`：

```env
CHANNEL_ACCESS_TOKEN=你的_LINE_CHANNEL_ACCESS_TOKEN
CHANNEL_SECRET=你的_LINE_CHANNEL_SECRET
CGU_OPENAI_API_KEY=你的_CGU_API_KEY
```

---

## Ngrok 設定

本專案使用 pyngrok 建立公開網址。

### 1. 註冊 ngrok 帳號

前往：

https://dashboard.ngrok.com/

註冊並登入帳號。

---

### 2. 取得 Authtoken

登入後至：

```text
Getting Started
→ Your Authtoken
```

取得你的：

```text
YOUR_AUTHTOKEN
```

---

### 3. 安裝並設定 ngrok

下載 ngrok：

https://ngrok.com/download

解壓縮後開啟 PowerShell，執行：

```bash
ngrok config add-authtoken YOUR_AUTHTOKEN
```

例如：

```bash
ngrok config add-authtoken 2abcxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

成功後會看到：

```text
Authtoken saved to configuration file
```

---

### 4. 驗證安裝

```bash
ngrok version
```

若成功顯示版本資訊，即表示設定完成。

---

## LINE Developers 設定

### 1. 建立 Messaging API Channel

至 LINE Developers 建立 Messaging API Channel。

取得：

* Channel Access Token
* Channel Secret

並填入 `.env`

---

### 2. 啟動程式

執行：

```bash
python linechatbot.py
```

啟動後畫面會顯示類似：

```text
https://xxxxxxxx.ngrok-free.app
```

---

### 3. 設定 Webhook URL

進入：

```text
LINE Developers
→ Messaging API
→ Webhook settings
```

找到：

```text
Webhook URL
```

將 ngrok 網址後面加上：

```text
/callback
```

例如：

```text
https://xxxxxxxx.ngrok-free.app/callback
```

填入 Webhook URL 欄位。

---

### 4. 啟用 Webhook

確認以下設定：

```text
Webhook URL
https://xxxxxxxx.ngrok-free.app/callback

Use webhook
Enabled
```

點選：

```text
Verify
```

若顯示：

```text
Success
```

表示 LINE 已成功連線至你的 Flask Server。

---

### 5. 加入 Bot 好友

回到：

```text
Messaging API
```

頁面。

使用：

```text
QR Code
```

或：

```text
Bot Basic ID
```

將 Bot 加入好友。

之後即可開始與 AI 聊天。

---

### 注意

每次重新執行程式時：

```bash
python linechatbot.py
```

ngrok 都可能產生新的網址，例如：

```text
https://abcd1234.ngrok-free.app
```

此時必須重新更新：

```text
Webhook URL
```

改為：

```text
https://abcd1234.ngrok-free.app/callback
```

否則 LINE 將無法收到訊息。


---

## 指令

### 查看記憶狀態

```text
@記憶狀態
```

顯示目前保存的聊天記錄數量。

---

### 清除記憶

```text
@清除記憶
```

刪除目前使用者所有聊天記錄。

---

### 幫助

```text
@幫助
```

顯示可用指令。

---

## 專案結構

```text
.
├── linechatbot.py
├── server.py
├── requirements.txt
├── .env
└── chat_history.json
```

---

## 聊天記錄

聊天紀錄會自動儲存在：

```text
chat_history.json
```

每位使用者擁有獨立聊天記錄。

系統最多保存最近 100 筆對話內容。

重新啟動程式後聊天記錄仍會保留。

---

## 注意事項

* 請勿將 `.env` 上傳至 GitHub。
* 請勿公開自己的 LINE Token。
* 請勿公開自己的 Channel Secret。
* 請勿公開自己的 CGU API Key。
* `chat_history.json` 建議加入 `.gitignore`。
* pyngrok 首次執行時可能會自動下載 ngrok。
* 建議先完成 `ngrok config add-authtoken YOUR_AUTHTOKEN` 設定，以避免匿名模式限制。

---

## GitHub 建議設定

建立 `.gitignore`：

```gitignore
.env
chat_history.json
__pycache__/
*.pyc
.vscode/
.idea/
```

---

## 作者

National Formosa University

Cloud Computing Course Project

LINE AI Chatbot with CGU LLM API
