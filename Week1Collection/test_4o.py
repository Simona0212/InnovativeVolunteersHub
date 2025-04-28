import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# 找到当前文件夹及其子文件夹下所有test_4o.json文件
json_files = [
    os.path.join(root, f)
    for root, dirs, files in os.walk(current_dir)
    for f in files
    if f.endswith("test_4o.json")
]
# print(json_files)
total_cnt = 0
aligned_cnt = 0
mis_aligned_cnt = 0
severe_miss_cnt = 0
score_4o = 0
score_manual = 0

for json_file in json_files:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        # print(data)
        # do something with data
    # data是list，里面是字典
    # 对每个item，如果有score_manual和score_4o字段
    for item in data:
        if "score_manual" in item and "score_4o" in item:
            # 如果score_manual和score_4o不相等
            score_4o += int(item["score_4o"])
            score_manual += int(item["score_manual"])
            total_cnt += 1
            if int(item["score_manual"]) == int(item["score_4o"]):
                aligned_cnt += 1
            elif abs(int(item["score_manual"]) - int(item["score_4o"])) > 1:
                severe_miss_cnt += 1
            else:
                mis_aligned_cnt += 1

print(f"total: {total_cnt}")
print(f"aligned: {aligned_cnt}")
print(f"mis-aligned: {mis_aligned_cnt}")
print(f"severe mis-aligned: {severe_miss_cnt}")
print(f"score_4o: {score_4o}")
print(f"score_manual: {score_manual}")
