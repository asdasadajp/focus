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

# AppData\Roaming\focus-timer にある blacklist.txt を参照
BLACKLIST_FILE = os.path.join(os.getenv("APPDATA"), "focus-timer", "blacklist.txt")

# デフォルト（exeと同じ場所）の blacklist.txt
script_dir = os.path.dirname(os.path.abspath(__file__))
default_blacklist = os.path.join(script_dir, "blacklist.txt")

# AppData に blacklist.txt がなければ、デフォルトからコピー、なければ空で作成
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

def block_sites(websites=None):
    if websites is None:
        websites = load_blacklist()
    
    if not websites:
        print("⚠️ ブラックリストが空です。")
        return

    try:
        # 現在のhostsファイルの内容を読み込む
        with open(HOSTS_PATH, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
        
        # 新しいエントリを追加
        new_entries = []
        for site in websites:
            if f"{REDIRECT_IP} {site}" not in content:
                new_entries.append(f"{REDIRECT_IP} {site}\n")
                print(f"🔒 {site} をブロックしました。")
            else:
                print(f"✅ {site} はすでにブロックされています。")
        
        # 新しいエントリがある場合のみ書き込み
        if new_entries:
            with open(HOSTS_PATH, "a", encoding="utf-8") as file:
                file.writelines(new_entries)
            print("✅ hostsファイルを更新しました。")
        else:
            print("ℹ️ 新しいブロックは必要ありませんでした。")
            
    except PermissionError:
        print("❌ 'hosts' ファイルにアクセスできません。管理者権限で実行してください。")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    # コマンドライン引数がある場合はそれを使用
    if len(sys.argv) > 1:
        websites = sys.argv[1:]
        block_sites(websites)
    else:
        block_sites()
