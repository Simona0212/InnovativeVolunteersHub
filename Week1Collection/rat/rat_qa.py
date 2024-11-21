import json
import os


# 读取json文件
def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# 写入json文件
def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # get the directory of this file
rat_data_path = os.path.join(BASE_DIR, "labels_test.json")
rat_qa_path = os.path.join(BASE_DIR, "rat_qa.json")

rat_data = read_json(rat_data_path)
rat_qa = read_json(rat_qa_path)

# 先判断有无重复、缺失数据
qa_foldername_set = set([item["foldername"] for item in rat_qa])
data_foldername_set = set([data["foldername"] for data in rat_data])
print("qa数据量：", len(rat_qa))
print("data数据量：", len(rat_data))
if len(qa_foldername_set) != len(rat_qa):
    print("重复数据：", len(rat_qa) - len(qa_foldername_set))
if len(data_foldername_set) != len(rat_data):
    print("重复数据：", len(rat_data) - len(data_foldername_set))
if len(data_foldername_set - qa_foldername_set) > 0:
    print(
        "缺失数据1：", data_foldername_set - qa_foldername_set
    )  # data中有而qa中没有的数据
    print("缺失数据量1：", len(data_foldername_set - qa_foldername_set))
    print("缺失数据2：", qa_foldername_set - data_foldername_set)
    print("缺失数据量2：", len(qa_foldername_set - data_foldername_set))

# for item in rat_qa:
#     if item["foldername"] in (qa_foldername_set - data_foldername_set):
#         # 将foldername字符串中左括号(前的空格删去（其余的空格不删）
#         item["foldername"] = item["foldername"].replace(" (", "(")
#         print("fixed：", item["foldername"])
#         write_json(rat_qa_path, rat_qa)


# 将qa的explanation和reasoning转移至data
# 先建立foldername到qa的映射
qa_foldername_dict = dict()
for item in rat_qa:
    qa_foldername_dict[item["foldername"]] = item

for data in rat_data:
    foldername = data["foldername"]
    if foldername in qa_foldername_dict:
        qa_item = qa_foldername_dict[foldername]
        data["explanation"] = qa_item["explanation"]
        data["reasoning"] = qa_item["reasoning"]
        data["hop_count"] = qa_item["reasoning"].count("→")
    else:
        print("缺失数据：", foldername)
write_json(rat_data_path, rat_data)
print("转移完成")

# rat_qa = []
# for data in rat_data:
#     item = dict()
#     item["foldername"] = data["foldername"]
#     item["word1"] = data["images"][0]["description"]
#     item["word2"] = data["images"][1]["description"]
#     item["answer"] = data["relation"]
#     item["explanation"] = ""
#     item["reasoning"] = ""
#     rat_qa.append(item)
# write_json(rat_qa_path, rat_qa)
