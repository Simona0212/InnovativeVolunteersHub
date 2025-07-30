import os
import json

print("____RIA____")

cnt_en_ria = 0
cnt_non_en_ria = 0
score_en_ria = 0
score_non_en_ria = 0
modelname = "gpt-4o"

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

data_single = "labels_test.json"

json_files_single = [
    "./Week1Collection/" + names_single[i] + "/" + modelname + "_judge.json"
    for i in range(len(names_single))
]


for i in range(len(json_files_single)):  # 不同name
    non_en_data_single = set()
    en_data_single = set()
    with open(
        "./Week1Collection/" + names_single[i] + "/" + data_single,
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)  # list
        for item in data:
            if item["language"] == "English":
                en_data_single.add(item["foldername"])
            else:
                non_en_data_single.add(item["foldername"])
    with open(json_files_single[i], "r", encoding="utf-8") as f:
        judge = json.load(f)  # judge是字典
        for key in judge:
            if key in en_data_single:
                if judge[key].get("score_4o") in set(["2", "1", "0", "4", "3"]):
                    if key in en_data_single:
                        cnt_en_ria += 1
                        score_en_ria += int(judge[key]["score_4o"])
                    elif key in non_en_data_single:
                        cnt_non_en_ria += 1
                        score_non_en_ria += int(judge[key]["score_4o"])
                    else:
                        print(f"Error: not in single language:{names_single[i]}|{key}")


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
    "./Multi_Images/" + names_multi[i] + "/" + modelname + "_multi_judge.json"
    for i in range(len(names_multi))
]

data_multi = "data_multi.json"

# multi
for i in range(len(json_files_multi)):
    non_en_data_multi = set()
    en_data_multi = set()
    with open(
        "./Multi_Images/" + names_multi[i] + "/" + data_multi, "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
        for item in data:
            if item["language"] == "English":
                en_data_multi.add(item["foldername"])
            else:
                non_en_data_multi.add(item["foldername"])
    with open(json_files_multi[i], "r", encoding="utf-8") as f:
        data = json.load(f)  # data是字典
        for key in data:
            # data[key]是列表
            for i, item in enumerate(data[key]):
                if item is None:
                    continue
                if isinstance(item, dict) and item.get("score_4o") in set(
                    ["2", "1", "0", "4", "3"]
                ):
                    if key in en_data_multi:
                        cnt_en_ria += 1
                        score_en_ria += int(item["score_4o"])
                    elif key in non_en_data_multi:
                        cnt_non_en_ria += 1
                        score_non_en_ria += int(item["score_4o"])
                    else:
                        print(
                            f"Error: not in multi language:{names_multi[i]}|{key}|{i}"
                        )

sr_eng_ria = score_en_ria / cnt_en_ria / 4
sr_non_eng_ria = score_non_en_ria / cnt_non_en_ria / 4
sr = (score_en_ria+ score_non_en_ria) / (cnt_en_ria + cnt_non_en_ria) / 4

print("english cnt:", cnt_en_ria)
print("english score:", sr_eng_ria)
print("non-english cnt:", cnt_non_en_ria)
print("non-english score:", sr_non_eng_ria)
print(
    "harmonic mean of eng score and non-eng score:",
    2 * sr_eng_ria * sr_non_eng_ria / (sr_eng_ria + sr_non_eng_ria),
)
print("sr:", sr)


print("___ICA___")
cnt_en_ica = 0
cnt_non_en_ica = 0
score_en_ica = 0
score_non_en_ica = 0
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
    "./Incontext_Images/" + names_ica[i] + "/" + "judge_" + modelname + ".json"
]
data_ica = "data_context.json"

for i in range(len(json_files_ica)):
    non_en_data_ica = set()
    en_data_ica = set()
    with open(
        "./Incontext_Images/" + names_ica[i] + "/" + data_ica, "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
        for item in data:
            if item["language"] == "English":
                en_data_ica.add(item["foldername"])
            else:
                non_en_data_ica.add(item["foldername"])
    with open(json_files_ica[i], "r", encoding="utf-8") as f:
        data = json.load(f)  # data是字典
        for key in data:
            # data[key]是列表
            for item in data[key]:
                if isinstance(item, dict) and item.get("score_4o") in set(
                    ["2", "1", "0", "4", "3"]
                ):
                    if key in en_data_ica:
                        cnt_en_ica += 1
                        score_en_ica += int(item["score_4o"])
                    elif key in non_en_data_ica:
                        cnt_non_en_ica += 1
                        score_non_en_ica += int(item["score_4o"])
                    else:
                        print(f"Error: not in ica language:{names_ica[i]}|{key}")
# # ica
# for i in range(len(json_files_ica)):
#     with open(json_files_ica[i], "r", encoding="utf-8") as f:
#         data = json.load(f)  # data是字典
#         for key in data:
#             # data[key]是列表
#             for item in data[key]:
#                 if isinstance(item, dict) and item.get("score_4o") in set(
#                     ["2", "1", "0", "4", "3"]
#                 ):
#                     total_score += int(item["score_4o"])
#                     cnt += 1
#                     if item["score_4o"] == "4":
#                         cnt4 += 1
#                     elif item["score_4o"] == "3":
#                         cnt3 += 1

# print("---ICA---")
# print(cnt)
# print("Qwen HR score:", total_score / cnt / 5)
# print("Qwen HR 4 score:", cnt4 / cnt)
# print("Qwen HR 3 score:", (cnt3 + cnt4) / cnt)
# print("Qwen tri-HR score:", cnt3 / cnt)
