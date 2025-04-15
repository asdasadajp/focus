import os

# Windows の hosts ファイルのパス
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

if __name__ == "__main__":
    block_sites()
