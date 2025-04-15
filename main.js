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
      nodeIntegration: false // 必要に応じて
    },
  });

  win.loadFile("index.html");

  // blacklist.txt のパス
  const blacklistPath = path.join(process.resourcesPath, 'app/blacklist.txt');

  // blacklist.txt を読み込んでレンダラープロセスに送信
  fs.readFile(blacklistPath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading blacklist.txt:', err);
      return;
    }
    // blacklist.txt の内容をレンダラープロセスに送信
    win.webContents.send('blacklist-data', data);
  });
}

// Python 実行イベントを受け取る
ipcMain.on("run-python", (event, script) => {
  const scriptParts = script.split(" "); // ["manual_focus.py", "block"]
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
