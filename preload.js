const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  onBlacklistData: (callback) => ipcRenderer.on("blacklist-data", (_, data) => callback(data)),
  saveBlacklist: (content) => ipcRenderer.send("save-blacklist", content),
  onSaveResult: (callback) => ipcRenderer.on("save-result", (_, msg) => callback(msg)),
  runPython: (script) => ipcRenderer.send("run-python", script),
  onPythonResult: (callback) => ipcRenderer.on("python-result", (_, msg) => callback(msg)),
});
