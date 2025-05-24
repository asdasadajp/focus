const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { exec } = require("child_process");
const fs = require("fs");

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.loadFile("index.html");

  // AppData 内の focus-timer ディレクトリ
  const appDataPath = path.join(app.getPath("appData"), "focus-timer");
  const blacklistPath = path.join(appDataPath, "blacklist.txt");

  // フォルダ・ファイルがなければ作成
  if (!fs.existsSync(appDataPath)) {
    fs.mkdirSync(appDataPath);
  }
  if (!fs.existsSync(blacklistPath)) {
    fs.writeFileSync(blacklistPath, "", "utf-8"); // 空ファイル作成
  }

  // HTML の読み込み完了後に blacklist.txt を送信
  win.webContents.on("did-finish-load", () => {
    fs.readFile(blacklistPath, "utf8", (err, data) => {
      if (err) {
        console.error("Error reading blacklist.txt:", err);
        return;
      }
      win.webContents.send("blacklist-data", data);
    });
  });

  // 保存要求を受け取って blacklist.txt を更新
  ipcMain.on("save-blacklist", (event, content) => {
    fs.writeFile(blacklistPath, content, "utf8", (err) => {
      if (err) {
        console.error("Error saving blacklist.txt:", err);
        event.sender.send("save-result", "❌ 保存に失敗しました");
        return;
      }
      event.sender.send("save-result", "✅ 保存完了");
    });
  });
}

// Python スクリプト実行
ipcMain.on("run-python", (event, script) => {
  const scriptParts = script.split(" ");
  const command = `python ${path.join(__dirname, scriptParts[0])} ${scriptParts.slice(1).join(" ")}`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      event.sender.send("python-result", `[エラー]: ${error.message}`);
      return;
    }
    if (stderr) {
      event.sender.send("python-result", `[stderr]: ${stderr}`);
      return;
    }
    event.sender.send("python-result", `[出力]: ${stdout}`);
  });
});

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
