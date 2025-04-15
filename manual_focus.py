import time
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
BLACKLIST_FILE = "blacklist.txt"

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        print("⚠️ blacklist.txt が見つかりません。")
        return []
    with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def block_sites():
    websites = load_blacklist()
    if not websites:
        print("⚠️ ブラックリストが空です。")
        return

    with open(HOSTS_PATH, "r+", encoding="utf-8", errors="ignore") as file:
        content = file.read()
        for site in websites:
            if site not in content:
                file.write(f"{REDIRECT_IP} {site}\n")
                print(f"🔒 {site} をブロックしました。")
            else:
                print(f"✅ {site} はすでにブロックされています。")

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

def block():
    print("🛡️ ブロック処理を開始します...")
    block_sites()

def unblock():
    print("🔓 ブロック解除処理を開始します...")
    unblock_sites()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "block":
            block()
        elif sys.argv[1] == "unblock":
            unblock()
