# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11xxxxxx  
**系級：** 資管系大一  
**姓名：** 王小明  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) | 從檔案取的所有行資料 | file_lines |
| Q2 d2 (in main) | 圖書館的書籍資料清單  | book_list |
| Q3 c_res (in check) | 檢查資源是否存在 | book_exists |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：**
神祕的單字母變數：d2, l1, p, b, x, f 等完全無意義，難以維護
- **Q2：**
全域變數污染：d2 被定義為全域變數，容易造成狀態管理混亂和測試困難
- **Q3：**
缺乏錯誤處理：檔案讀取和字串分割沒有 try-except，格式錯誤會直接崩潰
- **Q4：**
功能混雜在主函式中：邏輯全塞在 main() 中，難以單元測試和模組化複用
- **Q5：**
缺乏資料驗證：沒檢查 ISBN 或書名的有效性，也沒處理重複借閱等邊界情況

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

我將資料夾中的文件開放給copilot讀取，以便獲得專案的所需訊息，並要求他自己先過一遍題目的敘述，還有答案的要求，先根據這樣子的初步了解，將大概的需求先寫出來，接著我再根據題目所需的要求(例如code smell)再做詳細的判斷，最後再要求其對整個程式做修正

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 幫我詳細讀取Question.md，並根據Answer.md中的問題，將答案寫至聊天室，務必不要直接修改

Prompt B： 幫我進行code smell判斷，再抓取出幾個可能的問題

Prompt C：現在請你根據code smell發現的bug處，幫我修改legacy_lib.py的內容
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？

在執行的過程中，因為我開放讓其讀取整份文件，所以AI清楚知道我的需求是甚麼，並且我在最初下指令時，有明確禁止其直接修改文件，所以不用擔心資料直接被修改的問題，錯誤的部分倒是沒有發現。

2. 發現的問題：AI在第一次執行時，確實漏掉了exit時秀出分類統計的內容，並且排版也不是這麼好看，我讓其補上後又將排版修正了一次

3. 修正的對話：在 exit 時添加分類統計輸出，並將排版改的人性化一點。

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
PS D:\NTUST-0527-Final-master> python .\modern_library.py
=== 圖書管理系統 v1.0 (Modern) ===
命令：add <書名>/<ISBN>/<狀態> | show | borrow <ISBN> | return <ISBN> | exit
> add 深入淺出Python/978001/available
ISBN Exist
> add 資料結構理論/978002/available
ISBN Exist
> add 演算法實作/978003/available
ISBN Exist
> add 重複測試書/978001/available
ISBN Exist
> borrow 978002
Updated
> show
書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> exit

========================================
         📊 系統統計摘要
========================================
  📚 總書籍數:        3 本
  ✅ 可用書籍:        2 本
  📖 已借出書籍:      1 本
  📈 可用率:          66.7%
========================================

👋 感謝使用圖書館管理系統，再見！
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "深入淺出Python",
    "isbn": "978001",
    "status": "available"
  },
  {
    "title": "資料結構理論",
    "isbn": "978002",
    "status": "borrowed"
  },
  {
    "title": "演算法實作",
    "isbn": "978003",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
# 請在此處貼上 git log 內容
e7f0117 (HEAD -> master) Answer  fix
f4a33fd (origin/master) first update
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
# 請貼上你的 Repo 網址
https://github.com/kuanjiTW/B11409032-0527-Final
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
