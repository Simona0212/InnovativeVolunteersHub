import json
import os


# 获取当前文件夹下的直接子文件夹
def get_immediate_subdirectories(a_dir):
    return [
        name
        for name in os.listdir(
            a_dir
        )  # 获取当前文件夹下的所有文件和文件夹; name是文件名或文件夹名
        if os.path.isdir(os.path.join(a_dir, name))
    ]  # 判断是否是文件夹


# 获取当前文件夹下的所有文件
def get_immediate_files(a_dir):
    return [
        name
        for name in os.listdir(a_dir)  # 获取当前文件夹下的所有文件和文件夹
        if os.path.isfile(os.path.join(a_dir, name))
    ]  # 判断是否是文件


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
sample_path = os.path.join(BASE_DIR, "sample.json")  # get the directory of sample
sample_data = read_json(sample_path)  # read the sample data

analysis_path = os.path.join(BASE_DIR, "analysis.json")  # get the directory of analysis
analysis_data = read_json(analysis_path)  # read the analysis data

# 统计analysis_data中的"Non-Perfect Labels"标签分布
labels_set = dict()
for analysis_item in analysis_data:
    labels = analysis_item["Non-Perfect Labels"]
    for label in labels:
        if label not in labels_set:
            labels_set[label] = 1
        else:
            labels_set[label] += 1

# 打印标签分布（数量，百分比）
print("Labels Set:")
total = len(analysis_data)
for label, count in labels_set.items():
    print(f"{label}: {count}, {count/total:.2%}")
