import json

# 自分のBotのアクセストークンに置き換えてください
with open("secret.json", "r", encoding="utf-8") as f:
    TOKEN = json.load(f)["discord"]["token"]