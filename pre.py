import json

contents = []

with open('ccpc_train_v1.0.json', 'r', encoding='utf-8') as f:
    for i in range(10000):
        line = f.readline()
        contents.append(json.loads(line)['content'].replace('|', '，') + "。")

with open('content.txt', 'w', encoding='utf-8') as f:
    for s in contents:
        f.write(s + "\n")