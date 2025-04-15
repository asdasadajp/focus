import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 他の処理はそのまま


HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
BLACKLIST_FILE = "blacklist.txt"

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        print("⚠️ blacklist.txt が見つかりません。")
        return []
    with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def unblock_sites():
    websites = load_blacklist()
    if not websites:
        print("⚠️ ブラックリストが空です。")
        return

    with open(HOSTS_PATH, "r+", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(f"{REDIRECT_IP} {site}" in line for site in websites):
                file.write(line)
        file.truncate()
        for site in websites:
            print(f"🔓 {site} のブロックを解除しました。")

if __name__ == "__main__":
    unblock_sites()

