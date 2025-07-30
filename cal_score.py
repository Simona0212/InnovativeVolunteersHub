import os
import json

names_single = [
    "djt",
    "fxt",
    "fxx",
    "hzm",
    "jhy",
    "kjx",
    "li-rat",
    "lny",
    "rat",
    "wzd",
    "zdw",
    "zql",
]
json_files_single = [
    "./Week1Collection/djt/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/fxt/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/fxx/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/hzm/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/jhy/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/kjx/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/li-rat/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/lny/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/rat/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/wzd/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/zdw/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
    "./Week1Collection/zql/moonshotai\Kimi-VL-A3B-Instruct_judge_new.json",
]

# json_files_single = [
#     "./Week1Collection/djt/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/fxt/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/fxx/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/hzm/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/jhy/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/kjx/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/li-rat/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/lny/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/rat/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/wzd/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/zdw/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
#     "./Week1Collection/zql/Qwen/Qwen2.5-VL-7B-Instruct_judge_new.json",
# ]

cnt = 0
total_score = 0
cnt4 = 0
cnt3 = 0

# single
for i in range(len(json_files_single)):
    with open(json_files_single[i], "r", encoding="utf-8") as f:
        data = json.load(f)  # data是字典
        for key in data:
            if data[key].get("score_4o") in set(["2", "1", "0", "4", "3"]):
                total_score += int(data[key]["score_4o"])
                cnt += 1
                if data[key]["score_4o"] == "4":
                    cnt4 += 1
                elif data[key]["score_4o"] == "3":
                    cnt3 += 1


names_multi = [
    "djt",
    "fxt",
    "fxx",
    "hzm",
    "kjx",
    "li-rat",
    "lny",
    "rat",
    "wzd",
    "zdw",
    "zql",
]
json_files_multi = [
    "./Multi_Images/djt/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/fxt/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/fxx/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/hzm/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/kjx/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/li-rat/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/lny/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/rat/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/wzd/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/zdw/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
    "./Multi_Images/zql/moonshotai\Kimi-VL-A3B-Instruct_multi_judge.json",
]

# json_files_multi = [
#     "./Multi_Images/djt/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/fxt/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/fxx/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/hzm/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/kjx/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/li-rat/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/lny/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/rat/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/wzd/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/zdw/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
#     "./Multi_Images/zql/Qwen/Qwen2.5-VL-7B-Instruct_multi_judge.json",
# ]

# multi
for i in range(len(json_files_multi)):
    with open(json_files_multi[i], "r", encoding="utf-8") as f:
        data = json.load(f)  # data是字典
        for key in data:
            # data[key]是列表
            for item in data[key]:
                if isinstance(item, dict) and item.get("score_4o") in set(
                    ["2", "1", "0", "4", "3"]
                ):
                    total_score += int(item["score_4o"])
                    cnt += 1
                    if item["score_4o"] == "4":
                        cnt4 += 1
                    elif item["score_4o"] == "3":
                        cnt3 += 1

print("---RIA---")
print("cnt:", cnt)
print("Qwen HR score:", total_score / cnt / 4)
print("Qwen HR 4 score:", cnt4 / cnt)
print("Qwen HR 3 score:", (cnt3 + cnt4) / cnt)
print("Qwen tri-HR score:", cnt3 / cnt)

cnt = 0
total_score = 0
cnt4 = 0
cnt3 = 0

names_ica = [
    "djt",
    "fxt",
    "ljf",
    "lny",
    "tc",
    "wjl",
    "wzd",
    "zdw",
    "zhb",
]
json_files_ica = [
    "./Incontext_Images/djt/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/fxt/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/ljf/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/lny/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/tc/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/wjl/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/wzd/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/zdw/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
    "./Incontext_Images/zhb/moonshotai/judge_moonshotai_Kimi-VL-A3B-Instruct.json",
]

# json_files_ica = [
#     "./Incontext_Images/djt/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/fxt/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/ljf/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/lny/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/tc/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/wjl/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/wzd/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/zdw/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
#     "./Incontext_Images/zhb/Qwen/judge_Qwen_Qwen2.5-VL-7B-Instruct.json",
# ]


# ica
for i in range(len(json_files_ica)):
    with open(json_files_ica[i], "r", encoding="utf-8") as f:
        data = json.load(f)  # data是字典
        for key in data:
            # data[key]是列表
            for item in data[key]:
                if isinstance(item, dict) and item.get("score_4o") in set(
                    ["2", "1", "0", "4", "3"]
                ):
                    total_score += int(item["score_4o"])
                    cnt += 1
                    if item["score_4o"] == "4":
                        cnt4 += 1
                    elif item["score_4o"] == "3":
                        cnt3 += 1

print("---ICA---")
print(cnt)
print("Qwen HR score:", total_score / cnt / 4)
print("Qwen HR 4 score:", cnt4 / cnt)
print("Qwen HR 3 score:", (cnt3 + cnt4) / cnt)
print("Qwen tri-HR score:", cnt3 / cnt)
