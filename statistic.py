import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # get the directory of this file
INCONTEXT_DIR = os.path.join(
    BASE_DIR, "Incontext_Images"
)  # get the directory of incontext
TOTAL_RIA_PATH = os.path.join(BASE_DIR, "Week1Collection")
MULTI_PATH = os.path.join(BASE_DIR, "Multi_Images")
PURE_SINGLE_PATH = os.path.join(BASE_DIR, "Pure_Single_Images")

name_list_incontext = [
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

name_list_multi = [
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

name_list_pure = [
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
]

name_list_collection = [
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

incontext_file = "data_context.json"
multi_file = "data_multi.json"
pure_file = "data_single.json"
collection_file = "labels_test.json"


# 遍历context，计数
def count_incontext():
    count = 0
    for name in name_list_incontext:
        with open(
            os.path.join(INCONTEXT_DIR, name, incontext_file), "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
            count += len(data)
            print(name, len(data))
    return count


# 遍历multi，计数
def count_multi():
    count = 0
    for name in name_list_multi:
        with open(
            os.path.join(MULTI_PATH, name, multi_file), "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
            count += len(data)
            print(name, len(data))
    return count


# 遍历pure，计数
def count_pure():
    count = 0
    for name in name_list_pure:
        with open(
            os.path.join(PURE_SINGLE_PATH, name, pure_file), "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
            count += len(data)
            print(name, len(data))
    return count


# 遍历collection，计数
def count_collection():
    count = 0
    for name in name_list_collection:
        with open(
            os.path.join(TOTAL_RIA_PATH, name, collection_file), "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
            count += len(data)
            print(name, len(data))
    return count


# 打印统计结果
print("Incontext Images: ", count_incontext())
print("Multi Images: ", count_multi())
print("Pure Single Images: ", count_pure())
print("Collection: ", count_collection())
# print("Multi + Pure Single: ", count_multi() + count_pure())
