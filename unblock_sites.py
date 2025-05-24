import os
import sys
import io
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"

# AppData の専用ディレクトリ
app_dir = os.path.join(os.getenv("APPDATA"), "focus-timer")
os.makedirs(app_dir, exist_ok=True)

# AppData にある blacklist.txt を参照
BLACKLIST_FILE = os.path.join(app_dir, "blacklist.txt")

# デフォルト（実行ファイルと同じ場所）の blacklist.txt
script_dir = os.path.dirname(os.path.abspath(__file__))
default_blacklist = os.path.join(script_dir, "blacklist.txt")

# AppData に blacklist.txt がなければ、デフォルトからコピー or 空作成
if not os.path.exists(BLACKLIST_FILE):
    if os.path.exists(default_blacklist):
        shutil.copyfile(default_blacklist, BLACKLIST_FILE)
    else:
        with open(BLACKLIST_FILE, "w", encoding="utf-8") as f:
            f.write("")
        print("⚠️ デフォルトの blacklist.txt がなかったため、空ファイルを作成しました。")

def load_blacklist():
    try:
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"❌ blacklist.txt を読み込めませんでした: {e}")
        return []

def unblock_sites():
    websites = load_blacklist()
    if not websites:
        print("⚠️ ブラックリストが空です。")
        return

    try:
        with open(HOSTS_PATH, "r+", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate(0)  # 中身をクリア

            for line in lines:
                if not any(f"{REDIRECT_IP} {site}" in line for site in websites):
                    file.write(line)

        for site in websites:
            print(f"🔓 {site} のブロックを解除しました。")

    except PermissionError:
        print("❌ 'hosts' ファイルにアクセスできません。管理者権限で実行してください。")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    unblock_sites()
