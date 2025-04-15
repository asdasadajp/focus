# script.py
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("✅ Python スクリプトが正常に実行されました！")
