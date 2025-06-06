# 🧠 Focus Blocker App

このアプリは、学習や作業中に集中を妨げるウェブサイトをブロックする **Windows専用** のデスクトップアプリです。  
Electron（UI）＋ Python（ブロック処理）で構成されています。

---

## 🚀 特徴

- ✅ `blacklist.txt` に指定したサイトを Windows の hosts ファイルを使ってブロック
- ✅ 「ブロック」「解除」ボタンで簡単に切り替え可能
- ✅ スケジュール機能やフォーカスタイマー機能に拡張可能（今後対応予定）

---

## 📁 構成

```


## 🛠️ セットアップ方法

### 1. Node.js & Python のインストール（未インストールなら）

- [Node.js](https://nodejs.org/)
- [Python (3.x)](https://www.python.org/)

---

### 2. 必要パッケージのインストール

```bash
npm install
```

---

### 3. 起動

```bash
npm start
```
<strike>又は、リリースからzipファイルをダウンロードしてください。展開後、管理者モードでfocus-app.exeを実行してください。</strike>


---

## 📄 `blacklist.txt` の書き方

1行につき1つのドメインを記述します：

```
www.youtube.com
twitter.com
netflix.com
```

---

## ⚠️ 注意事項

- **Windowsのhostsファイル編集には管理者権限が必要** です。  
  実行時に Python スクリプトが正常に動作しない場合は、**Electronアプリを管理者権限で起動**してください。
- `blacklist.txt` が存在しない場合や空の場合、警告が表示されます。

---

## 📌 今後の予定（アイデア）

- [ ] スケジュールに基づいた自動ブロック機能
- [ ] ホワイトリストモード（許可されたサイト以外をすべてブロック）
- [ ] 統計表示（どれだけフォーカスできたか）

---



---
#   f o c u s 
 
 
