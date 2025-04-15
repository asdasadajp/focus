const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  runPython: (script) => ipcRenderer.send("run-python", script),
  onPythonResult: (callback) => ipcRenderer.on("python-result", (_, data) => callback(data)),
});
